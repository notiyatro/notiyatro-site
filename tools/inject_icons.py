# Tüm sayfalara NO favicon bağlantılarını ekler (idempotent).
import pathlib,re
ROOT=pathlib.Path('/home/claude/notiyatro')
TAG='<link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml" id="noicon"><link rel="icon" href="/favicon.ico?v=2" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2"><meta name="theme-color" content="#000000">'
n=0
for p in ROOT.rglob('*.html'):
    if 'node_modules' in p.parts: continue
    t=p.read_text()
    if 'id="noicon"' in t or '</head>' not in t: continue
    t=re.sub(r'<link rel="(?:shortcut )?icon"[^>]*>','',t)
    t=t.replace('</head>',TAG+'</head>',1); p.write_text(t); n+=1
print('icons added:',n)
