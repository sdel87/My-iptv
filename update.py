import requests

SOURCES = [
    ("🇬🇧 UK", "https://iptv-org.github.io/iptv/countries/uk.m3u"),
    ("🇺🇸 USA", "https://iptv-org.github.io/iptv/countries/us.m3u"),
    ("🇨🇦 Canada", "https://iptv-org.github.io/iptv/countries/ca.m3u"),
    ("🇦🇺 Australia", "https://iptv-org.github.io/iptv/countries/au.m3u"),
]

OUTPUT = "playlist.m3u"
seen = set()

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("#EXTM3U\n")

    for country, url in SOURCES:
        print(f"Downloading {country}...")

        response = requests.get(url, timeout=120)
        response.raise_for_status()

        lines = response.text.splitlines()

        i = 0

        while i < len(lines):

            if lines[i].startswith("#EXTINF:") and i + 1 < len(lines):

                info = lines[i]
                stream_url = lines[i + 1].strip()

                if stream_url.startswith("http") and stream_url not in seen:

                    seen.add(stream_url)

                    if 'group-title="' in info:
                        start = info.find('group-title="') + len('group-title="')
                        end = info.find('"', start)

                        info = (
                            info[:start]
                            + country
                            + info[end:]
                        )
                    else:
                        info = info.replace(
                            "#EXTINF:",
                            f'#EXTINF: group-title="{country}"',
                            1
                        )

                    out.write(info + "\n")
                    out.write(stream_url + "\n")

            i += 1

print(f"Done. Channels: {len(seen)}")
