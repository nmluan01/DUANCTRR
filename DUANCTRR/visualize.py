"""Trực quan hóa đồ thị mạng lưới đường bộ và các tuyến kết nối đề xuất.

Bố cục 3 cột: bảng mã đỉnh | bản đồ mạng lưới | bảng dữ liệu đầu vào.
"""
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

# Kiểu đỉnh: (tiền tố mã, hình marker, nhãn chú giải)
KIND_STYLE = {
    "kcn": ("K", "s", "KCN"),
    "cang": ("C", "D", "Cảng"),
    "nut": ("N", "o", "Nút giao"),
    "khac": ("V", "o", "Khác"),
}


def _kind(name):
    n = name.strip().lower()
    if n.startswith("kcn"):
        return "kcn"
    if n.startswith("cảng") or n.startswith("cang"):
        return "cang"
    if n.startswith("nút") or n.startswith("nut"):
        return "nut"
    return "khac"


def draw(g, components, suggestions, output="ket_qua_do_thi.png",
         title="Kiểm tra tính liên thông của mạng lưới đường bộ kết nối các khu công nghiệp"):
    """Vẽ đồ thị theo tọa độ g.coords.

    components: danh sách các thành phần liên thông.
    suggestions: [(u, v, distance_km, component), ...].
    output: đường dẫn ảnh đầu ra.
    """
    if not g.vertices:
        raise ValueError("Đồ thị không có đỉnh để trực quan hóa.")

    palette = plt.get_cmap("tab10")
    comp_of = {}
    for i, comp in enumerate(components):
        for v in comp:
            comp_of[v] = i

    # Mã đỉnh theo loại: K1, K2..., C1..., N1...
    counters = {k: 0 for k in KIND_STYLE}
    code, kind_of = {}, {}
    for v in g.vertices:
        k = _kind(v)
        counters[k] += 1
        code[v] = f"{KIND_STYLE[k][0]}{counters[k]}"
        kind_of[v] = k

    # Đỉnh thiếu tọa độ được đặt theo vòng tròn để vẫn hiển thị được.
    n = len(g.vertices)
    pos = {}
    for i, v in enumerate(g.vertices):
        if v in g.coords:
            pos[v] = g.coords[v]
        else:
            a = 2 * math.pi * i / max(n, 1)
            pos[v] = (math.cos(a) * 10, math.sin(a) * 10)

    fig = plt.figure(figsize=(21, 11), facecolor="white")
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 3.8, 1.45], wspace=0.04,
                          left=0.01, right=0.99, top=0.88, bottom=0.04)
    ax_l = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])
    ax_r = fig.add_subplot(gs[2])

    # ---------- Tiêu đề ----------
    fig.text(0.5, 0.945, title, ha="center", va="center", fontsize=18,
             weight="bold", color="white",
             bbox=dict(boxstyle="round,pad=0.5,rounding_size=0.6",
                       fc="#14306b", ec="none"))

    # ---------- Cột trái: bảng mã đỉnh ----------
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1)
    ax_l.set_xticks([]); ax_l.set_yticks([])
    ax_l.set_facecolor("#f6f6fb")
    for s in ax_l.spines.values():
        s.set_color("#9aa5d6")
    ax_l.set_title("Bảng mã đỉnh", fontsize=11, weight="bold", color="white",
                   bbox=dict(boxstyle="round,pad=0.35", fc="#3d5bb8", ec="none"))
    step = min(0.045, 0.94 / max(n, 1))
    y = 0.96
    for v in g.vertices:
        k = kind_of[v]
        ci = comp_of.get(v, 0)
        ax_l.scatter(0.07, y, s=55, marker=KIND_STYLE[k][1], color=palette(ci % 10),
                     edgecolor="black", linewidth=.5)
        ax_l.text(0.15, y, code[v], fontsize=8.5, weight="bold", va="center")
        ax_l.text(0.30, y, v, fontsize=8.5, va="center")
        y -= step
    present = sorted({kind_of[v] for v in g.vertices})
    ax_l.legend(handles=[Line2D([0], [0], marker=KIND_STYLE[k][1], color="w",
                                markerfacecolor="#888", markeredgecolor="black",
                                markersize=7, label=KIND_STYLE[k][2]) for k in present],
                loc="lower center", ncol=3, fontsize=7.5, frameon=False,
                handletextpad=0.2, columnspacing=0.8)

    # ---------- Cột giữa: bản đồ ----------
    ax.set_facecolor("#e9f1df")
    for s in ax.spines.values():
        s.set_color("#9fbf8a")
    ax.set_title("Mạng lưới giao thông (đồ thị)", fontsize=11, weight="bold", color="white",
                 bbox=dict(boxstyle="round,pad=0.35", fc="#3d5bb8", ec="none"))

    # Cạnh hiện có
    for u, v, w in g.edges:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        ci = comp_of.get(u, 0)
        ax.plot([x1, x2], [y1, y2], color=palette(ci % 10), lw=2.0, alpha=.8, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{w:g}", fontsize=7, color="#333333",
                ha="center", va="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=.75, pad=1), zorder=2)

    # Tuyến đề xuất – nét đứt đỏ
    for u, v, d, *_ in suggestions:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        ax.plot([x1, x2], [y1, y2], linestyle="--", color="red", lw=2.8, zorder=3)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"+{d:g} km", fontsize=8, color="red",
                ha="center", va="bottom", weight="bold",
                bbox=dict(facecolor="white", edgecolor="red", alpha=.9, pad=2), zorder=5)

    # Đỉnh: hình theo loại, nhãn là mã đỉnh
    for v in g.vertices:
        x, y = pos[v]
        ci = comp_of.get(v, 0)
        ax.scatter(x, y, s=260, marker=KIND_STYLE[kind_of[v]][1], color=palette(ci % 10),
                   edgecolor="black", linewidth=.8, zorder=4)
        ax.annotate(code[v], (x, y), ha="center", va="center", fontsize=7,
                    color="white", weight="bold", zorder=6)
        ax.annotate(v, (x, y), xytext=(0, 13), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7,
                    bbox=dict(boxstyle="round,pad=.15", fc="white", ec="none", alpha=.7),
                    zorder=6)

    # Chú giải thành phần và tuyến đề xuất
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=palette(i % 10),
                      markeredgecolor="black", markersize=8,
                      label=f"Thành phần {i+1} ({len(c)} đỉnh)")
               for i, c in enumerate(components)]
    if suggestions:
        handles.append(Line2D([0], [0], color="red", lw=2.5, ls="--", label="Tuyến đề xuất"))
    ax.legend(handles=handles, loc="upper left", framealpha=.95, fontsize=8.5)

    # La bàn
    ax.annotate("", xy=(0.95, 0.95), xytext=(0.95, 0.85), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=2, color="black"))
    ax.text(0.95, 0.965, "N", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=13, weight="bold")

    ax.set_xlabel("Tọa độ X (km – theo dữ liệu mô phỏng)")
    ax.set_ylabel("Tọa độ Y (km – theo dữ liệu mô phỏng)")
    ax.grid(True, linestyle=":", alpha=.35)
    ax.set_aspect("equal", adjustable="datalim")

    # ---------- Cột phải: bảng dữ liệu đầu vào ----------
    ax_r.axis("off")
    ax_r.set_title("Dữ liệu đầu vào", fontsize=11, weight="bold", color="white",
                   bbox=dict(boxstyle="round,pad=0.35", fc="#3d5bb8", ec="none"))
    rows = [[f"{code[u]} – {code[v]}", f"{w:g}"] for u, v, w in g.edges]
    n_real = len(rows)
    for u, v, d, *_ in suggestions:
        rows.append([f"{code[u]} – {code[v]} (đề xuất)", f"+{d:g}"])
    if rows:
        h = min(1.0, 0.03 * (len(rows) + 1))
        tbl = ax_r.table(cellText=rows, colLabels=["Tuyến đường", "Dài (km)"],
                         cellLoc="center", bbox=[0, 1 - h, 1, h])
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(7.5)
        for (r, c), cell in tbl.get_celld().items():
            cell.set_edgecolor("#d5d9ea")
            if r == 0:
                cell.set_facecolor("#1d6f78")
                cell.set_text_props(color="white", weight="bold")
            elif r > n_real:
                cell.set_text_props(color="red")
                cell.set_facecolor("#fff4f4")
            elif r % 2 == 0:
                cell.set_facecolor("#f1f4fb")

    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output
