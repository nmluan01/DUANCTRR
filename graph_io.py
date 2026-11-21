"""
[THÀNH VIÊN 1] Xây dựng cấu trúc dữ liệu đồ thị + kiểm tra hợp lệ dữ liệu đầu vào.
Đồ thị vô hướng G = (V, E), trọng số = chiều dài đoạn đường (km).
Lưu bằng DANH SÁCH KỀ (dict), có hàm xuất MA TRẬN KỀ.
"""
import csv


class Graph:
    def __init__(self):
        self.adj = {}      # adj[u] = {v: w, ...}
        self.coords = {}   # coords[u] = (x_km, y_km)

    def add_vertex(self, v):
        self.adj.setdefault(v, {})

    def add_edge(self, u, v, w):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u][v] = w
        self.adj[v][u] = w          # vô hướng

    def has_edge(self, u, v):
        return v in self.adj.get(u, {})

    @property
    def vertices(self):
        return sorted(self.adj)

    @property
    def edges(self):
        """Danh sách cạnh (u, v, w), mỗi cạnh một lần."""
        seen, out = set(), []
        for u in self.adj:
            for v, w in self.adj[u].items():
                if (v, u) not in seen:
                    seen.add((u, v))
                    out.append((u, v, w))
        return out

    def neighbors(self, u):
        return sorted(self.adj[u])

    def to_matrix(self):
        """Trả về (danh_sách_đỉnh, ma_trận_kề); 0 = không có cạnh."""
        vs = self.vertices
        idx = {v: i for i, v in enumerate(vs)}
        m = [[0] * len(vs) for _ in vs]
        for u, v, w in self.edges:
            m[idx[u]][idx[v]] = m[idx[v]][idx[u]] = w
        return vs, m


def load_nodes(path, g):
    """Đọc toạ độ đỉnh (phục vụ vẽ sơ đồ và đề xuất tuyến theo khoảng cách)."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            name = row["ten"].strip()
            g.add_vertex(name)
            g.coords[name] = (float(row["x_km"]), float(row["y_km"]))


def load_graph(edge_path, node_path=None):
    """
    Đọc file cạnh CSV (dinh_a, dinh_b, chieu_dai_km).
    Trả về (Graph, danh_sách_cảnh_báo). Dòng lỗi bị bỏ qua và ghi cảnh báo:
      - thiếu cột / tên rỗng, - trọng số không phải số hoặc <= 0,
      - khuyên (u == v),    - cạnh trùng lặp.
    """
    g, warnings = Graph(), []
    if node_path:
        load_nodes(node_path, g)

    with open(edge_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # bỏ dòng tiêu đề
        for ln, row in enumerate(reader, start=2):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) < 3 or not row[0].strip() or not row[1].strip():
                warnings.append(f"Dòng {ln}: thiếu dữ liệu -> bỏ qua")
                continue
            u, v = row[0].strip(), row[1].strip()
            try:
                w = float(row[2])
            except ValueError:
                warnings.append(f"Dòng {ln}: chiều dài '{row[2]}' không phải số -> bỏ qua")
                continue
            if w <= 0:
                warnings.append(f"Dòng {ln}: chiều dài <= 0 -> bỏ qua")
                continue
            if u == v:
                warnings.append(f"Dòng {ln}: khuyên ({u}) -> bỏ qua")
                continue
            if g.has_edge(u, v):
                warnings.append(f"Dòng {ln}: cạnh {u}-{v} bị trùng -> bỏ qua")
                continue
            g.add_edge(u, v, w)
    return g, warnings

if __name__ == "__main__":

    import os
    base = os.path.dirname(os.path.abspath(__file__))
    g, warns = load_graph(os.path.join(base, "data", "edges.csv"),
                          os.path.join(base, "data", "nodes.csv"))

    print(f"|V| = {len(g.vertices)} đỉnh, |E| = {len(g.edges)} cạnh")
    print(f"Cảnh báo dữ liệu: {len(warns)}")
    for w in warns:
        print("  !", w)

    print("\nDanh sách kề:")
    for u in g.vertices:
        print(f"  {u:<20} -> " + ", ".join(f"{v}({w:g})" for v, w in sorted(g.adj[u].items())))

    vs, m = g.to_matrix()
    print("\nMa trận kề (5 đỉnh đầu):")
    for i in range(5):
        print(f"  {vs[i]:<20}", m[i][:5])
