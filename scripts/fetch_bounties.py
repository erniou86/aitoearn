#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AiToEarn - Global AI Bounty Scanner
扫描 GitHub 上所有带 bounty 标签的 AI 相关开放任务，输出可接单清单。
数据来源: GitHub Search API (公开数据, 无需认证)

用法:
    python scripts/fetch_bounties.py            # 输出前 20 条
    python scripts/fetch_bounties.py --top 50   # 输出前 50 条
    python scripts/fetch_bounties.py --save     # 同时保存到 bounties/latest.json
"""
import json
import ssl
import sys
import urllib.request
from datetime import datetime

# 已知的 bot 刷屏仓库，自动过滤
BOT_REPOS = {"relayhop/sn-monetization-runtime", "SPLURT-Station/S.P.L.U.R.T-tg"}
# 已知的娱乐/测试仓库，自动过滤
JUNK_REPOS = {"zhangjiayang6835-cyber/bounty-plaza", "iduyuhe/LDA"}

HEADERS = {
    "User-Agent": "AiToEarn-Bounty-Scanner/1.0",
    "Accept": "application/json",
}


def _ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def get(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
        return r.read().decode("utf-8", "ignore")


def clean(items, maxn=20):
    result = []
    for it in items or []:
        repo = it.get("repository_url", "").replace("https://api.github.com/repos/", "")
        if repo in BOT_REPOS or repo in JUNK_REPOS:
            continue
        title = it.get("title", "")
        if title.startswith("[radar]") or title.startswith("[BOUNTY] Suggestion"):
            continue
        result.append({
            "title": title[:120],
            "repo": repo,
            "url": it.get("html_url"),
            "created": (it.get("created_at") or "")[:10],
            "comments": it.get("comments", 0),
            "labels": [l.get("name") for l in it.get("labels", [])][:5],
        })
        if len(result) >= maxn:
            break
    return result


def scan(query: str, maxn: int = 20):
    url = (
        "https://api.github.com/search/issues?q="
        + urllib.request.quote(query, safe="")
        + "&per_page=50&sort=created&order=desc"
    )
    try:
        js = json.loads(get(url))
        return js.get("total_count", 0), clean(js.get("items", []), maxn)
    except Exception as e:
        return -1, [{"error": str(e)}]


def main():
    top = 20
    do_save = False
    for a in sys.argv[1:]:
        if a == "--save":
            do_save = True
        elif a.startswith("--top"):
            try:
                top = int(a.split("=")[1])
            except Exception:
                pass

    queries = {
        "AI bounty": "label:bounty+state:open+ai+in:title,body",
        "MCP bounty": "label:bounty+state:open+mcp+in:title,body",
        "Agent bounty": "label:bounty+state:open+agent+in:title,body",
    }

    print(f"# AiToEarn Bounty Scanner - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"扫描 GitHub 开放 bounty 任务\n")

    all_items = {}
    for name, q in queries.items():
        total, items = scan(q, top)
        all_items[name] = items
        print(f"## {name}: 共 {total} 个开放任务")
        for it in items:
            print(f"- [{it['repo']}] {it['title']}")
            print(f"  {it['url']} (comments: {it['comments']}, labels: {','.join(it['labels'])})")
        print()

    if do_save:
        import os
        out_dir = os.path.join(os.path.dirname(__file__), "..", "bounties")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "latest.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"scanned_at": datetime.now().isoformat(), "data": all_items},
                      f, ensure_ascii=False, indent=2)
        print(f"已保存: {os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
