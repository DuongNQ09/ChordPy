import hashlib

# Kích thước không gian định danh
M = 6
ID_SPACE = 2 ** M

# Hàm băm ánh xạ chuỗi vào không gian định danh
def hash_key(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % ID_SPACE

# Lớp Node đại diện cho một nút trong vòng Chord
class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.finger_table = [None] * M
        self.successor = None

    # Tìm successor cho một định danh bất kỳ
    def find_successor(self, key_id, nodes):
        sorted_nodes = sorted(nodes, key=lambda n: n.id)
        for node in sorted_nodes:
            if node.id >= key_id:
                return node
        return sorted_nodes[0]

    # Xây dựng finger table cho nút hiện tại
    def build_finger_table(self, nodes):
        for i in range(M):
            start = (self.id + 2 ** i) % ID_SPACE
            self.finger_table[i] = self.find_successor(start, nodes)

# Tạo vòng Chord từ danh sách node ID
def create_chord_ring(node_ids):
    nodes = [Node(nid) for nid in node_ids]
    for node in nodes:
        node.successor = node.find_successor((node.id + 1) % ID_SPACE, nodes)
        node.build_finger_table(nodes)
    return nodes


# Test case
node_ids = [10, 22, 38, 45, 60]
nodes = create_chord_ring(node_ids)

# ID của khóa
key = "word"
key_id = hash_key(key)
responsible_node = nodes[0].find_successor(key_id, nodes)

print(f"Key '{key}' có ID = {key_id}")
print(f"Nút chịu trách nhiệm: Node {responsible_node.id}")

# Finger table
for node in nodes:
    print(f"\nNode {node.id} Finger Table:")
    for i in range(M):
        entry = (node.id + 2 ** i) % ID_SPACE
        target = node.finger_table[i].id
        print(f"  Start: {entry} → Node {target}")