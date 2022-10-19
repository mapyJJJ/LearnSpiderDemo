#!/usr/bin/python3
# 命令行视频下载工具，下载b站对应链接下的视频，电影，动漫
# 不依赖其他第三方平台，非破解脚本！！！

# 视频下载格式：flv，mp4，支持链接批量下载
# 获取高清分辨率或者一些需要大会员才能解锁的分辨率时，需要本人账号登陆后拿到cookie，才能下载
# example:

# python3 bilibili_video_download_cli.py --url "<链接>" --type "flv" --outputdir /home/user/video/
# python3 bilibili_video_download_cli.py --url "<链接>" --type "flv" --outputdir /home/user/video/ --cookiefile ./mycookie.txt
# python3 bilibili_video_download_cli.py --urlfile ./urls.txt --type "flv" --outputdir /home/user/video/ --cookiefile ./mycookie.txt
# 需要将cookie写入mycookie.txt中，如果不指定cookie，一般只能下载360p
# urls.txt 中，每个链接地址占用一行

import argparse
import functools
import hashlib
import os
import random
import re
import sys
import time
import types
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Generic, List, Literal, Tuple, TypeVar, Union, cast

import requests
import rich
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


F = TypeVar("F")


class HandleUnExceptError(Generic[F]):
    def __init__(self, method: Callable) -> None:
        functools.wraps(method)(self)

    def __call__(self, *args, **kwds) -> F:
        try:
            return self.__wrapped__(*args, **kwds)  # type: ignore
        except Exception as e:
            rich.print(f"[red]【error】程序执行出错，报错信息如下: \n {e.__str__()}")
            sys.exit(0)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return types.MethodType(self, instance)


class Config:
    def __init__(self, cookie: str = "", cookie_file: str = "") -> None:
        # 如果是未登录状态的cookie，是不支持下载高分辨率的视频的
        if cookie:
            self.cookie = cookie
        elif cookie_file:
            self.cookie = open(cookie_file).read()
        else:
            self.cookie = ""

        self.cookie = self.cookie.strip()

        # request timeout
        self.timeout = 10

        # 每次连接拉取的数据量
        self.each_download_size = 80 * 1024 * 1024

        # 断点续传，程序中断时间
        self.rest_download_time = 3

        # player_info_api
        self.player_info_api = "https://api.bilibili.com/x/player/playurl?avid=%s&cid=%s&qn=%s&fnver=0&fnval=0&fourk=1&ep_id=&type=%s&otype=json"

        # get aid&cid api
        self.get_video_id_api = "https://api.bilibili.com/pgc/view/web/season"

        # fake ua
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727)",
        ]

        # headers for parse page
        self.parse_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "max-age=0",
            "cookie": self.cookie,
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": random.choice(self.user_agent_list),
        }

        # header for download req
        self.download_headers = {
            "user-agent": random.choice(self.user_agent_list),
            "referer": "https://www.bilibili.com",  # NOTICE refere一定需要，否则会被403
            "cookie": self.cookie,
        }

        # qn
        self.qn_map = {
            120: "4K 超清",
            116: "1080P 60帧",
            80: "1080P 高清",
            64: "720P 高清",
            32: "480P 清晰",
            16: "360P 流畅",
        }

        # terminal log
        self.display_req_error_log = lambda: rich.print(
            "[red]【×】请求连接失败，被拒绝或者请求超时，检查是否未联网或者使用了代理!!!"
        )
        self.display_video_qn_log = lambda desc: rich.print(
            f"[green]【√】获取到的视频分辨率为: {desc}"
        )
        self.display_all_video_url_useless_log = lambda: rich.print(
            f"[red] 【×】所有视频地址都不可获取，无法下载该视频"
        )
        self.display_success_download_log = lambda file_path: rich.print(
            f"""
            [green]【√】下载成功！
            视频保存至 {file_path}
            """
        )
        self.display_video_has_exists_log = lambda title: rich.print(
            f"[yellow]【?】视频已经存在 {title}, 如需重新下载请先手动删除原视频后重试!"
        )
        self.display_cannot_parse_this_link_log = lambda url: rich.print(
            f"[red]【×】无法解析该页面（确认cookie是否有效） : {url}"
        )


class RequestMixin:
    def __init__(self, config: Config) -> None:
        self.config = config

    def request(
        self,
        url,
        headers,
        response_type: Literal["json", "text"] = "text",
    ) -> Union[str, dict]:
        try:
            if response_type == "text":
                res = requests.get(
                    url, headers=headers, timeout=self.config.timeout
                ).content.decode()
            else:
                res = requests.get(
                    url, headers=headers, timeout=self.config.timeout
                ).json()
        except requests.exceptions.ConnectionError:
            config.display_req_error_log()
            sys.exit(0)
        return res


@dataclass
class ParsePageMainData:
    """获得video链接的关键信息字段"""

    cid: int
    aid: int
    title: str
    last_ep_id: int


class Spider(RequestMixin):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    @HandleUnExceptError[ParsePageMainData]
    def parse_page_get_data(self, page_url: str) -> ParsePageMainData:
        """在html中获取video相关id
        除了影视番剧等视频，其他所有由up主上传的视频都可用这个方法取到id信息
        """
        page_html_text = cast(str, self.request(page_url, self.config.parse_headers))
        avid_list = re.findall(r"aid=(\d+)", page_html_text) or re.findall(
            r"\"aid\":(\d+)", page_html_text
        )
        cid_list = re.findall(r"cid=(\d+)", page_html_text) or re.findall(
            r"\"cid\":(\d+)", page_html_text
        )
        # assert avid_list and cid_list, "[error] not found cid or avid"
        title = re.findall(r"<h1 title=\"(.*?)\"", page_html_text) or [
            str(int(datetime.now().timestamp()))
        ]

        last_ep_ids = re.findall(r"\"last_ep_id\":(\d+)", page_html_text) or (0,)
        return ParsePageMainData(
            title=str(title[0]),
            last_ep_id=int(last_ep_ids[0]),
            cid=([_cid for _cid in cid_list if int(_cid)] or (0,))[0],
            aid=([_aid for _aid in avid_list if int(_aid)] or (0,))[0],
        )

    @HandleUnExceptError[Tuple[int, int]]
    def parse_cid_aid_api(self, api_url: str, last_ep_id: int) -> Tuple[int, int]:
        """使用api获取video相关id
        番剧电影等链接都需要通过这种方式拿到id信息
        """

        data = cast(
            dict,
            self.request(
                api_url, headers=self.config.parse_headers, response_type="json"
            ),
        )
        # result , episodes, id
        for _item in data["result"]["episodes"]:
            if int(last_ep_id) == int(_item["id"]):
                return _item["aid"], _item["cid"]
        return (0, 0)

    @HandleUnExceptError
    def parse_player_info_get_video_urls(self, info_api: str, qn: int) -> List[str]:
        """解析视频详情api，获取player_url
        包含 主要地址 和 几个备用的cdn地址
        """

        player_urls = []

        info_data = cast(
            dict,
            self.request(info_api, self.config.parse_headers, response_type="json"),
        )

        quality = info_data["data"]["quality"]
        if desc := self.config.qn_map.get(quality):
            self.config.display_video_qn_log(desc)
        durl_data = info_data["data"]["durl"][0]
        player_urls.append(durl_data["url"])
        player_urls.extend(durl_data["backup_url"])

        return player_urls

    def download_video(
        self,
        page_url: str,
        urls: List[str],
        title: str,
        _type: Literal["flv", "mp4"],
        outputdir: str = ".",
    ):
        """请求 player_url , 传输视频数据到本地
        - 对视频uri 和 title进行摘要，防止下载重复的视频
        - 断点续传 : 对于较大的视频文件，长时间的tcp传输可能会导致b站服务器主动关闭连接
        - 切换可用的cdn地址，提供了几个备用的视频地址，程序在未能成功建立连接的情况下，需要自动切换
        """

        def _do(url, retry_download: bool = False):
            nonlocal video_size, ncalls
            ncalls += 1
            has_file_size = 0
            if os.path.exists(file_path):
                if not retry_download:
                    self.config.display_video_has_exists_log(title)
                    sys.exit(0)
                has_file_size = os.path.getsize(file_path)

            f = open(file_path, "ab+")
            stream_file = requests.get(
                url,
                stream=True,
                timeout=self.config.timeout,
                headers=self.config.download_headers,
            )
            if not video_size:
                video_size = int(stream_file.headers["Content-Length"])
            with Progress(  # 使用 rich progress 展示更好看的进度条
                TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "|",
                DownloadColumn(binary_units=True),
                "|",
                TransferSpeedColumn(),
                "|",
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(
                    "download",
                    filename=filename + "|请求次数" + str(ncalls),
                    total=video_size,
                )
                progress.update(task, advance=has_file_size)
                current_size = 0
                try:
                    for chunk in stream_file.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            size = chunk.__sizeof__()
                            progress.update(task, advance=size)
                            current_size += size
                        if current_size >= self.config.each_download_size:
                            break
                except Exception:
                    pass
            f.close()
            has_file_size = os.path.getsize(file_path)
            if has_file_size < video_size:
                time.sleep(self.config.rest_download_time)
                self.config.download_headers["Range"] = "bytes=%d-" % has_file_size
                _do(url, True)
            return

        md5 = hashlib.md5()
        mixed_path_title = page_url.partition("?")[0] + title
        md5.update(mixed_path_title.encode("utf-8"))
        hash_str = md5.hexdigest()

        filename = f"{title}_{hash_str}.{_type}"
        file_path = (
            f"{outputdir if outputdir.endswith('/') else outputdir + '/'}{filename}"
        )
        ncalls = 0
        video_size = 0

        for _url in urls:
            try:
                _do(_url)
                break
            except Exception as e:
                os.remove(file_path)
                if _url == urls[-1]:
                    self.config.display_all_video_url_useless_log()
                    sys.exit(0)
                continue

        self.config.display_success_download_log(file_path)
        return

    def gen_player_info_api(self, avid, cid, qn: int, _type: Literal["flv", "mp4"]):
        return str(config.player_info_api % (avid, cid, qn, _type))

    def classify_page_url(self, url) -> Tuple[bool, str]:
        if ep_video := re.match(r"^https?://www.bilibili.com/\S+/ep(\d+)$", url):
            return (
                True,
                config.get_video_id_api + f"?ep_id={ep_video.groups()[0]}",
            )

        # if season_video := re.match(r"^https?://www.bilibili.com/\S+/ss(\d+)$", url):
        #     return (
        #         True,
        #         config.get_video_id_api + f"?season_id={season_video.groups()[0]}",
        #     )

        return (False, "")


def main():
    if not (args.url or args.urlfile):
        rich.print("[yellow]【warning】url 和 urlfile参数不能都为空!")
        parse.print_help()
        sys.exit(0)

    urls = []
    if args.urlfile:
        with open(args.urlfile, "r") as f:
            urls += [_u.strip() for _u in f.readlines()]
    if args.url:
        urls.append(args.url)

    spider = Spider(config)

    # 多线程同时拉取有被限速的风险，
    # 而且基本上一个4k视频最少也是几百兆
    # 在本地带宽拉满的情况下 多线程的意义也不大
    for url in urls:
        spical_video, get_cid_aid_api = spider.classify_page_url(url.partition("?")[0])
        data = spider.parse_page_get_data(url)
        if spical_video:
            if not data.last_ep_id:
                config.display_cannot_parse_this_link_log(url)
                continue
            aid, cid = spider.parse_cid_aid_api(get_cid_aid_api, data.last_ep_id)
            data.aid = aid
            data.cid = cid

        player_info_api = spider.gen_player_info_api(
            data.aid, data.cid, qn=args.qn, _type=args.type
        )

        player_urls = spider.parse_player_info_get_video_urls(player_info_api, args.qn)
        spider.download_video(url, player_urls, data.title, args.type, args.outputdir)


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="b站视频下载工具")
    parse.add_argument("--url", help="视频地址链接", default="")
    parse.add_argument("--urlfile", help="批量下载对应文件中的所有地址，每个链接一行", default="")
    parse.add_argument(
        "--qn",
        help="""
    分辨率大小
    120: "4K 超清",
    116: "1080P 60帧",
    80: "1080P 高清",
    64: "720P 高清",
    32: "480P 清晰",
    16: "360P 流畅",
    """,
        default=120,
    )
    parse.add_argument(
        "--type", help="保存文件类型 mp4 | flv， 有的视频mp4格式获取到的分辨率较低", default="flv"
    )
    parse.add_argument(
        "--cookie", help="账号的cookie，注意传递时要用双引号包起来，但不建议直接作为参数在此处传递", default=""
    )
    parse.add_argument(
        "--cookiefile", help="读取文本中的cookie值，为了安全请将cookie值写入某个文件中，由程序自行读取", default=""
    )
    parse.add_argument("--outputdir", help="将视频存入指定的文件夹路径中", default=".")
    args = parse.parse_args()

    config = Config(cookie=args.cookie, cookie_file=args.cookiefile)

    main()  # execute
