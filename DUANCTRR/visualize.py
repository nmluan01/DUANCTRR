"""Trực quan hóa đồ thị mạng lưới đường bộ và các tuyến kết nối đề xuất."""
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def draw(g, components, suggestions, output="ket_qua_do_thi.png", title="Mạng lưới đường bộ – thành phần liên thông"):
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

    # Các đỉnh thiếu tọa độ được đặt theo vòng tròn để vẫn hiển thị được.
    import math
    n = len(g.vertices)
    pos = {}
    for i, v in enumerate(g.vertices):
        if v in g.coords:
            pos[v] = g.coords[v]
        else:
            a = 2 * math.pi * i / max(n, 1)
            pos[v] = (math.cos(a) * 10, math.sin(a) * 10)

    fig, ax = plt.subplots(figsize=(15, 10))
    # Cạnh hiện có
    for u, v, w in g.edges:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        ci = comp_of.get(u, 0)
        ax.plot([x1, x2], [y1, y2], color=palette(ci % 10), lw=1.8, alpha=.75, zorder=1)
        ax.text((x1+x2)/2, (y1+y2)/2, f"{w:g}", fontsize=7, color="#333333",
                bbox=dict(facecolor="white", edgecolor="none", alpha=.7, pad=1), zorder=2)

    # Tuyến đề xuất – nét đứt đỏ
    for u, v, d, *_ in suggestions:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        ax.plot([x1, x2], [y1, y2], linestyle="--", color="red", lw=2.8, zorder=3)
        ax.text((x1+x2)/2, (y1+y2)/2, f"Đề xuất {d:g} km", fontsize=8, color="red",
                ha="center", va="bottom", bbox=dict(facecolor="white", edgecolor="red", alpha=.85, pad=2), zorder=5)

    # Đỉnh, mã số và tên
    for i, v in enumerate(g.vertices, 1):
        x, y = pos[v]
        ci = comp_of.get(v, 0)
        ax.scatter(x, y, s=105, color=palette(ci % 10), edgecolor="black", linewidth=.7, zorder=4)
        ax.annotate(f"{i}\n{v}", (x, y), xytext=(0, 9), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7.5,
                    bbox=dict(boxstyle="round,pad=.2", fc="white", ec="none", alpha=.75), zorder=6)

    # Chú giải thành phần và tuyến đề xuất
    handles = []
    for i, comp in enumerate(components):
        handles.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=palette(i % 10),
                              markeredgecolor='black', markersize=8,
                              label=f"TP liên thông {i+1} ({len(comp)} đỉnh)"))
    if suggestions:
        handles.append(Line2D([0], [0], color='red', lw=2.5, ls='--', label='Tuyến kết nối đề xuất'))
    ax.legend(handles=handles, loc="best", framealpha=.95)
    ax.set_title(title, fontsize=14, weight="bold", pad=15)
    ax.set_xlabel("Tọa độ X (km – theo dữ liệu mô phỏng)")
    ax.set_ylabel("Tọa độ Y (km – theo dữ liệu mô phỏng)")
    ax.grid(True, linestyle=":", alpha=.35)
    ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return output
