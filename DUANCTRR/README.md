# Đề tài 1: Kiểm tra tính liên thông của mạng lưới đường bộ kết nối các KCN

**Sinh viên - MSSV :** Ngô Minh Luân-087207006085, Lục Chấn Hưng-075207003923, Ngô Tấn Phát-072206006176, Nguyễn Minh Đức-001206001559, Trương Xuân Hùng-075207002722
**Lớp học phần:** 012012204405
**Môn học:** Cấu trúc rời rạc

## Mô tả

Chương trình mô hình hóa mạng lưới đường bộ nối các khu công nghiệp (KCN) bằng đồ thị vô hướng có trọng số (đỉnh là KCN/nút giao, cạnh là tuyến đường, trọng số là chiều dài km), sau đó:

1. Đọc dữ liệu từ file CSV và kiểm tra dữ liệu hợp lệ.
2. Duyệt đồ thị bằng BFS và DFS từ một đỉnh xuất phát.
3. Tìm các thành phần liên thông.
4. Phát hiện khu vực bị cô lập và đề xuất tuyến đường bổ sung để mạng liên thông.
5. Vẽ sơ đồ đồ thị và lưu thành ảnh.

## Cấu trúc thư mục

| File | Chức năng |
|------|-----------|
| `main.py` | Chương trình chính |
| `graph_io.py` | Đọc dữ liệu, xây dựng đồ thị |
| `traversal.py` | Thuật toán BFS, DFS |
| `components.py` | Thành phần liên thông, khu vực cô lập, đề xuất tuyến mới |
| `visualize.py` | Vẽ đồ thị |
| `data/edges.csv`, `data/nodes.csv` | Dữ liệu đầu vào |
| `ket_qua.txt` | Kết quả chạy chương trình |
| `ket_qua_do_thi.png` | Sơ đồ đồ thị |

## Cách chạy

```
pip install matplotlib networkx
python main.py
```

Chạy với file dữ liệu khác:

```
python main.py edges.csv nodes.csv
```

## Kết quả

Xem file `ket_qua.txt` và ảnh `ket_qua_do_thi.png`.