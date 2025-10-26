import os
import pydot

# !!! QUAN TRỌNG: Bạn hãy thay thế đường dẫn này bằng đường dẫn THỰC TẾ của thư mục 'bin' trong Graphviz trên máy bạn.
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin' 

# 1. In phiên bản pydot để xác nhận thư viện đã được cài đặt
print("pydot version:", pydot.__version__)

# 2. Tạo một đồ thị đơn giản (graph)
graph = pydot.Dot(graph_type='graph')

# 3. Thêm các node (đỉnh)
graph.add_node(pydot.Node("A"))
graph.add_node(pydot.Node("B"))

# 4. Thêm một edge (cạnh)
graph.add_edge(pydot.Edge("A", "B"))

# 5. Xuất đồ thị ra file ảnh PNG
try:
    graph.write_png("test_output.png")
    print("-------------------------------------------------------")
    print("✅ Graphviz chạy thành công, file test_output.png đã được tạo!")
    print("    -> Vui lòng kiểm tra file 'test_output.png' trong thư mục hiện tại.")
    print("-------------------------------------------------------")
except Exception as e:
    print("-------------------------------------------------------")
    print(f"❌ Xảy ra lỗi khi chạy Graphviz: {e}")
    print("    -> Vui lòng kiểm tra lại đường dẫn Graphviz/bin trong code.")
    print("-------------------------------------------------------")