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

import hashlib
import os
import argparse
import random
import re
import sys
import time
from datetime import datetime
from typing import List, Literal, Tuple, Union, cast

import requests
import rich
from rich.progress import (BarColumn, DownloadColumn, Progress, TextColumn,
                           TimeRemainingColumn, TransferSpeedColumn)


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


def request(
    url, headers, timeout=10, response_type: Literal["json", "text"] = "text"
) -> Union[str, dict]:
    try:
        if response_type == "text":
            res = requests.get(
                url, headers=headers, timeout=config.timeout
            ).content.decode()
        else:
            res = requests.get(url, headers=headers, timeout=config.timeout).json()
    except requests.exceptions.ConnectionError:
        print_error_info("请求页面连接失败，被拒绝或者请求超时，未联网或者使用了代理")
        sys.exit(0)
    return res


def print_error_info(info: str):
    rich.print(f"[red] error: {info}")


def parse_page(page_url: str):
    page_html_text = cast(str, request(page_url, config.parse_headers))

    avid_list = re.findall(r"aid=(\d+)", page_html_text) or re.findall(
        r"\"aid\":(\d+)", page_html_text
    )
    cid_list = re.findall(r"cid=(\d+)", page_html_text) or re.findall(
        r"\"cid\":(\d+)", page_html_text
    )
    title = re.findall(r"<h1 title=\"(.*?)\"", page_html_text) or [
        str(int(datetime.now().timestamp()))
    ]
    assert avid_list and cid_list, "[error] not found cid or avid"
    return avid_list[0], cid_list[0], title[0]


def parse_player_info_get_video_urls(info_api: str, qn: int) -> Tuple[List[str], int]:
    player_urls = []

    info_data = cast(
        dict, request(info_api, config.parse_headers, response_type="json")
    )

    try:
        quality = info_data["data"]["quality"]
        if desc := config.qn_map.get(quality):
            rich.print(f"[blue]【√】获取到的视频分辨率为: {desc}")
        durl_data = info_data["data"]["durl"][0]
        player_urls.append(durl_data["url"])
        player_urls.extend(durl_data["backup_url"])
        file_size = int(durl_data["size"])
    except Exception as e:
        print_error_info("解析失败" + str(e))
        sys.exit(0)

    return player_urls, file_size


def download_video(
    page_url: str,
    urls: List[str],
    file_size: int,
    title: str,
    _type: Literal["flv", "mp4"],
    outputdir: str = ".",
):
    
    def _do(url):
        # 视频名称和path做一个摘要，防止重复下载，即便名字相同 page_uri 也不同
        md5 = hashlib.md5()
        mixed_path_title = page_url.partition("?")[0] + title
        print(mixed_path_title)
        md5.update(mixed_path_title.encode("utf-8"))
        hash_str = md5.hexdigest()

        filename = f"{title}_{hash_str}.{_type}"
        file_path = f"{outputdir if outputdir.endswith('/') else outputdir + '/'}{filename}"
        if os.path.exists(file_path):
            rich.print(f'[yellow]视频{title},已经存在,如需覆盖请先手动删除原视频后重试')
            return
        f = open(file_path, "wb")
        try:
            stream_file = requests.get(
                url,
                headers=config.download_headers,
                stream=True,
                timeout=config.timeout,
            )
            # start_time = time.monotonic()
            # temp_size = 0
            # has_download_size = 0
            with Progress(  # 使用 rich progress 展示更好看的进度条
                TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "|",
                DownloadColumn(),
                "|",
                TransferSpeedColumn(),
                "|",
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(
                    "download",
                    filename=filename,
                    total=file_size,  # filename仅作名称展示
                )

                for chunk in stream_file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        size = chunk.__sizeof__()
                        progress.update(task, advance=size)
                        # has_download_size += size
                        # now_time = time.monotonic()

                        # if now_time - start_time > 2:
                        #     size_diff = has_download_size - temp_size
                        #     network_speed = round(
                        #         size_diff / (1024**2) / (now_time - start_time), 2
                        #     )
                        #     temp_size = has_download_size
                        #     start_time = now_time
                        # print(
                        #     f"已下载: {round(has_download_size/(1024**2),2)} MB / {file_size} MB , 速度: {network_speed} Mb/s", flush=True
                        # )
            rich.print("[green]【√】下载完成 !!!")
            rich.print(f"[green] 文件保存路径: {file_path}")
        except Exception as e:
            print_error_info(str(e))
        finally:
            f.close()
        return

    for _url in urls:
        try:
            _do(_url)
            return
        except Exception as e:
            if _url == urls[-1]:
                print_error_info(str(e))
                sys.exit(0)
            continue


def gen_player_info_api(avid, cid, qn: int, _type: Literal["flv", "mp4"]):
    """最主要的接口"""

    api_path = "https://api.bilibili.com/x/player/playurl?avid=%s&cid=%s&qn=%s&fnver=0&fnval=0&fourk=1&ep_id=&type=%s&otype=json"
    return str(api_path % (avid, cid, qn, _type))


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

    if not (args.url or args.urlfile):
        rich.print('[yellow]【warning】url 和 urlfile参数不能都为空')
        parse.print_help()
        sys.exit(0)

    urls = []
    if args.urlfile:
        with open(args.urlfile, "r") as f:
            urls += [_u.strip() for _u in f.readlines()]
    if args.url:
        urls.append(args.url)

    # 多线程同时拉取有被限速的风险，而且基本上一个4k视频最少也是几百兆 ，在本地带宽拉满的情况下 多线程的意义也不大
    for url in urls:
        avid, cid, title = parse_page(url)
        info_api = gen_player_info_api(avid, cid, qn=args.qn, _type=args.type)
        player_urls, file_size = parse_player_info_get_video_urls(info_api, args.qn)
        download_video(url, player_urls, file_size, title, args.type, args.outputdir)
