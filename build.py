import io, re, html, os

src = 'C:/Users/SSAFY/Desktop/gachijoopging/docs/legal/'
out_dir = os.path.dirname(os.path.abspath(__file__))


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    return t


def md2html(md):
    out = []
    inlist = False
    rows = []

    def flush():
        nonlocal inlist, rows
        if inlist:
            out.append('</ul>')
            inlist = False
        if rows:
            out.append('<table>' + ''.join(rows) + '</table>')
            rows = []

    for line in md.split('\n'):
        l = line.rstrip()
        if l.startswith('|'):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if all(re.fullmatch(r'-+', c) for c in cells):
                continue
            tag = 'td' if rows else 'th'
            rows.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>')
            continue
        if rows:
            flush()
        if l.startswith('- '):
            if not inlist:
                out.append('<ul>')
                inlist = True
            out.append(f'<li>{inline(l[2:])}</li>')
            continue
        if inlist and l.startswith('   - '):
            out.append(f'<li style="margin-left:1.2em">{inline(l[5:])}</li>')
            continue
        if inlist:
            flush()
        m = re.match(r'(#+) (.*)', l)
        if m:
            out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>')
            continue
        m = re.match(r'(\d+)\. (.*)', l)
        if m:
            out.append(f'<p class="n">{m[1]}. {inline(m[2])}</p>')
            continue
        if l:
            out.append(f'<p>{inline(l)}</p>')
    flush()
    return '\n'.join(out)


STYLE = ('body{font-family:system-ui,sans-serif;max-width:720px;margin:0 auto;padding:24px 16px;line-height:1.7;color:#222}'
         'h1{font-size:1.5em}h2{font-size:1.15em;margin-top:2em}table{border-collapse:collapse;width:100%;font-size:.95em}'
         'th,td{border:1px solid #ccc;padding:6px 8px;text-align:left;vertical-align:top}code{background:#f3f3f3;padding:0 4px}p.n{margin:.3em 0 .3em 1em}')

for name in ['terms', 'privacy', 'marketing']:
    md = io.open(src + name + '.md', encoding='utf-8').read()
    title = re.match(r'# (.*)', md)[1]
    page = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{STYLE}</style></head><body>\n{md2html(md)}\n</body></html>')
    io.open(os.path.join(out_dir, name + '.html'), 'w', encoding='utf-8', newline='\n').write(page)

io.open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8', newline='\n').write(
    '<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>가치줍깅 약관</title></head><body><ul>'
    '<li><a href="terms">이용약관</a></li><li><a href="privacy">개인정보처리방침</a></li><li><a href="marketing">마케팅 정보 수신 동의</a></li></ul></body></html>')
