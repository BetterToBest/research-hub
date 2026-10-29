"""Rebuild paper PDFs from their HTML pages.

    python3 tools/build_pdfs.py optimal-transfer-design dual-currency-inflation
    python3 tools/build_pdfs.py --all
    python3 tools/build_pdfs.py --list

Each paper `<name>.html` at the repository root has its PDF at
`papers/pdfs/<name>.pdf`. The script prints the HTML page to that file with
headless Chrome or Chromium (the earlier PDFs were made the same way, by Chrome's
print to PDF), using the page's own print stylesheet in styles.css. Run it whenever
a paper's HTML changes (CLAUDE.md).

The browser is --browser, else $CHROME, else the first of chrome-headless-shell,
chromium, chromium-browser, google-chrome, google-chrome-stable or chrome on the
PATH, else a Playwright headless shell or Chromium under /opt/pw-browsers. Prefer
chrome-headless-shell where it exists: in some containers full Chrome in headless
mode hangs instead of exiting. After each build the script
checks that the file is a PDF and, if pdftotext is installed, that its text
contains the page's title (the <h1>). Exit code 1 if any build fails.
"""
import argparse
import glob
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "papers" / "pdfs"


def papers():
    """Names that have both a root HTML page and a PDF."""
    return sorted(p.stem for p in PDF_DIR.glob("*.pdf") if (ROOT / f"{p.stem}.html").exists())


def find_browser(explicit):
    for c in (explicit, os.environ.get("CHROME")):
        if c:
            return c
    for name in ("chrome-headless-shell", "chromium", "chromium-browser", "google-chrome",
                 "google-chrome-stable", "chrome"):
        path = shutil.which(name)
        if path:
            return path
    for pattern in ("/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell",
                    "/opt/pw-browsers/chromium-*/chrome-linux*/chrome"):
        found = sorted(glob.glob(pattern))
        if found:
            return found[-1]
    sys.exit("No Chrome or Chromium found; pass --browser or set $CHROME.")


def title_of(page):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", page.read_text(encoding="utf-8"), re.S)
    if not m:
        return None
    text = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
    return " ".join(text.split())


def build(name, browser, timeout):
    page = ROOT / f"{name}.html"
    out = PDF_DIR / f"{name}.pdf"
    with tempfile.TemporaryDirectory() as profile:
        tmp = pathlib.Path(profile) / "out.pdf"
        cmd = [browser, "--headless", "--no-sandbox", "--disable-gpu", "--no-first-run",
               f"--user-data-dir={profile}", "--no-pdf-header-footer",
               f"--print-to-pdf={tmp}", page.as_uri()]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if not tmp.exists() or not tmp.read_bytes().startswith(b"%PDF"):
            return f"no PDF written (exit {r.returncode}): {r.stderr.strip()[-300:]}"
        if shutil.which("pdftotext"):
            want = title_of(page)
            got = subprocess.run(["pdftotext", "-layout", str(tmp), "-"], capture_output=True, text=True).stdout
            if want and " ".join(want.split()[:6]) not in " ".join(got.split()):
                return f"PDF text does not contain the page title {want[:60]!r}"
        shutil.move(str(tmp), out)
    return None


def main():
    ap = argparse.ArgumentParser(description="Rebuild paper PDFs from their HTML pages.")
    ap.add_argument("names", nargs="*", help="paper names (HTML file names without .html)")
    ap.add_argument("--all", action="store_true", help="rebuild every paper's PDF")
    ap.add_argument("--list", action="store_true", help="list the papers that have a PDF")
    ap.add_argument("--browser", help="path to Chrome or Chromium")
    ap.add_argument("--timeout", type=int, default=120, help="seconds per page (default 120)")
    o = ap.parse_args()
    known = papers()
    if o.list:
        print("\n".join(known))
        return
    names = known if o.all else [n.removesuffix(".html") for n in o.names]
    if not names:
        ap.error("name at least one paper, or use --all")
    unknown = [n for n in names if n not in known]
    if unknown:
        sys.exit(f"Not a paper with a PDF: {', '.join(unknown)} (see --list)")
    browser = find_browser(o.browser)
    failed = 0
    for n in names:
        err = build(n, browser, o.timeout)
        print(f"{'FAIL' if err else 'ok  '}  papers/pdfs/{n}.pdf" + (f": {err}" if err else ""))
        failed += bool(err)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
