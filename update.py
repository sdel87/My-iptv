import requests

SOURCES = [
    ("🇬🇧 UK", "https://iptv-org.github.io/iptv/countries/uk.m3u"),
    ("🇺🇸 USA", "https://iptv-org.github.io/iptv/countries/us.m3u"),
    ("🇨🇦 Canada", "https://iptv-org.github.io/iptv/countries/ca.m3u"),
    ("🇦🇺 Australia", "https://iptv-org.github.io/iptv/countries/au.m3u"),
]

OUTPUT = "playlist.m3u"

seen = set()
channels = []

for country, url in SOURCES:
    print(f"Downloading {country}...")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    lines = response.text.splitlines()

    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("#EXTINF:"):
            info = line

            if i + 1 < len(lines):
                stream_url = lines[i + 1].strip()

                if stream_url.startswith("http"):
                    if stream_url not in seen:
                        seen.add(stream_url)

                        info = info.replace(
                            'group-title="',
                            f'group-title="{country} / ',
                            1
                        )

                        channels.append((info, stream_url))

        i += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for info, stream_url in channels:
        f.write(info + "\n")
        f.write(stream_url + "\n")

print(f"Done. Channels: {len(channels)}")
