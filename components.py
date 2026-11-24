"""
[THÀNH VIÊN 3] Xác định thành phần liên thông, khoanh vùng khu vực cô lập 
và đề xuất tuyến đường bổ sung dựa trên khoảng cách Euclid.
"""
from traversal import bfs, dfs_iterative
import math

def find_components(g, method="bfs"):
    if method not in ("bfs", "dfs"):
        raise ValueError("method phải là 'bfs' hoặc 'dfs'")
    algo = bfs if method == "bfs" else dfs_iterative

    visited = set()
    components = []

    # Duyệt qua từng đỉnh trong đồ thị
    for u in g.vertices:
        if u not in visited:
            order, _ = algo(g, u)
            visited.update(order)
            components.append(sorted(order))

    # Sắp xếp các thành phần theo số lượng đỉnh giảm dần
    components.sort(key=len, reverse=True)
    return components

def isolated_areas(components):
    """
    Xác định các khu vực bị cô lập (các thành phần liên thông ngoài thành phần lớn nhất).
    """
    if len(components) <= 1:
        return []
    return components[1:] # Trả về từ thành phần thứ 2 trở đi

def suggest_links(g, components):
    """
    Đề xuất tuyến đường ngắn nhất (khoảng cách Euclid) từ các cụm cô lập về mạng chính.
    Trả về danh sách các tuple: (dinh_mang_chinh, dinh_cum_co_lap, khoang_cach, toan_bo_cum_co_lap)
    """
    if len(components) <= 1:
        return []
        
    main_comp = set(components[0])
    suggestions = []
    
    for comp in components[1:]:
        min_dist = float('inf')
        best_pair = (None, None)
        
        # Tìm cặp đỉnh (u thuộc mạng chính, v thuộc cụm cô lập) có khoảng cách gần nhất
        for u in main_comp:
            if u not in g.coords:
                continue
            x1, y1 = g.coords[u]
            
            for v in comp:
                if v not in g.coords:
                    continue
                x2, y2 = g.coords[v]
                
                dist = math.hypot(x1 - x2, y1 - y2) # Khoảng cách Euclid
                if dist < min_dist:
                    min_dist = dist
                    best_pair = (u, v)
                    
        if best_pair[0] and best_pair[1]:
            suggestions.append((best_pair[0], best_pair[1], round(min_dist, 1), comp))
            
    return suggestions