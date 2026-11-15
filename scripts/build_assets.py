"""Build original, dependency-free profile artwork. Run from repository root."""
from pathlib import Path
from html import escape
import math

OUT = Path('assets')
OUT.mkdir(exist_ok=True)

def svg(name, width, height, title, body, animated=False):
    style = '''<style>text{font-family:monospace}.pulse{animation:pulse 5s ease-in-out infinite}@keyframes pulse{50%{opacity:.45}}@media(prefers-reduced-motion:reduce){.pulse{animation:none}}</style>'''
    text = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Original ZUOLEM engineering laboratory illustration.</desc>{style}<rect width="{width}" height="{height}" rx="16" fill="#0D1117"/>{body}</svg>'''
    (OUT / name).write_text(text, encoding='utf-8')

grid = ''.join(f'<path d="M{x} 0V400"/>' for x in range(0,1200,40)) + ''.join(f'<path d="M0 {y}H1200"/>' for y in range(0,400,40))
mountains = ''
for row in range(8):
    pts=[]
    for x in range(540,1201,22):
        peak=100*math.exp(-((x-800)/90)**2)+75*math.exp(-((x-1030)/75)**2)
        y=355-row*12-peak*(row/7)
        pts.append(f'{x},{y:.1f}')
    mountains += f'<polyline points="{" ".join(pts)}"/>'
for x in range(540,1201,22):
    peak=100*math.exp(-((x-800)/90)**2)+75*math.exp(-((x-1030)/75)**2)
    mountains += f'<path d="M{x} 355L{x} {271-peak:.1f}"/>'
signal=' '.join(f'{x},{190+18*math.sin(x/13)*math.exp(-((x-1000)/150)**2):.1f}' for x in range(730,1150,3))
svg('hero.svg',1200,400,'ZUOLEM // Engineering × Data × R&D', f'''
<g stroke="#173B46" opacity=".32">{grid}</g>
<path d="M32 55V30H150M1050 370H1168V345" fill="none" stroke="#B7F768"/>
<text x="55" y="79" fill="#45D6C5" font-size="14" letter-spacing="4">INDEPENDENT ENGINEERING LAB</text>
<text x="48" y="192" fill="#B7F768" font-size="105" font-weight="900" letter-spacing="-7">ZUOLEM//</text>
<text x="55" y="236" fill="#E6EDF3" font-size="23" letter-spacing="3">ENGINEERING × DATA × R&amp;D</text>
<text x="55" y="299" fill="#8BADA9" font-size="16">Build. Measure. Analyse. Iterate.</text>
<g stroke="#45D6C5" fill="none" opacity=".5">{mountains}</g>
<polyline class="pulse" points="{signal}" fill="none" stroke="#B7F768" stroke-width="2"/>
<g fill="none" stroke="#45D6C5" stroke-width="2"><circle cx="976" cy="90" r="8"/><path d="M954 68L998 112M998 68L954 112"/><ellipse cx="952" cy="66" rx="14" ry="5"/><ellipse cx="1000" cy="66" rx="14" ry="5"/><ellipse cx="952" cy="114" rx="14" ry="5"/><ellipse cx="1000" cy="114" rx="14" ry="5"/><path d="M1110 130V65M1110 65L1080 85M1110 65L1114 30M1110 65L1136 85M850 100h34v34h-34zM859 90v10m15-10v10m-15 34v10m15-10v10"/></g>
<text x="55" y="364" fill="#60857E" font-size="12" letter-spacing="2">FIELD NOTES / INSTRUMENTS / EXPERIMENTS</text>''')

illustrations = [
('zuostation','ZuoStation','ENVIRONMENTAL MONITORING','ESP32 / WEATHER STATION', '<path d="M300 140V38m-34 33h68m-34-33l-25 21m25-21l25 21M270 140h60M285 100h30v24h-30z"/><path d="M190 65q16-30 32 0t32 0M365 105q12-22 24 0t24 0"/>'),
('m-spect','m-spect','SPECTRAL ACQUISITION & ANALYSIS','MICRO-SPECTROMETER PROGRAMS','<path d="M185 100h65l35-42 30 70-65-28m65 28 85-48M315 114l85-49M312 101l88-51"/><path d="M190 150h220M200 145l25-5 20-30 20 33 30-68 20 65 20-18 20 22 35-9"/>'),
('electrolyser-hmi','Electrolyser-HMI','CONTROL & MONITORING','ELECTROLYSER INTERFACE','<rect x="190" y="45" width="200" height="105" rx="8"/><path d="M205 125h70m-70-15 15-10 12 5 15-30 14 10 13-5M290 65v65m20-65v65m20-65v65M350 75h20m-20 20h20m-20 20h20"/><circle cx="300" cy="165" r="5"/>'),
('b9-solar','B9-Solar','SOLAR SOFTWARE TOOLS','RENEWABLE ENERGY','<circle cx="365" cy="55" r="23"/><path d="M365 20v-8m0 86v-8m35-35h10m-90 0h10m60-25 7-7m-64 64 7-7M200 90h110l25 70H175zM192 113h126m-135 24h144M235 90l-10 70m45-70 10 70M255 160v18m-35 0h70"/>')]
for i,(name,title,desc,tag,art) in enumerate(illustrations,1):
    svg(name+'.svg',560,290,title+' — private project',f'''<rect x="1" y="1" width="558" height="288" rx="15" fill="none" stroke="#173B46"/><text x="24" y="31" fill="#45D6C5" font-size="11" letter-spacing="2">EXPERIMENT / 0{i}</text><text x="454" y="31" fill="#8BADA9" font-size="11">PRIVATE</text><g fill="none" stroke="#45D6C5" stroke-width="1.7">{art}</g><text x="24" y="211" fill="#B7F768" font-size="28" font-weight="bold">{title}</text><text x="24" y="242" fill="#D1DEDF" font-size="13">{escape(desc)}</text><text x="24" y="270" fill="#71918E" font-size="11" letter-spacing="1">{tag}</text>''')

tools=[('PY','Python'),('DB','SQL'),('JS','JavaScript'),('π','Raspberry Pi'),('∞','Arduino'),('$_','Linux'),('⎇','Git'),('∑','Scientific computing')]
for i,(icon,label) in enumerate(tools):
    svg('tool-'+str(i)+'.svg',250,64,label,f'<rect x="1" y="1" width="248" height="62" rx="12" fill="none" stroke="#173B46"/><text x="18" y="41" font-size="23" fill="#B7F768">{escape(icon)}</text><text x="63" y="38" font-size="15" fill="#D1DEDF">{label}</text>')
print('Built hero, four project illustrations, and eight tool badges.')
