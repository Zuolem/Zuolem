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

def render(days):
    if len(days) < 300:
        raise ValueError('Incomplete public calendar; keeping existing SVG')
    end = max(days)
    start = end - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    colors = ['#17302E', '#285842', '#478447', '#7EBD52', '#B7F768']
    cells = []
    months = []
    for day, level in sorted(days.items()):
        if day < start or day > end:
            continue
        offset = (day-start).days
        x, y = 42 + (offset//7)*19, 78 + (offset%7)*19
        cells.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{colors[level]}"><title>{day}: intensity {level}/4</title></rect>')
        if day.day == 1:
            months.append(f'<text x="{x}" y="64">{day:%b}</text>')
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')
    legend = ''.join(f'<rect x="{888+i*20}" y="241" width="14" height="14" rx="3" fill="{c}"/>' for i,c in enumerate(colors))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 280" role="img" aria-labelledby="title desc"><title id="title">ZUOLEM public contribution signal</title><desc id="desc">Public GitHub calendar, {start} through {end}. Updated {stamp}. Intensity from zero to four; no private repository details.</desc><rect width="1100" height="280" rx="16" fill="#0D1117"/><rect x="1" y="1" width="1098" height="278" rx="15" fill="none" stroke="#173B46"/><g font-family="monospace" font-size="12" fill="#8BADA9"><text x="42" y="33" fill="#B7F768" font-size="16">ZUOLEM / CONTRIBUTION SIGNAL</text>{''.join(months)}<text x="42" y="253">PUBLIC PROFILE / SNAPSHOT {stamp}</text><text x="838" y="253">LESS</text><text x="996" y="253">MORE</text></g>{''.join(cells)}{legend}</svg>'''

if __name__ == '__main__':
    request = Request('https://github.com/users/Zuolem/contributions', headers={'User-Agent': 'ZUOLEM-profile-artwork', 'Accept': 'text/html'})
    with urlopen(request, timeout=30) as response:
        document = response.read().decode('utf-8')
    calendar = Calendar()
    calendar.feed(document)
    output = render(calendar.days)
    Path('assets/activity.svg').write_text(output, encoding='utf-8')
    print(f'Updated activity from {len(calendar.days)} public calendar days.')
