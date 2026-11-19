"""
[THÀNH VIÊN 2] Duyệt đồ thị: BFS (hàng đợi) và DFS (đệ quy / ngăn xếp).

Các hàm được main.py và components.py gọi:
    bfs(g, s)               -> (order, parent)
    dfs(g, s)               -> (order, parent)
    format_tree(parent, s)  -> chuỗi cây duyệt

Chạy riêng để thử nhiều đỉnh xuất phát:
    python traversal.py --start "KCN Amata"
    python traversal.py --start "Cảng Phú Hữu" --edges data/edges.csv --nodes data/nodes.csv
"""
import argparse
import os
import sys
from collections import deque


def bfs(g, s):
    """BFS dùng hàng đợi (FIFO). Độ phức tạp O(|V| + |E|).

    Trả về (order, parent):
      order  : danh sách đỉnh theo thứ tự thăm
      parent : parent[v] = đỉnh cha trong cây BFS (parent[s] = None)
    """
    visited = {s}
    parent = {s: None}
    order = []
    q = deque([s])
    while q:
        u = q.popleft()
        order.append(u)                  # "tham u"
        for v in g.neighbors(u):
            if v not in visited:
                visited.add(v)           # đánh dấu ngay khi đưa vào hàng đợi
                parent[v] = u
                q.append(v)
    return order, parent


def dfs(g, s):
    """DFS đệ quy (ngăn xếp lời gọi hàm, LIFO). Độ phức tạp O(|V| + |E|).

    Trả về (order, parent) giống bfs.
    """
    visited = set()
    parent = {s: None}
    order = []

    def visit(u):
        visited.add(u)
        order.append(u)                  # "tham u"
        for v in g.neighbors(u):
            if v not in visited:
                parent[v] = u
                visit(v)

    visit(s)
    return order, parent


def dfs_iterative(g, s):
    """DFS dùng ngăn xếp tường minh, thay cho bản đệ quy khi đồ thị rất lớn.
    Cho cùng thứ tự thăm với dfs() ở trên.
    """
    visited = set()
    parent = {s: None}
    order = []
    stack = [(s, iter(g.neighbors(s)))]
    visited.add(s)
    order.append(s)
    while stack:
        u, it = stack[-1]
        for v in it:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                order.append(v)
                stack.append((v, iter(g.neighbors(v))))
                break
        else:
            stack.pop()                  # hết đỉnh kề chưa thăm -> quay lui
    return order, parent


def format_tree(parent, root):
    """Trả về chuỗi vẽ cây duyệt (từ mảng parent) dạng cây thư mục."""
    children = {}
    for v, p in parent.items():
        if p is not None:
            children.setdefault(p, []).append(v)

    lines = [str(root)]

    def walk(u, prefix):
        kids = children.get(u, [])
        for i, c in enumerate(kids):
            last = i == len(kids) - 1
            lines.append(prefix + ("└── " if last else "├── ") + str(c))
            walk(c, prefix + ("    " if last else "│   "))

    walk(root, "")
    return "\n".join(lines)


def hops(parent, v):
    """Số cạnh trên đường đi từ gốc tới v theo cây duyệt."""
    d = 0
    while parent[v] is not None:
        v = parent[v]
        d += 1
    return d


def count_components(g, algo):
    """Đếm thành phần liên thông bằng BFS hoặc DFS (mục 1.2.3)."""
    visited, n = set(), 0
    for v in g.vertices:
        if v not in visited:
            order, _ = algo(g, v)
            visited.update(order)
            n += 1
    return n


def _cli():
    from graph_io import load_graph

    base = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Duyệt BFS và DFS từ một đỉnh xuất phát")
    ap.add_argument("--start", required=True, help="tên đỉnh xuất phát, ví dụ \"KCN Amata\"")
    ap.add_argument("--edges", default=os.path.join(base, "data", "edges.csv"))
    ap.add_argument("--nodes", default=os.path.join(base, "data", "nodes.csv"))
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.setrecursionlimit(10000)

    g, _ = load_graph(args.edges, args.nodes)
    s = args.start
    if s not in g.adj:
        sys.exit("Lỗi: đỉnh '%s' không có trong đồ thị.\nCác đỉnh hợp lệ:\n  %s"
                 % (s, "\n  ".join(g.vertices)))

    b_order, b_par = bfs(g, s)
    d_order, d_par = dfs(g, s)
    total = len(g.vertices)

    print(f"=== Đỉnh xuất phát: {s} ===")
    for name, order, par in (("BFS", b_order, b_par), ("DFS", d_order, d_par)):
        print(f"\n--- {name}: thăm {len(order)}/{total} đỉnh ---")
        print("Thứ tự: " + " → ".join(order))
        print(f"Cây {name}:")
        print(format_tree(par, s))

    print("\n--- So sánh BFS và DFS ---")
    print("Cùng tập đỉnh được thăm:", set(b_order) == set(d_order))
    print("Độ sâu cây BFS:", max(hops(b_par, v) for v in b_par),
          "| Độ sâu cây DFS:", max(hops(d_par, v) for v in d_par))
    worse = [(v, hops(b_par, v), hops(d_par, v)) for v in b_order
             if hops(d_par, v) > hops(b_par, v)]
    print(f"Số đỉnh mà đường đi DFS dài hơn BFS (tính theo số cạnh): {len(worse)}")
    for v, hb, hd in worse[:5]:
        print(f"  {s} → {v}: BFS = {hb} cạnh, DFS = {hd} cạnh")

    print("\n--- Thành phần liên thông (Câu hỏi vấn đáp 1) ---")
    cb, cd = count_components(g, bfs), count_components(g, dfs)
    print(f"BFS: {cb} thành phần | DFS: {cd} thành phần | Bằng nhau: {cb == cd}")


if __name__ == "__main__":
    _cli()
