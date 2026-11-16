#!/usr/bin/env python3
"""Shared header, footer and head links for the Hub's front page, papers index and wiki (S41).

  python3 tools/apply_site_shell.py            # rewrite the shell blocks in the pages
  python3 tools/apply_site_shell.py --check    # fail if a page's shell differs from this template

Each page holds three marked blocks that this script owns:
  <!-- SHELL:head -->   ... <!-- /SHELL:head -->     stylesheet and script links
  <!-- SHELL:header --> ... <!-- /SHELL:header -->   skip link, site header, breadcrumb row
  <!-- SHELL:footer --> ... <!-- /SHELL:footer -->   site footer
Edit the template here, never the blocks. The stylesheet is assets/site.css, the behaviour assets/site.js.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# page -> (root prefix, current nav key, breadcrumb [(label, href-from-page or None)], header search)
PAGES = {
    'index.html': ('', 'home', None, False),
    'papers/index.html': ('../', 'papers', [('Home', '../'), ('Papers', None)], False),
    'wiki/index.html': ('../', 'wiki', [('Home', '../'), ('Wiki', None)], True),
    'wiki/faq.html': ('../', 'wiki', [('Home', '../'), ('Wiki', 'index.html'), ('FAQ', None)], False),
    'wiki/glossary.html': ('../', 'wiki', [('Home', '../'), ('Wiki', 'index.html'), ('Glossary', None)], False),
    'wiki/implementation-roadmap.html': ('../', 'wiki', [('Home', '../'), ('Wiki', 'index.html'), ('Implementation Guide', None)], False),
    'wiki/international-adaptation-guide.html': ('../', 'wiki', [('Home', '../'), ('Wiki', 'index.html'), ('International Adaptation Guide', None)], False),
}

NAV = [('home', 'Home', ''), ('papers', 'Papers', 'papers/'), ('findings', 'Findings', '#findings'),
       ('tools', 'Tools', '#tools'), ('wiki', 'Wiki', 'wiki/'), ('help', 'Get involved', '#help')]


def head(r):
    return (f'<link rel="stylesheet" href="{r}assets/site.css">\n'
            f'    <script src="{r}assets/site.js"></script>')


def header(r, cur, crumbs, search):
    items = []
    for key, label, href in NAV:
        cur_attr = ' aria-current="page"' if key == cur and key in ('home', 'papers', 'wiki') else ''
        items.append(f'                <a href="{r}{href}"{cur_attr}>{label}</a>')
    nav = '\n'.join(items)
    s = ''
    if search:
        s = ('''
            <form class="header-search" role="search" aria-label="Search documentation" onsubmit="runSearch(event)">
                <input type="search" id="search-input" placeholder="Search documentation..." aria-label="Search documentation" autocomplete="off">
                <button type="submit" aria-label="Submit search">Search</button>
            </form>''')
    out = f'''<a class="skip-link" href="#main-content">Skip to main content</a>
<header class="site-header" role="banner">
    <div class="container">
        <div class="header-inner">
            <a class="brand" href="{r}"><img src="{r}assets/bettertobest-mark-cool-academic.svg" alt="" width="32" height="32"><span>Better To Best <em>Research Hub</em></span></a>
            <nav class="site-nav" id="site-nav" aria-label="Primary">
{nav}
            </nav>
            <div class="header-tools">
                <button type="button" class="theme-toggle" id="themeToggle" aria-label="Switch to dark theme">Dark</button>
                <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
            </div>{s}
        </div>
    </div>
</header>'''
    if crumbs:
        parts = []
        for i, (label, href) in enumerate(crumbs):
            if i:
                parts.append('<span aria-hidden="true">/</span>')
            parts.append(f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>')
        out += ('\n<div class="crumbs"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb">'
                + ' '.join(parts) + '</nav></div></div>')
    return out


def footer(r):
    return f'''<footer class="site-footer" role="contentinfo">
    <div class="container">
        <p>&copy; 2025&ndash;2026 Better To Best Research Hub. All research is open access under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>. The Simulation's code is open source under the <a href="https://github.com/BetterToBest/compassionism-simulation/blob/main/LICENSE-CODE.txt" target="_blank" rel="noopener noreferrer">Apache License 2.0</a>. Created by Duke Johnson in collaboration with Claude (Anthropic).</p>
        <p>Contact: <a href="mailto:BetterToBestResearch@gmail.com">BetterToBestResearch@gmail.com</a></p>
        <nav class="footer-links" aria-label="Footer navigation">
            <a href="{r}">Home</a>
            <a href="{r}papers/">Research Papers</a>
            <a href="{r}wiki/">Wiki</a>
            <a href="{r}wiki/glossary.html">Glossary</a>
            <a href="{r}wiki/faq.html">FAQ</a>
            <a href="{r}integrated-implementation-roadmap.html">Implementation Roadmap</a>
            <a href="{r}wiki/implementation-roadmap.html">General Roadmap</a>
            <a href="{r}wiki/international-adaptation-guide.html">International Guide</a>
            <a href="{r}corrections.html">Corrections</a>
            <a href="{r}v1/">Version 1 (archived)</a>
            <a href="https://github.com/BetterToBest/research-hub/discussions" target="_blank" rel="noopener noreferrer">Discussions</a>
            <a href="https://independentresearcher.academia.edu/DukeJohnson" target="_blank" rel="noopener noreferrer">Academia.edu</a>
        </nav>
    </div>
</footer>'''


BLOCKS = {'head': re.compile(r'(<!-- SHELL:head -->)(.*?)(<!-- /SHELL:head -->)', re.S),
          'header': re.compile(r'(<!-- SHELL:header -->)(.*?)(<!-- /SHELL:header -->)', re.S),
          'footer': re.compile(r'(<!-- SHELL:footer -->)(.*?)(<!-- /SHELL:footer -->)', re.S)}


def render(page):
    r, cur, crumbs, search = PAGES[page]
    return {'head': head(r), 'header': header(r, cur, crumbs, search), 'footer': footer(r)}


def main():
    check = '--check' in sys.argv
    bad = []
    for page in PAGES:
        path = os.path.join(ROOT, page)
        s = open(path, encoding='utf-8').read()
        want = render(page)
        out = s
        for name, rx in BLOCKS.items():
            if not rx.search(out):
                bad.append(f'{page}: missing SHELL:{name} block')
                continue
            out = rx.sub(lambda m: f'{m.group(1)}\n{want[name]}\n{m.group(3)}', out, count=1)
        if out != s:
            if check:
                bad.append(f'{page}: shell differs from tools/apply_site_shell.py')
            else:
                open(path, 'w', encoding='utf-8').write(out)
                print('updated', page)
    if bad:
        print('\n'.join(bad)); sys.exit(1)
    print('shell ok' if check else 'done')


if __name__ == '__main__':
    main()
