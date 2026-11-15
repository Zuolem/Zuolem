"""Read only GitHub's public calendar; never authenticate or read repositories."""
from datetime import date, datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-date' in attrs and 'data-level' in attrs:
            day = date.fromisoformat(attrs['data-date'])
            level = int(attrs['data-level'])
            if level not in range(5):
                raise ValueError('Unexpected contribution intensity')
            self.days[day] = level

def render(days, mobile=False):
    if len(days) < 300:
        raise ValueError('Incomplete public calendar; keeping existing SVG')
    end = max(days)
    start = end - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    colors = ['#15262B', '#245D40', '#428C46', '#7EBD52', '#B7F768']
    cells = []
    months = []
    towers = []
    for day, level in sorted(days.items()):
        if day < start or day > end:
            continue
        offset = (day-start).days
        week, weekday = offset//7, offset%7
        x, y = 32 + week*13, 43 + weekday*16
        cells.append(f'<rect x="{x}" y="{y}" width="10" height="12" rx="1" fill="{colors[level]}"><title>{day}: intensity {level}/4</title></rect>')
        if day.day == 1:
            months.append(f'<text x="{x}" y="29">{day:%b}</text>')
        # Each column maps to one actual calendar day. Height encodes its level,
        # never an invented contribution count. All days are retained.
        tx, ty = 780 + week*5.4 + weekday*11, 130 - week*.85 + weekday*5.5
        height = level*13
        top = f'{tx:.1f},{ty-height:.1f} {tx+4.8:.1f},{ty-height-.8:.1f} {tx+14.4:.1f},{ty-height+4:.1f} {tx+9.6:.1f},{ty-height+4.8:.1f}'
        face1 = f'{tx:.1f},{ty:.1f} {tx+9.6:.1f},{ty+4.8:.1f} {tx+9.6:.1f},{ty-height+4.8:.1f} {tx:.1f},{ty-height:.1f}'
        face2 = f'{tx+9.6:.1f},{ty+4.8:.1f} {tx+14.4:.1f},{ty+4:.1f} {tx+14.4:.1f},{ty-height+4:.1f} {tx+9.6:.1f},{ty-height+4.8:.1f}'
        towers.append(f'<g><title>{day}: intensity {level}/4</title><polygon points="{face1}" fill="{colors[level]}" fill-opacity=".7"/><polygon points="{face2}" fill="{colors[level]}" fill-opacity=".45"/><polygon points="{top}" fill="{colors[level]}" stroke="#3F8C70" stroke-width=".4"/></g>')
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')
    legend = ''.join(f'<rect x="{608+i*16}" y="171" width="11" height="11" rx="1" fill="{c}"/>' for i,c in enumerate(colors))
    calendar = f'<g font-family="monospace" font-size="11" fill="#9FBAB7">{"".join(months)}<text x="0" y="72">M</text><text x="0" y="104">W</text><text x="0" y="136">F</text></g>{"".join(cells)}{legend}'
    landscape = ''.join(towers)
    w,h = (740,440) if mobile else (1200,220)
    if mobile:
        landscape = f'<g transform="translate(-1075 123) scale(1.5)">{landscape}</g>'
    else:
        landscape += '<text x="805" y="182" font-size="11" fill="#9FBAB7" font-family="monospace">DAILY INTENSITY / ISOMETRIC VIEW</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">ZUOLEM public contribution signal</title><desc id="desc">Public GitHub calendar, {start} through {end}. Updated {stamp}. Both plots show the same daily intensity from zero to four, not exact contribution counts. No private repository details.</desc><rect width="{w}" height="{h}" fill="#0D1117"/>{calendar}{landscape}<text x="32" y="{h-13}" fill="#9FBAB7" font-family="monospace" font-size="11">PUBLIC PROFILE / SNAPSHOT {stamp} / INTENSITY 0–4</text></svg>'''

if __name__ == '__main__':
    request = Request('https://github.com/users/Zuolem/contributions', headers={'User-Agent': 'ZUOLEM-profile-artwork', 'Accept': 'text/html'})
    with urlopen(request, timeout=30) as response:
        document = response.read().decode('utf-8')
    calendar = Calendar()
    calendar.feed(document)
    output = render(calendar.days)
    mobile_output = render(calendar.days, mobile=True)
    Path('assets/activity.svg').write_text(output, encoding='utf-8')
    Path('assets/activity-mobile.svg').write_text(mobile_output, encoding='utf-8')
    print(f'Updated activity from {len(calendar.days)} public calendar days.')
