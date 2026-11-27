# Tüm sayfalara NO favicon bağlantılarını ekler (idempotent).
import pathlib,re
ROOT=pathlib.Path('/home/claude/notiyatro')
TAG='<link rel="icon" href="/favicon.svg" type="image/svg+xml" id="noicon"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#000000">'
n=0
for p in ROOT.rglob('*.html'):
    if 'node_modules' in p.parts: continue
    t=p.read_text()
    if 'id="noicon"' in t or '</head>' not in t: continue
    t=re.sub(r'<link rel="(?:shortcut )?icon"[^>]*>','',t)
    t=t.replace('</head>',TAG+'</head>',1); p.write_text(t); n+=1
print('icons added:',n)
