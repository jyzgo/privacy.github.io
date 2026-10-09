"""生成各款「零采集」游戏的隐私政策页（<slug>.html）。改文案改这里，重跑：python _gen.py
零采集 = 安卓壳 ads.provider=none、无 INTERNET 权限、游戏不发任何网络请求。
接了 AdMob 的放进 ADS：页面从 index.html（AdMob 披露版，Solitaire 用的那份）派生，只换应用名 / 包名 / 日期，
文案只维护 index.html 一处。接了 AdMob 以外的 SDK（统计等）要另写披露，别塞进这两类。
beatlap.html（间歇计时 App：AdMob + Play 内购）是手写的，不在 GAMES 里，本脚本不碰它。"""
import html, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = '1 October 2026'
DATE_ADS = '8 October 2026'
# 2026-10-08 起这 6 款安卓首发带 AdMob（minik.json android.ads.provider=admob）
ADS = {'catcubeaway', 'catnapsudoku', 'catwatersort', 'jaderings', 'arrowdashvane', 'puddingcatblocks'}
GAMES = [  # (文件名, 英文名, 包名)
    ('catcubeaway', 'Cat Cube Away', 'com.adevegame.catcubeaway'),
    ('catnapsudoku', 'Cat Nap Sudoku', 'com.adevegame.catnapsudoku'),
    ('catwatersort', 'Meow Latte Sort', 'com.adevegame.meowlattesort'),
    ('jaderings', 'Jade Ring Unlock', 'com.adevegame.jaderingunlock'),
    ('arrowdashvane', 'Arrow Dashvane', 'com.adevegame.arrowdashvane'),
    ('puddingcatblocks', 'Pudding Cat Blocks', 'com.adevegame.puddingcatblocks'),
    ('haunteddorm', 'Nap Till Dawn', 'com.adevegame.naptilldawn'),
]

TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Privacy Policy — {name}</title>
<style>
  :root {{ --fg:#1b1d1f; --muted:#5c6470; --bg:#ffffff; --card:#f6f7f9; --line:#e3e6ea; --accent:#1a6b3c; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --fg:#e8eaed; --muted:#9aa4b2; --bg:#15181b; --card:#1e2226; --line:#2c3238; --accent:#6fd3a8; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--fg);
         font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width: 760px; margin: 0 auto; padding: 48px 16px 80px; }}
  h1 {{ font-size: 28px; margin: 0 0 6px; }}
  h2 {{ font-size: 19px; margin: 36px 0 10px; }}
  .meta {{ color: var(--muted); font-size: 14px; margin-bottom: 32px; }}
  ul {{ padding-left: 22px; }}
  li {{ margin: 6px 0; }}
  a {{ color: var(--accent); }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; margin: 18px 0; }}
  .card p {{ margin: 0; }}
  footer {{ margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; }}
</style>
</head>
<body>
<div class="wrap">

<h1>Privacy Policy</h1>
<div class="meta">{name} &middot; Adevegames &middot; Effective {date}</div>

<p>This policy applies to the mobile game <strong>{name}</strong> (<code>{pkg}</code>),
published by <strong>Adevegames</strong>.</p>

<div class="card">
<p><strong>The short version.</strong> {name} does not collect, store on any server, or share
any personal information. It has no ads, no analytics, no accounts and no in-app purchases, and it
does not connect to the internet. Your progress stays on your device.</p>
</div>

<h2>Information we collect</h2>

<p>None. The game does not request the internet permission and sends no data to us or to any
third party. We do not collect your name, email address, phone number, location, device
identifiers, advertising ID, contacts, photos or any usage statistics.</p>

<h2>Data stored on your device</h2>

<p>Your game progress, settings and statistics are saved only in the app's local storage on your
device. They are never uploaded, and they are permanently removed when you uninstall the app or
clear its data in your device settings.</p>

<h2>Third-party services</h2>

<p>The game contains no third-party advertising, analytics or tracking SDKs. Google Play
processes information when you download or update an app; that is covered by Google's own
<a href="https://policies.google.com/privacy" target="_blank" rel="noopener">privacy policy</a>,
not by this one.</p>

<h2>Children</h2>

<p>Because the game collects no personal information from anyone, it collects none from
children.</p>

<h2>Changes to this policy</h2>

<p>If a future version of the game starts collecting any information (for example by adding ads),
we will update this page and the effective date above before that version is released.</p>

<h2>Contact</h2>

<p>Questions about this policy can be sent to
<a href="mailto:adevegame@gmail.com">adevegame@gmail.com</a>.</p>

<footer>Adevegames &middot; Last updated {date}</footer>

</div>
</body>
</html>
'''

with open(os.path.join(HERE, 'index.html'), encoding='utf-8') as f:
    ADS_SRC = f.read()


def ads_page(name, pkg):
    s = ADS_SRC
    for old, new in [
        ('<title>Privacy Policy — Adevegames</title>', f'<title>Privacy Policy — {name}</title>'),
        ('<div class="meta">Adevegames &middot; Effective 27 September 2026</div>',
         f'<div class="meta">{name} &middot; Adevegames &middot; Effective {DATE_ADS}</div>'),
        ('It applies to <strong>Solitaire Collection</strong> (<code>com.solitaire.adevegame</code>)\nand our other published apps.</p>',
         f'It applies to <strong>{name}</strong> (<code>{pkg}</code>).</p>'),
        ('Adevegames &middot; Last updated 27 September 2026', f'Adevegames &middot; Last updated {DATE_ADS}'),
    ]:
        if s.count(old) != 1:
            raise SystemExit(f'index.html 里找不到（或不唯一）: {old[:60]}… —— index.html 改过就同步改这里')
        s = s.replace(old, new)
    return s


for slug, name, pkg in GAMES:
    page = ads_page(html.escape(name), pkg) if slug in ADS else TPL.format(name=html.escape(name), pkg=pkg, date=DATE)
    with open(os.path.join(HERE, slug + '.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print('https://jyzgo.github.io/privacy.github.io/%s.html' % slug)
