"""Minimal ThuyenMCP hub client (stateless MCP JSON-RPC over HTTP).

Usage:
  python -I tools/thuyenmcp.py list                      # list tool names
  python -I tools/thuyenmcp.py schema <tool>             # show a tool's input schema
  python -I tools/thuyenmcp.py call <tool> '<json args>' # call a tool, print result

Auth: in Claude cloud sessions the agent sub-token is injected by the network proxy.
Elsewhere set THUYENMCP_TOKEN (sent as Authorization: Bearer). Never commit the token.
Endpoint override: THUYENMCP_URL (default https://sound.thuyenlabs.io.vn/mcp).
"""
import json, os, sys, time
import requests

URL = os.environ.get("THUYENMCP_URL", "https://sound.thuyenlabs.io.vn/mcp")


def rpc(method, params=None, timeout=600, retries=3):
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
         "MCP-Protocol-Version": "2025-06-18"}
    tok = os.environ.get("THUYENMCP_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    for i in range(retries):
        try:
            r = requests.post(URL, json=body, headers=h, timeout=timeout)
            r.raise_for_status()
            txt = r.text
            if txt.lstrip().startswith("event:") or "\ndata:" in txt or txt.startswith("data:"):
                txt = [l[5:].strip() for l in txt.splitlines() if l.startswith("data:")][-1]
            d = json.loads(txt)
            if "error" in d:
                raise RuntimeError(d["error"])
            return d["result"]
        except (requests.ConnectionError, requests.Timeout):
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))


def call(tool, args=None, **kw):
    res = rpc("tools/call", {"name": tool, "arguments": args or {}}, **kw)
    out = []
    for c in res.get("content", []):
        out.append(c.get("text") if c.get("type") == "text" else json.dumps(c)[:500])
    if res.get("isError"):
        raise RuntimeError("\n".join(out))
    return "\n".join(o for o in out if o)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        for t in rpc("tools/list")["tools"]:
            print(t["name"])
    elif cmd == "schema":
        t = next(t for t in rpc("tools/list")["tools"] if t["name"] == sys.argv[2])
        print(t.get("description", "")); print(json.dumps(t.get("inputSchema"), indent=1, ensure_ascii=False))
    elif cmd == "call":
        print(call(sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}))
