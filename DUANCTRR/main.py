"""
Đề tài 1: Kiểm tra tính liên thông của mạng lưới đường bộ kết nối các KCN.
Chạy:  python main.py [edges.csv] [nodes.csv]
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))   # thư mục chứa main.py
from graph_io import load_graph
from traversal import bfs, dfs, format_tree
from components import find_components, isolated_areas, suggest_links
from visualize import draw


def main():
    edge_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "data", "edges.csv")
    node_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "data", "nodes.csv")
    out = []
    P = lambda s="": (print(s), out.append(s))

    # 1. Xây dựng đồ thị + kiểm tra hợp lệ
    g, warns = load_graph(edge_file, node_file)
    P("=" * 70)
    P("1. CẤU TRÚC DỮ LIỆU ĐỒ THỊ")
    P(f"   |V| = {len(g.vertices)} đỉnh, |E| = {len(g.edges)} cạnh")
    P(f"   Cảnh báo dữ liệu: {len(warns)}")
    for w in warns:
        P("   ! " + w)
    P("   Danh sách kề:")
    for u in g.vertices:
        P(f"   {u:<20} -> " + ", ".join(f"{v}({w:g})" for v, w in sorted(g.adj[u].items())))

    # 2. BFS / DFS
    start = "KCN Amata" if "KCN Amata" in g.adj else g.vertices[0]
    P("\n" + "=" * 70)
    P(f"2. DUYỆT ĐỒ THỊ TỪ ĐỈNH XUẤT PHÁT: {start}")
    for name, fn in (("BFS", bfs), ("DFS", dfs)):
        order, parent = fn(g, start)
        P(f"\n--- {name}: thăm {len(order)}/{len(g.vertices)} đỉnh ---")
        P("Thứ tự: " + " → ".join(order))
        P(f"Cây {name}:")
        P(format_tree(parent, start))

    # 3. Thành phần liên thông (kiểm tra chéo BFS == DFS)
    cb, cd = find_components(g, "bfs"), find_components(g, "dfs")
    P("\n" + "=" * 70)
    P("3. THÀNH PHẦN LIÊN THÔNG")
    P(f"   BFS: {len(cb)} thành phần | DFS: {len(cd)} thành phần | "
      f"Trùng khớp: {sorted(cb) == sorted(cd)}")
    P("   => Mạng lưới " + ("LIÊN THÔNG" if len(cb) == 1 else "KHÔNG liên thông"))
    for i, c in enumerate(cb, 1):
        P(f"   TP {i} ({len(c)} đỉnh): " + ", ".join(c))

    # 4. Khoanh vùng + đề xuất
    iso = isolated_areas(cb)
    P("\n" + "=" * 70)
    P("4. KHU VỰC BỊ CÔ LẬP & ĐỀ XUẤT TUYẾN BỔ SUNG")
    if not iso:
        P("   Không có khu vực cô lập.")
        sug = []
    else:
        for i, c in enumerate(iso, 1):
            P(f"   Khu vực cô lập {i}: " + ", ".join(c))
        sug = suggest_links(g, cb)
        P(f"   Cần tối thiểu {len(sug)} tuyến mới (= số TP - 1):")
        for u, v, d, comp in sug:
            P(f"   + Nối '{u}' ↔ '{v}' (≈ {d} km đường chim bay) -> nối nhóm {len(comp)} đỉnh [{comp[0]}, ...] vào mạng chính")
        P(f"   Tổng chiều dài đề xuất ≈ {round(sum(s[2] for s in sug), 1)} km")

    # 5. Trực quan hoá
    draw(g, cb, sug, os.path.join(BASE, "ket_qua_do_thi.png"),
         "Mạng lưới đường bộ các KCN Đồng Nai – thành phần liên thông")
    P("\n5. Đã lưu sơ đồ: ket_qua_do_thi.png")
    open(os.path.join(BASE, "ket_qua.txt"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
