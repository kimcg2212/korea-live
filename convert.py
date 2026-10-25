import json
import urllib.request
from pathlib import Path

SOURCE_URL = "http://141.164.53.195/live/korea-live.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "korea-live.m3u"


def clean(value):
    return str(value or "").replace('"', "'").replace("\r", " ").replace("\n", " ").strip()


def main():
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; M3U-Converter/1.0)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        channels = json.load(response)

    lines = ["#EXTM3U"]
    for channel in channels:
        title = clean(channel.get("title") or channel.get("name") or "Unnamed")
        name = clean(channel.get("name") or title)
        group = clean(channel.get("group"))
        logo = clean(channel.get("logo"))
        headers = channel.get("headers") or {}

        for uri in channel.get("uris") or []:
            uri = str(uri).strip()
            if not uri:
                continue
            lines.append(
                f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" '
                f'group-title="{group}",{title}'
            )
            if headers.get("user-agent"):
                lines.append(f'#EXTVLCOPT:http-user-agent={str(headers["user-agent"]).strip()}')
            if headers.get("cookie"):
                lines.append(f'#EXTVLCOPT:http-cookie={str(headers["cookie"]).strip()}')
            lines.append(uri)

    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_FILE.name}: {len(channels)} channels")


if __name__ == "__main__":
    main()
