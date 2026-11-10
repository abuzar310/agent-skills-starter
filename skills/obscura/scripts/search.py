#!/usr/bin/env python3
"""Web search through Obscura: python search.py "your words" [-n 8] [--json]

Fetches DuckDuckGo's plain HTML results page with the `obscura` binary and prints
title, real URL and snippet for each result. Set OBSCURA_BIN if obscura is not on PATH.
"""
import argparse, json, os, shutil, subprocess, sys, urllib.parse

JS = (
    'JSON.stringify([...document.querySelectorAll(".result")].map(r=>{'
    'const a=r.querySelector(".result__a");let u=a&&a.getAttribute("href")||"";'
    'const m=u.match(/uddg=([^&]+)/);if(m)u=decodeURIComponent(m[1]);'
    'const s=r.querySelector(".result__snippet");'
    'return {title:a?a.textContent.trim():"",url:u,snippet:s?s.textContent.trim():""}'
    '}).filter(x=>x.url&&!x.url.includes("duckduckgo.com/y.js")))'
)


def find_bin():
    b = os.environ.get("OBSCURA_BIN") or shutil.which("obscura")
    if not b:
        sys.exit("obscura not found: install it (see SKILL.md) or set OBSCURA_BIN")
    return b


def main():
    ap = argparse.ArgumentParser(description="Search the web with Obscura")
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=8, help="results to show (default 8)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(a.query)
    p = subprocess.run([find_bin(), "fetch", url, "--quiet", "--timeout", "20", "--eval", JS],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    out = p.stdout.strip()
    try:
        results = json.loads(out[out.index("["):])[: a.n]
    except ValueError:
        sys.exit(f"No results (the search page may have refused the request).\n{p.stderr.strip()[:500]}")
    if not results:
        sys.exit("No results. If this keeps happening, use the agent's built-in web search.")
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}\n   {r['url']}\n   {r['snippet']}\n")


if __name__ == "__main__":
    main()
