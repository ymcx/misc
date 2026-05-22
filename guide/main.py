from datetime import datetime, timedelta
import sys
import gzip
from urllib.request import Request
from urllib import request
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


URL = "https://epgshare01.online/epgshare01/epg_ripper_FI1.xml.gz"


def format_channel(channel: str, channels: list[str]) -> tuple[str, int]:
    channel = channel[: channel.rfind(".")]
    n = max(len(channel) for channel in channels)

    return channel, n


def format_time(time: str) -> str:
    time: datetime = datetime.strptime(time, "%Y%m%d%H%M%S %z").astimezone()
    time: str = time.strftime("%H:%M")

    return time


# TODO: display the current programme as well
def is_time_today(time: str) -> bool:
    time: datetime = datetime.strptime(time, "%Y%m%d%H%M%S %z")
    time_now = datetime.now()
    time_this_midnight = time_now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_next_midnight = time_this_midnight + timedelta(days=1)

    return time_now.timestamp() < time.timestamp() < time_next_midnight.timestamp()


def get_title(node: Element[str]) -> str | None:
    for child in node:
        tag = child.tag
        if tag != "title":
            continue

        return child.text


def get_programme(node: Element[str], channels: list[str]) -> str | None:
    tag = node.tag
    if tag != "programme":
        return None

    channel = node.get("channel")
    if not channel:
        return None
    channel_fmt, n = format_channel(channel, channels)
    if channel_fmt not in channels:
        return None

    time = node.get("start")
    if not time or not is_time_today(time):
        return None
    time_fmt = format_time(time)

    title = get_title(node)
    if not title:
        return None
    title_fmt = title

    return f"{channel_fmt:>{n}} {time_fmt} {title_fmt}"


def get_programmes(channels: list[str]) -> str:
    request_url = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    response = request.urlopen(request_url).read()
    data = gzip.decompress(response).decode()
    nodes = ElementTree.fromstring(data)
    programmes = [get_programme(node, channels) for node in nodes]
    output = "\n".join(programme for programme in programmes if programme)

    return output


def main() -> None:
    channels = sys.argv[1:]
    programmes = get_programmes(channels)
    print(programmes)


if __name__ == "__main__":
    main()
