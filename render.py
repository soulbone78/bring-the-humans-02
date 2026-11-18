#!/usr/bin/env python3
"""render.py — render README.md as a GitHub-style repository page (HTML).

Pure standard library. The HTML is screenshotted with Playwright to produce
screenshot.png for the bring-the-humans-02 entry (a GitHub repository page
with this README showing, the way the bounty asks for it).

The three make.fun badge images are fetched live and embedded as data URIs so
the capture never shows a broken image; if the fetch fails, a simple local
SVG badge with the same words is drawn instead.

Usage:
    python3 render.py [README.md] [page.html]
"""

import base64
import html
import re
import sys
import urllib.request
from pathlib import Path

OWNER = "soulbone78"
REPO = "bring-the-humans-02"
BOUNTY_URL = "https://make.fun/bounty/bring-the-humans-02"

# label, value shown when a badge cannot be fetched live
BADGE_FALLBACK = {
    "https://make.fun/badge/bring-the-humans-02.svg": ("make.fun", "bring-the-humans-02"),
    "https://make.fun/badge/bring-the-humans-02/soulbone78/bring-the-humans-02/rank.svg": ("rank", "pending"),
    "https://make.fun/badge/bring-the-humans-02/soulbone78/bring-the-humans-02/reward.svg": ("reward", "$1,000 USDC"),
}

_badge_cache = {}


def fetch_badge(url):
    """Return a data-URI for a badge SVG, fetched live, or a local fallback."""
    if url in _badge_cache:
        return _badge_cache[url]
    data_uri = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "render.py"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
        if raw.lstrip().startswith(b"<svg"):
            data_uri = "data:image/svg+xml;base64," + base64.b64encode(raw).decode()
    except Exception:
        data_uri = None
    if data_uri is None:
        left, right = BADGE_FALLBACK.get(url, ("make.fun", "badge"))
        lw, rw = len(left) * 7 + 12, len(right) * 7 + 12
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="20">'
            '<rect width="%d" height="20" fill="#555"/>'
            '<rect x="%d" width="%d" height="20" fill="#4c1"/>'
            '<text x="%d" y="14" fill="#fff" font-family="Verdana" font-size="11" '
            'text-anchor="middle">%s</text>'
            '<text x="%d" y="14" fill="#fff" font-family="Verdana" font-size="11" '
            'text-anchor="middle">%s</text></svg>'
            % (lw + rw, lw, lw, rw, lw // 2, html.escape(left),
               lw + rw // 2, html.escape(right))
        )
        data_uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    _badge_cache[url] = data_uri
    return data_uri


def slugify(text):
    """GitHub-style heading anchor: lowercase, punctuation dropped, spaces to -."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s", "-", text.strip())


def inline(text):
    """Inline markdown: `code`, images, links, **bold**, *italic*."""
    code_spans = []

    def stash_code(m):
        code_spans.append(m.group(1))
        return "\x00%d\x00" % (len(code_spans) - 1)

    text = re.sub(r"`([^`\n]+)`", stash_code, text)
    text = html.escape(text)

    def image(m):
        alt, src = m.group(1), m.group(2)
        if src.startswith("https://make.fun/badge/"):
            src = fetch_badge(src)
        return '<img src="%s" alt="%s">' % (html.escape(src, quote=True), alt)

    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", image, text)

    def link(m):
        label, href = m.group(1), m.group(2)
        return '<a href="%s">%s</a>' % (html.escape(href, quote=True), label)

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)

    def restore_code(m):
        return "<code>%s</code>" % html.escape(code_spans[int(m.group(1))])

    return re.sub(r"\x00(\d+)\x00", restore_code, text)


_BLOCK_START = re.compile(
    r"^(#{1,6}\s|```|---+\s*$|\||>\s?|[-*]\s+\S|\d+[.)]\s+|<details>|<sub>|<sup>)"
)


def parse_blocks(lines):
    """Parse GitHub-flavoured Markdown lines into a list of block tuples."""
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            blocks.append(("h", len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            buf, j = [], i + 1
            while j < n and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            blocks.append(("code", lang, "\n".join(buf)))
            i = j + 1
            continue
        if re.match(r"^---+\s*$", line):
            blocks.append(("hr",))
            i += 1
            continue
        if line.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            rows, j = [], i + 2
            while j < n and lines[j].startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            blocks.append(("table", header, rows))
            i = j
            continue
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                rest = lines[i][1:]
                buf.append(rest[1:] if rest.startswith(" ") else rest)
                i += 1
            blocks.append(("quote", parse_blocks(buf)))
            continue
        if line.startswith("<details>"):
            inner, j = [], i + 1
            while j < n and lines[j].strip() != "</details>":
                inner.append(lines[j])
                j += 1
            summary = ""
            if inner and inner[0].strip().startswith("<summary>"):
                summary = re.sub(r"^<summary>(.*)</summary>$", r"\1",
                                 inner[0].strip())
                inner = inner[1:]
            blocks.append(("details", summary, parse_blocks(inner)))
            i = j + 1
            continue
        if line.lstrip().startswith("<sub>") or line.lstrip().startswith("<sup>"):
            blocks.append(("html", line.strip()))
            i += 1
            continue
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            items = []
            while i < n:
                m2 = re.match(r"^[-*]\s+(.*)$", lines[i])
                if not m2:
                    break
                items.append(m2.group(1))
                i += 1
            blocks.append(("ul", items))
            continue
        m = re.match(r"^\d+[.)]\s+(.*)$", line)
        if m:
            items = []
            while i < n:
                m2 = re.match(r"^\d+[.)]\s+(.*)$", lines[i])
                if not m2:
                    break
                items.append(m2.group(1))
                i += 1
            blocks.append(("ol", items))
            continue
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not _BLOCK_START.match(lines[i]):
            buf.append(lines[i])
            i += 1
        blocks.append(("p", " ".join(part.strip() for part in buf)))
    return blocks


def render_blocks(blocks):
    out = []
    for block in blocks:
        kind = block[0]
        if kind == "h":
            _, level, text = block
            out.append('<h%d id="%s">%s</h%d>'
                       % (level, slugify(text), inline(text), level))
        elif kind == "p":
            out.append("<p>%s</p>" % inline(block[1]))
        elif kind == "code":
            _, lang, code = block
            cls = ' class="language-%s"' % html.escape(lang) if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, html.escape(code)))
        elif kind == "hr":
            out.append("<hr>")
        elif kind == "table":
            _, header, rows = block
            cells = "".join("<th>%s</th>" % inline(c) for c in header)
            body = "".join(
                "<tr>" + "".join("<td>%s</td>" % inline(c) for c in row) + "</tr>"
                for row in rows)
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
                       % (cells, body))
        elif kind == "quote":
            out.append("<blockquote>%s</blockquote>" % render_blocks(block[1]))
        elif kind == "details":
            _, summary, inner = block
            out.append("<details><summary>%s</summary>%s</details>"
                       % (summary, render_blocks(inner)))
        elif kind == "html":
            text = block[1]
            m = re.match(r"^<(sub|sup)>(.*)</(sub|sup)>$", text)
            if m:
                out.append("<%s>%s</%s>" % (m.group(1), inline(m.group(2)), m.group(1)))
            else:
                out.append(text)
        elif kind == "ul":
            items = []
            for it in block[1]:
                m = re.match(r"^\[([ xX])\]\s+(.*)$", it)
                if m:
                    checked = " checked" if m.group(1).lower() == "x" else ""
                    items.append('<li class="task"><input type="checkbox" disabled%s> %s</li>'
                                 % (checked, inline(m.group(2))))
                else:
                    items.append("<li>%s</li>" % inline(it))
            out.append("<ul>%s</ul>" % "".join(items))
        elif kind == "ol":
            out.append("<ol>%s</ol>"
                       % "".join("<li>%s</li>" % inline(it) for it in block[1]))
    return "\n".join(out)


CSS = """
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;font-size:14px;line-height:1.5;color:#1f2328;background:#fff}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}
.gh-header{background:#010409;color:#fff;padding:14px 24px;display:flex;align-items:center;gap:16px}
.gh-header .logo{font-size:20px;font-weight:700}
.gh-header .search{border:1px solid #3d444d;border-radius:6px;padding:4px 12px;color:#9198a1;font-size:13px;width:260px}
.repo-head{padding:20px 24px 0;border-bottom:1px solid #d0d7de}
.repo-name{font-size:20px;font-weight:400}
.repo-name .owner{color:#0969da}.repo-name .sep{color:#656d76;padding:0 4px}
.repo-name .name{color:#0969da;font-weight:600}
.public{border:1px solid #d0d7de;border-radius:2em;color:#656d76;font-size:12px;padding:1px 8px;margin-left:8px;vertical-align:middle}
.tabs{display:flex;gap:24px;margin-top:16px}
.tabs span{padding:8px 2px;color:#1f2328}
.tabs .active{border-bottom:2px solid #fd8c73;font-weight:600}
.container{display:flex;gap:24px;max-width:1280px;margin:0 auto;padding:16px 24px 32px}
.main{flex:1;min-width:0}
.file-box{border:1px solid #d0d7de;border-radius:6px;margin-bottom:16px}
.file-header{background:#f6f8fa;padding:10px 16px;border-bottom:1px solid #d0d7de;font-size:13px}
.file-header b{color:#1f2328}
.file-row{display:flex;gap:10px;padding:8px 16px;border-top:1px solid #d0d7de;font-size:14px}
.file-row:first-child{border-top:none}
.file-row .fname{color:#1f2328}
.readme-box{border:1px solid #d0d7de;border-radius:6px}
.readme-header{padding:12px 16px;border-bottom:1px solid #d0d7de;font-weight:600;display:flex;justify-content:space-between}
.markdown-body{padding:32px;font-size:16px;line-height:1.6;word-wrap:break-word}
.markdown-body h1{font-size:2em;border-bottom:1px solid #d0d7de;padding-bottom:.3em;margin:.67em 0}
.markdown-body h2{font-size:1.5em;border-bottom:1px solid #d0d7de;padding-bottom:.3em;margin-top:24px}
.markdown-body p{margin:0 0 16px}
.markdown-body ul,.markdown-body ol{padding-left:2em;margin:0 0 16px}
.markdown-body li+li{margin-top:.25em}
.markdown-body li.task{list-style:none;margin-left:-1.6em}
.markdown-body li.task input{margin-right:6px;vertical-align:middle}
.markdown-body code{padding:.2em .4em;background:rgba(175,184,193,.2);border-radius:6px;font-size:85%;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.markdown-body pre{padding:16px;background:#f6f8fa;border-radius:6px;overflow:auto;line-height:1.45;font-size:85%}
.markdown-body pre code{padding:0;background:transparent;font-size:100%}
.markdown-body table{border-collapse:collapse;margin:0 0 16px;display:block;overflow:auto}
.markdown-body th,.markdown-body td{padding:6px 13px;border:1px solid #d0d7de}
.markdown-body th{background:#f6f8fa;font-weight:600}
.markdown-body blockquote{border-left:.25em solid #d0d7de;color:#656d76;padding:0 1em;margin:0 0 16px}
.markdown-body blockquote p{margin-bottom:8px}
.markdown-body hr{height:.25em;background:#d0d7de;border:0;margin:24px 0}
.markdown-body details{border:1px solid #d0d7de;border-radius:6px;padding:10px 16px;margin:0 0 16px}
.markdown-body summary{cursor:pointer;font-weight:600}
.markdown-body summary::-webkit-details-marker{color:#656d76}
.markdown-body img{vertical-align:middle;margin:0 4px 8px 0}
.sidebar{width:296px;flex-shrink:0}
.sidebar h3{font-size:16px;margin:4px 0 8px}
.sidebar p{color:#1f2328}
.sidebar .website{word-break:break-all}
.topic{display:inline-block;background:#ddf4ff;color:#0969da;border-radius:2em;padding:2px 10px;font-size:12px;font-weight:500;margin:4px 4px 0 0}
.page-footer{border-top:1px solid #d0d7de;color:#656d76;font-size:12px;text-align:center;padding:24px}
"""

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>__OWNER__/__REPO__: Earn USDC with your AI coding agent</title>
<style>__CSS__</style></head><body>
<div class="gh-header"><span class="logo">GitHub</span><span class="search">Type / to search</span></div>
<div class="repo-head">
<div class="repo-name"><span class="owner">__OWNER__</span><span class="sep">/</span><span class="name">__REPO__</span><span class="public">Public</span></div>
<div class="tabs"><span class="active">Code</span><span>Issues</span><span>Pull requests</span><span>Actions</span><span>Projects</span><span>Wiki</span><span>Security</span><span>Insights</span></div>
</div>
<div class="container"><div class="main">
<div class="file-box">
<div class="file-header"><b>main</b> &nbsp;·&nbsp; 4 Files</div>
<div class="file-row"><span>📄</span><span class="fname">LICENSE</span></div>
<div class="file-row"><span>📄</span><span class="fname">README.md</span></div>
<div class="file-row"><span>📄</span><span class="fname">render.py</span></div>
<div class="file-row"><span>🖼️</span><span class="fname">screenshot.png</span></div>
</div>
<div class="readme-box"><div class="readme-header"><span>README.md</span><span>Preview</span></div>
<div class="markdown-body">
__BODY__
</div></div></div>
<div class="sidebar"><h3>About</h3>
<p>A newcomer&rsquo;s guide to make.fun: what it is, how to set up, and how to earn USDC with your AI coding agent.</p>
<p class="website"><a href="__BOUNTY_URL__">make.fun/bounty/bring-the-humans-02</a></p>
<p><span class="topic">makefun</span></p>
</div></div>
<div class="page-footer">Rendered from README.md by render.py &middot; a GitHub-style view of this repository</div>
</body></html>
"""


def build_page(readme_text):
    body = render_blocks(parse_blocks(readme_text.splitlines()))
    page = (PAGE.replace("__OWNER__", OWNER)
                .replace("__REPO__", REPO)
                .replace("__BOUNTY_URL__", BOUNTY_URL)
                .replace("__CSS__", CSS)
                .replace("__BODY__", body))
    return page


def main():
    readme_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("README.md")
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("page.html")
    text = readme_path.read_text(encoding="utf-8")
    out_path.write_text(build_page(text), encoding="utf-8")
    print("wrote %s (%d bytes)" % (out_path, out_path.stat().st_size))


if __name__ == "__main__":
    main()
