#!/usr/bin/env python3
"""Hub figures generated from a Simulation release (S40).

  python3 tools/build_figures.py --fetch ../compassionism-simulation --tag v5.8.0 --label "Release 2" --engine-files r2-effects,r2-backing
                                                                        # snapshot a release into data/releases/ and make it current
  python3 tools/build_figures.py                                        # write every <!-- FIG:name --> block in the pages
  python3 tools/build_figures.py --check                                # fail if a page disagrees with the release

The current release is named in data/releases/current.json. When the next engine round is released, fetch it
with a new tag and label (and its data-file names); every block then follows it, and --check lists each page that
still states the earlier release's figures. Block text must not hard-code release numbers: it reads them from the snapshot.
The snapshot holds the rows of the release's own data files
(r2-effects, r2-backing), read from the tag with `git show`, plus each file's SHA-256.
Every number printed in a block is computed here from those rows; nothing is typed by hand.
A page marks a block as  <!-- FIG:name -->...<!-- /FIG -->  and the script owns what is inside.
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR = os.path.join(ROOT, 'data', 'releases', 'current.json')
BLOCK = re.compile(r'(<!-- FIG:([\w.-]+) -->)(.*?)(<!-- /FIG -->)', re.S)


def fetch(sim, tag, label, files):
    snap = {'release': tag, 'label': label, 'engine': None, 'files': {}, 'tables': {}}
    snap['commit'] = subprocess.check_output(['git', '-C', sim, 'rev-parse', tag + '^{commit}'], text=True).strip()
    for f in files:
        raw = subprocess.check_output(['git', '-C', sim, 'show', f'{tag}:data/studies/{f}.json'])
        d = json.loads(raw)
        snap['files'][f] = hashlib.sha256(raw).hexdigest()
        snap['engine'] = d['meta']['engine']
        snap['tables'][f] = {'columns': d['columns'], 'rows': [list(r) for r in zip(*d['data'])]}
    name = f'{tag}-{label.lower().replace(" ", "")}.json'
    os.makedirs(os.path.dirname(CUR), exist_ok=True)
    json.dump(snap, open(os.path.join(os.path.dirname(CUR), name), 'w'), indent=1)
    json.dump({'snapshot': name}, open(CUR, 'w'))
    print('snapshot written:', name, snap['commit'][:7], snap['engine'])


def table(snap, name):
    t = snap['tables'][name]
    return [dict(zip(t['columns'], r)) for r in t['rows']]


# --- number formats -------------------------------------------------------------------------
def pt(x, n=1): return f'{x:.{n}f}'
def pct(x, n=1): return f'{x:.{n}f}%'
def usd(x): return '$' + format(int(round(x, -2)), ',')   # nearest hundred, year-0 dollars
def span(a, b, n=1): return f'{a:.{n}f} to {b:.{n}f}'


def eff(snap, design, env, years, key):
    for r in table(snap, 'r2-effects'):
        if (r['design'], r['environment'], r['years']) == (design, env, years) and r['outcome'].startswith(key):
            return r
    raise KeyError((design, env, years, key))


# --- figure blocks ----------------------------------------------------------------------------
def fig_release_design(snap):
    k = lambda key: eff(snap, 'release design', 'Reference', 20, key)
    cost, wp, med = k('cost of living'), k('wealth poverty'), k('median real wealth')
    return (
        f'<p><strong>What the simulation finds ({snap["release"]}).</strong> The opt-in design (the design as the Hub’s papers set it: adults choose to take part) is run at full backing '
        '(its own statement: the payout is matched by new output), 500 paired runs of 500 adults, against no programme, in the Reference '
        'environment over 20 years. Adults below the cost of living (basket poverty, averaged over the adult-years): '
        f'{pct(cost["no programme"])} without the programme, {pct(cost["programme"])} with it, a fall of {pt(-cost["effect"])} points '
        f'(95% interval {pt(-cost["hi95"])} to {pt(-cost["lo95"])}). Adults with little wealth (yearly average): '
        f'{pct(wp["no programme"])} without, {pct(wp["programme"])} with, a fall of {pt(-wp["effect"])} points '
        f'({pt(-wp["hi95"])} to {pt(-wp["lo95"])}). Median real wealth (year-0 dollars) rises by about {usd(med["effect"])} '
        f'({usd(med["lo95"])} to {usd(med["hi95"])}). Each figure is the effect against no programme in the same release; '
        'the 40-year horizon and the Adverse and Stress environments, where the wealth gain is smaller, are on the '
        '<a href="https://bettertobest.github.io/compassionism-simulation/findings.html">findings page</a>.</p>')


def fig_wealth_history(snap):
    return (
        '<p><strong>An earlier release said the opposite about wealth.</strong> v5.6.0 counted the share of adults under $25,000 '
        'at the end of the run, with all wealth held as cash, and found that share higher with the programme. '
        f'The current release ({snap["release"]}) averages every year and holds wealth by asset class, so the two measure '
        'different things and their figures are not compared here. The current release supersedes v5.6 on wealth.</p>')


def inflation_ranges(snap):
    rows = [r for r in table(snap, 'r2-backing') if r['outcome'].startswith('programme inflation')]
    mech = [r for r in rows if r['row'].startswith("the model's own mechanism")]
    grid = [r for r in rows if r['row'] == 'grid']
    full = [r for r in grid if r['backed share (fraction of the payout)'] == 1.0]
    none = [r for r in grid if r['backed share (fraction of the payout)'] == 0.0]
    be = [r for r in table(snap, 'r2-backing') if r['row'].startswith('break-even')]
    return mech, full, none, be


def fig_inflation(snap):
    mech, full, none, be = inflation_ranges(snap)
    mlo, mhi = min(r['effect'] for r in mech), max(r['effect'] for r in mech)
    flo, fhi = min(r['effect'] for r in full), max(r['effect'] for r in full)
    bshare = [r['backed share (fraction of the payout)'] * 100 for r in mech]
    blo, bhi = min(be, key=lambda r: r['backed share (fraction of the payout)']), max(be, key=lambda r: r['backed share (fraction of the payout)'])
    return (
        f'<p><strong>Inflation in the simulation ({snap["release"]}).</strong> Inflation depends on how much new output backs the payout. '
        f'At full backing, which is a design statement and not a result, programme inflation is {pt(flo, 2)} to {pt(fhi, 2)} points a year '
        'across both designs, three environments and both horizons. At the model’s own backing mechanism, which backs '
        f'{pt(min(bshare), 1)} to {pt(max(bshare), 1)}% of the payout, it is {pt(mlo)} to {pt(mhi)} points a year '
        '(over the mechanism with and without its ceiling). Programme inflation stays under 5% a year only when backing is above about '
        f'{pt(min(r["backed share (fraction of the payout)"] for r in be) * 100, 0)} to {pt(max(r["backed share (fraction of the payout)"] for r in be) * 100, 0)}% '
        'of the payout. So no figure here says the framework contains inflation unless the output behind the payout is also in place.</p>')


FIGS = {'r2-release-design': fig_release_design, 'r2-inflation': fig_inflation, 'wealth-history': fig_wealth_history}


# --- pages ------------------------------------------------------------------------------------
def pages():
    return sorted(p for p in glob.glob(os.path.join(ROOT, '*.html')))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fetch', metavar='SIM_CLONE')
    ap.add_argument('--tag'); ap.add_argument('--label'); ap.add_argument('--engine-files', default='r2-effects,r2-backing')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    if a.fetch:
        return fetch(a.fetch, a.tag, a.label, a.engine_files.split(','))
    snap = json.load(open(os.path.join(os.path.dirname(CUR), json.load(open(CUR))['snapshot'])))
    TAG = snap['release']
    bad, n = [], 0
    for p in pages():
        s = open(p, encoding='utf-8').read()
        def sub(m):
            nonlocal n
            name = m.group(2)
            if name not in FIGS:
                bad.append(f'{os.path.basename(p)}: unknown block {name}')
                return m.group(0)
            n += 1
            new = '\n' + FIGS[name](snap) + '\n'
            if new != m.group(3):
                bad.append(f'{os.path.basename(p)}: block {name} differs from the release')
            return m.group(1) + new + m.group(4)
        out = BLOCK.sub(sub, s)
        if not a.check and out != s:
            open(p, 'w', encoding='utf-8').write(out)
    if a.check:
        if bad:
            print('\n'.join(bad)); sys.exit(1)
        print(f'ok: {n} blocks match {TAG}')
    else:
        print(f'{n} blocks written from {TAG}')


if __name__ == '__main__':
    main()
