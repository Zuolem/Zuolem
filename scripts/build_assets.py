"""Original vector profile artwork. Standard library; run from repository root."""
from pathlib import Path
from html import escape
import math
import random

OUT = Path('assets')
OUT.mkdir(exist_ok=True)
LIME, CYAN = '#B7F768', '#45D6C5'

def svg(name, w, h, title, body):
    style = '''<style>text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,'Liberation Mono',monospace}.pulse{animation:pulse 6s ease-in-out infinite}@keyframes pulse{50%{opacity:.4}}@media(prefers-reduced-motion:reduce){.pulse{animation:none}}</style>'''
    defs = '''<defs><linearGradient id="panel" x2=".8" y2="1"><stop stop-color="#101E24"/><stop offset="1" stop-color="#0D1117"/></linearGradient><linearGradient id="neon" x2=".3" y2="1"><stop stop-color="#45D6C5"/><stop offset="1" stop-color="#B7F768"/></linearGradient><radialGradient id="aura"><stop stop-color="#127C70" stop-opacity=".35"/><stop offset="1" stop-color="#0D1117" stop-opacity="0"/></radialGradient></defs>'''
    output=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Original ZUOLEM engineering artwork. Project charts are decorative, not measured results.</desc>{style}{defs}<rect width="{w}" height="{h}" fill="#0D1117"/>{body}</svg>'
    (OUT/name).write_text(output,encoding='utf-8')

def txt(x,y,text,size=18,color='#D1DEDF',mono=False,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" class="{"mono" if mono else "label"}" {extra}>{escape(text)}</text>'

def panel(w,h):
    return f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="11" fill="url(#panel)" stroke="#31505A"/>'

def terrain():
    rng=random.Random(47)
    points=[]
    for row in range(13):
        line=[]
        depth=row/12
        for col in range(37):
            x=430+col*21
            ridge=140*math.exp(-((x-875)/100)**2)+62*math.exp(-((x-655)/75)**2)
            y=222-95*depth-ridge*math.sin(depth*math.pi*.67)
            x+=(rng.random()-.5)*13 if col not in (0,36) else 0
            y+=(rng.random()-.5)*15*depth
            line.append((x,y))
        points.append(line)
    mesh=''
    for row in range(12):
        for col in range(36):
            a,b,c,d=points[row][col],points[row][col+1],points[row+1][col],points[row+1][col+1]
            for tri in ((a,b,c),(b,c,d)):
                coords=' '.join(f'{x:.1f},{y:.1f}' for x,y in tri)
                mesh+=f'<polygon points="{coords}" fill="#092B30" fill-opacity=".14" stroke="#45D6C5" stroke-opacity="{.13+.4*row/12:.2f}" stroke-width=".65"/>'
    return mesh

hero_bg='<ellipse cx="860" cy="137" rx="400" ry="150" fill="url(#aura)"/>'
hero_bg+=''.join(f'<path d="M{450+i*45} 15L{250+i*70} 238" stroke="#173B46" stroke-opacity=".28"/>' for i in range(18))
hero_bg+=terrain()
hero_art='''<g fill="none" stroke="#45D6C5" stroke-width="1.4"><path d="M565 63h36m-29-9 20 18m0-18-20 18"/><ellipse cx="561" cy="58" rx="11" ry="3"/><ellipse cx="605" cy="58" rx="11" ry="3"/><path d="M583 67v8m-6 0h12"/><path d="M1104 200V78m0 0-42 17m42-17 5-66m-5 66 39 29"/><circle cx="1104" cy="78" r="4"/><rect x="967" y="153" width="29" height="54" rx="4"/><rect x="1003" y="160" width="29" height="47" rx="4"/><path d="M981 153v-13h36v20m-9-20v-12h7v12m-36 25v29m37-22v25M940 210h112"/></g><g stroke="#B7F768" fill="none"><path d="M655 210h203l8-5h110m-141-92h100m-10-3v6" opacity=".55"/><path d="M1034 209h125"/><circle class="pulse" cx="866" cy="205" r="3" fill="#B7F768"/></g>'''
hero_type=txt(27,86,'ZUOLEM//',70,'url(#neon)',True,'font-weight="bold" letter-spacing="2"')+txt(29,125,'ENGINEERING × DATA × R&D',22,LIME,True,'letter-spacing="2"')+txt(30,181,'Build. Measure. Analyse. Iterate.',16,'#A6BFBB',True)
hero_type+='<path d="M14 43V25h18m360 0h18v18M14 137v18h18m360 0h18v-18" fill="none" stroke="#B7F768"/>'
svg('hero.svg',1200,245,'ZUOLEM // Engineering × Data × R&D',hero_bg+hero_art+hero_type)
svg('hero-mobile.svg',600,265,'ZUOLEM // Engineering × Data × R&D',f'<g transform="translate(-190 105) scale(.66)" opacity=".45">{hero_bg}{hero_art}</g>'+txt(22,77,'ZUOLEM//',66,'url(#neon)',True,'font-weight="bold"')+txt(24,115,'ENGINEERING × DATA × R&D',21,LIME,True)+txt(24,157,'Build. Measure. Analyse. Iterate.',17,'#B1C6C1',True))

def whoami(mobile=False):
    w,h=(600,250) if mobile else (1200,178)
    body=panel(w,h)+f'<path d="M1 32H{w-1}" stroke="#29414A"/>'
    for x,c in [(21,'#FF605C'),(39,'#FFBD44'),(57,'#00CA4E')]:
        body+=f'<circle cx="{x}" cy="17" r="5" fill="{c}"/>'
    body+=txt(w-195,22,'ZUOLEM / LAB NOTES',12,'#A1BCB6',True)
    lines=['Scientific computing · Engineering R&D','Data analytics · Computer vision','Embedded systems & IoT','Signal processing · Automation'] if mobile else ['Scientific computing · Engineering R&D · Data analytics','Computer vision · Embedded systems & IoT · Signal processing · Automation']
    body+=txt(25,65,'BUILD / MEASURE / UNDERSTAND',14,CYAN,True,'letter-spacing="1.5"')
    for i,line in enumerate(lines):
        body+=txt(25,96+i*28,line,18 if mobile else 21,'#DFE9E7')
    return body+txt(25,h-19,'> Build. Measure. Analyse. Iterate.',17,LIME,True)
svg('whoami.svg',1200,178,'ZUOLEM technical interests — lab notes',whoami())
svg('whoami-mobile.svg',600,250,'ZUOLEM technical interests — lab notes',whoami(True))

# Original tool marks. Only technologies already confirmed in the brief.
icons=[
('Python','<path d="M12 3h15q8 0 8 8v9H18v5H8q-7 0-7-8t7-8h12V6h-8z" fill="#3897CB"/><path d="M31 40H16q-8 0-8-8v-9h17v-5h10q7 0 7 8t-7 8H23v3h8z" fill="#FFD447"/><circle cx="26" cy="8" r="2" fill="#0D1117"/><circle cx="17" cy="34" r="2" fill="#0D1117"/>'),
('JavaScript','<rect x="2" y="2" width="38" height="38" rx="3" fill="#F1D847"/>'+txt(9,32,'JS',23,'#111820',True,'font-weight="bold"')),
('SQL','<ellipse cx="21" cy="8" rx="17" ry="6" fill="#286D91" stroke="#46BCE6"/><path d="M4 8v25c0 9 34 9 34 0V8M4 20c0 9 34 9 34 0" fill="none" stroke="#46BCE6" stroke-width="2"/>'+txt(8,31,'SQL',12,'#DDF7FF',True)),
('Raspberry Pi','<path d="M20 10Q5-2 6 4q2 8 14 6M22 10Q37-2 36 4q-2 8-14 6" fill="#7CC85A"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#E93772" stroke="#0D1117"/>' for x,y in [(14,16),(27,16),(10,26),(21,26),(32,26),(16,36),(27,36)])),
('Arduino','<path d="M21 22C2-4-9 45 12 30l19-16c21-16 31 32 10 17L21 14" transform="translate(0 2) scale(.82)" fill="none" stroke="#45D6C5" stroke-width="4"/><path d="M5 21h7m19 0h7m-3-3v6" stroke="#45D6C5" stroke-width="2"/>'),
('Linux','<ellipse cx="22" cy="26" rx="13" ry="17" fill="#121A22" stroke="#96A8AC"/><ellipse cx="22" cy="29" rx="9" ry="12" fill="#E7EDEF"/><circle cx="18" cy="12" r="4" fill="#E7EDEF"/><circle cx="26" cy="12" r="4" fill="#E7EDEF"/><path d="m15 18 7-4 7 4-7 5zM7 37l12 4-16 1zm20 4 12-4 4 5z" fill="#FFD447"/>'),
('Git','<rect x="7" y="7" width="29" height="29" rx="4" transform="rotate(45 21.5 21.5)" fill="#F47A52"/><path d="M13 10l17 17m-9-9v17" stroke="#0D1117" stroke-width="3"/><g fill="#0D1117"><circle cx="13" cy="10" r="3"/><circle cx="30" cy="27" r="3"/><circle cx="21" cy="35" r="3"/></g>'),
('Sci. computing','<path d="M35 6H10l14 15L10 37h25" fill="none" stroke="#B7F768" stroke-width="4"/><circle cx="37" cy="20" r="3" fill="#45D6C5"/>')]

def toolbox(mobile=False):
    body=''
    for i,(label,mark) in enumerate(icons):
        x=(i%4)*(145 if mobile else 160)+30
        y=(i//4)*92+17
        body+=f'<g transform="translate({x+30} {y})">{mark}</g>'+txt(x+51,y+63,label,14,'#BACDCA',False,'text-anchor="middle"')
    px,py,pw,ph=(0,218,600,174) if mobile else (718,3,482,202)
    body+=f'<g transform="translate({px} {py})">'+panel(pw,ph)+f'<path d="M1 34H{pw-1}" stroke="#29414A"/>'+txt(20,24,'> RESEARCH FOCUS',15,LIME,True)
    for i,line in enumerate(['Scientific instrumentation','Engineering research & data visualisation','Embedded hardware & automation','Computer vision & image processing']):
        body+=txt(20,62+29*i,'> '+line,17,LIME if i%2==0 else '#C1D9D2',True)
    return body+'</g>'
svg('toolbox.svg',1200,225,'Toolbox and technical domains',toolbox())
svg('toolbox-mobile.svg',600,395,'Toolbox and technical domains',toolbox(True))

projects=[
('zuostation','ZuoStation',['ESP32-based weather station for','environmental monitoring.'],['ESP32','IoT','Sensors'],'<path d="M9 37h30q16-2 12-17-4-12-16-10Q26-4 15 9 0 8 2 22q-10 11 7 15zM15 42v8m13-8v8m12-8v8"/>'),
('m-spect','m-spect',['Micro-spectrometer programs for','spectral acquisition and analysis.'],['Spectroscopy','Data analysis'],'<path d="M18 3h18m-14 0v17L6 47q-2 4 3 4h34q5 0 3-5L31 20V3M14 36h24"/>'),
('electrolyser-hmi','Electrolyser-HMI',['Control and monitoring interface','for an electrolyser system.'],['HMI','Control','Monitoring'],'<path d="M2 14 26 2l24 12-24 12zM2 28l24 12 24-12M2 40l24 12 24-12"/>'),
('b9-solar','B9-Solar',['Solar-related software tools.',''],['Solar','Energy','Software'],'<path d="M8 8h40L38 40H0zM5 18h40M3 29h39M21 8 12 40M35 8 26 40M20 40v9m-12 0h24"/>')]

def chart(kind):
    if kind==0:
        rng=random.Random(9)
        ys=[76]
        for i in range(29):
            ys.append(max(15,min(78,ys[-1]+rng.randint(-14,12))))
        pts=' '.join(f'{i*5},{y}' for i,y in enumerate(ys))
        return f'<path d="M0 83H145" stroke="#284D43"/><polygon points="0,83 {pts} 145,83" fill="#B7F768" fill-opacity=".12"/><polyline points="{pts}" fill="none" stroke="#B7F768" stroke-width="1.5"/>'
    if kind==1:
        pts=' '.join(f'{x},{80-64*math.exp(-((x-43)/6)**2)-28*math.exp(-((x-83)/5)**2)-22*math.exp(-((x-118)/5)**2):.2f}' for x in range(145))
        return f'<polyline points="{pts}" fill="none" stroke="#B7F768" stroke-width="1.5"/>'
    if kind==2:
        return '<path d="M0 80H30l8-13h25l8-15h26l8-18h40" fill="none" stroke="#B7F768" stroke-width="1.7"/>'
    return ''.join(f'<rect x="{i*14}" y="{85-h}" width="10" height="{h}" fill="url(#neon)" opacity="{.4+i*.06}"/>' for i,h in enumerate([13,28,22,48,37,67,43,57,76,51]))

def card(i):
    name,title,lines,tags,icon=projects[i]
    body=panel(590,158)+f'<g transform="translate(20 24)" fill="none" stroke="#B7F768" stroke-width="2">{icon}</g>'
    body+=txt(86,32,title,23,CYAN,False,'font-weight="bold"')
    badge_x=86+len(title)*13+12
    body+=f'<rect x="{badge_x}" y="14" width="66" height="23" rx="11" fill="#0B151B" stroke="#49656C"/>'+txt(badge_x+33,30,'Private',13,'#B5C9CC',False,'text-anchor="middle"')
    for j,line in enumerate(lines):
        body+=txt(86,62+j*23,line,17,'#D1DEDF')
    x=86
    for tag in tags:
        tw=20+len(tag)*8
        body+=f'<rect x="{x}" y="116" width="{tw}" height="24" rx="12" fill="#10252D" stroke="#32616C"/>'+txt(x+tw/2,133,tag,13,'#D1E7E6',False,'text-anchor="middle"')
        x+=tw+9
    return body+f'<g transform="translate(426 43)">{chart(i)}</g>'

desktop=mobile=''
for i,(name,title,*_) in enumerate(projects):
    body=card(i)
    svg(name+'.svg',590,158,title+' — private project',body)
    desktop+=f'<g transform="translate({(i%2)*610} {(i//2)*174})">{body}</g>'
    mobile+=f'<g transform="translate(5 {i*174})">{body}</g>'
svg('projects.svg',1200,332,'Four private engineering projects',desktop)
svg('projects-mobile.svg',600,680,'Four private engineering projects',mobile)
print('Built panoramic hero, lab notes, toolbox, and compact project cards with mobile compositions.')
