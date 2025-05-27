from collections import deque
import time

class BodyArray:
    def __init__(self, matrix):
        self.matrix = [row[:] for row in matrix]
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
    
    def calculate_water_volume_a(self):
        if self.rows < 3 or self.cols < 3:
            return 0
        
        # Вода остается только во внутренних углублениях
        water_volume = 0
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                min_neighbor = min(
                    self.matrix[i-1][j],
                    self.matrix[i+1][j],
                    self.matrix[i][j-1],
                    self.matrix[i][j+1]
                )
                if self.matrix[i][j] < min_neighbor:
                    water_volume += min_neighbor - self.matrix[i][j]
        return water_volume
    
    def pour_water_b(self, i0, j0, V):
        if not (0 <= i0 < self.rows and 0 <= j0 < self.cols):
            return
        
        while V > 0:
            queue = [(i0, j0)]
            visited = set()
            filled = set()
            min_height = self.matrix[i0][j0]
            
            # Находим все точки с текущей минимальной высотой
            while queue:
                i, j = queue.pop(0)
                if (i, j) in visited:
                    continue
                visited.add((i, j))
                
                if self.matrix[i][j] == min_height:
                    filled.add((i, j))
                    # Добавляем соседей
                    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.rows and 0 <= nj < self.cols:
                            queue.append((ni, nj))
                elif self.matrix[i][j] > min_height:
                    pass
            
            if not filled:
                break
                
            # Находим следующую минимальную высоту среди соседей
            next_height = float('inf')
            for i, j in filled:
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols and (ni, nj) not in filled:
                        if self.matrix[ni][nj] > min_height:
                            next_height = min(next_height, self.matrix[ni][nj])
            
            if next_height == float('inf'):
                # Можно заполнить до бесконечности
                delta_h = V / len(filled)
                for i, j in filled:
                    self.matrix[i][j] += delta_h
                V = 0
            else:
                delta_h = next_height - min_height
                max_possible = delta_h * len(filled)
                if V >= max_possible:
                    for i, j in filled:
                        self.matrix[i][j] = next_height
                    V -= max_possible
                else:
                    delta_h = V / len(filled)
                    for i, j in filled:
                        self.matrix[i][j] += delta_h
                    V = 0
class Node:
    def __init__(self, i, j, height):
        self.i = i
        self.j = j
        self.height = height
        self.neighbors = []
    
    def add_neighbor(self, node):
        self.neighbors.append(node)

class BodyLinkedList:
    def __init__(self, matrix):
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
        self.nodes = []
        
        # Создаем узлы
        nodes_matrix = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                node = Node(i, j, matrix[i][j])
                row.append(node)
            nodes_matrix.append(row)
        
        # Устанавливаем связи между соседями
        for i in range(self.rows):
            for j in range(self.cols):
                node = nodes_matrix[i][j]
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        node.add_neighbor(nodes_matrix[ni][nj])
        
        self.nodes_matrix = nodes_matrix
    
    def calculate_water_volume_a(self):
        if self.rows < 3 or self.cols < 3:
            return 0
        
        water_volume = 0
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                node = self.nodes_matrix[i][j]
                min_neighbor = min(n.height for n in node.neighbors)
                if node.height < min_neighbor:
                    water_volume += min_neighbor - node.height
        return water_volume
    
    def pour_water_b(self, i0, j0, V):
        if not (0 <= i0 < self.rows and 0 <= j0 < self.cols):
            return
        
        node = self.nodes_matrix[i0][j0]
        
        while V > 0:
            queue = [node]
            visited = set()
            filled = set()
            min_height = node.height
            
            # Находим все точки с текущей минимальной высотой
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                
                if current.height == min_height:
                    filled.add(current)
                    # Добавляем соседей
                    for neighbor in current.neighbors:
                        queue.append(neighbor)
                elif current.height > min_height:
                    pass
            
            if not filled:
                break
                
            # Находим следующую минимальную высоту среди соседей
            next_height = float('inf')
            for current in filled:
                for neighbor in current.neighbors:
                    if neighbor not in filled and neighbor.height > min_height:
                        next_height = min(next_height, neighbor.height)
            
            if next_height == float('inf'):
                # Можно заполнить до бесконечности
                delta_h = V / len(filled)
                for current in filled:
                    current.height += delta_h
                V = 0
            else:
                delta_h = next_height - min_height
                max_possible = delta_h * len(filled)
                if V >= max_possible:
                    for current in filled:
                        current.height = next_height
                    V -= max_possible
                else:
                    delta_h = V / len(filled)
                    for current in filled:
                        current.height += delta_h
                    V = 0
                  
class BodySTL:
    def __init__(self, matrix):
        self.matrix = [row[:] for row in matrix]
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
    
    def calculate_water_volume_a(self):
        if self.rows < 3 or self.cols < 3:
            return 0
        
        water_volume = 0
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                min_neighbor = min(
                    self.matrix[i-1][j],
                    self.matrix[i+1][j],
                    self.matrix[i][j-1],
                    self.matrix[i][j+1]
                )
                if self.matrix[i][j] < min_neighbor:
                    water_volume += min_neighbor - self.matrix[i][j]
        return water_volume
    
    def pour_water_b(self, i0, j0, V):
        if not (0 <= i0 < self.rows and 0 <= j0 < self.cols):
            return
        
        while V > 0:
            queue = deque([(i0, j0)])
            visited = set()
            filled = set()
            min_height = self.matrix[i0][j0]
            
            # Находим все точки с текущей минимальной высотой
            while queue:
                i, j = queue.popleft()
                if (i, j) in visited:
                    continue
                visited.add((i, j))
                
                if self.matrix[i][j] == min_height:
                    filled.add((i, j))
                    # Добавляем соседей
                    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.rows and 0 <= nj < self.cols:
                            queue.append((ni, nj))
                elif self.matrix[i][j] > min_height:
                    pass
            
            if not filled:
                break
                
            # Находим следующую минимальную высоту среди соседей
            next_height = float('inf')
            for i, j in filled:
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols and (ni, nj) not in filled:
                        if self.matrix[ni][nj] > min_height:
                            next_height = min(next_height, self.matrix[ni][nj])
            
            if next_height == float('inf'):
                # Можно заполнить до бесконечности
                delta_h = V / len(filled)
                for i, j in filled:
                    self.matrix[i][j] += delta_h
                V = 0
            else:
                delta_h = next_height - min_height
                max_possible = delta_h * len(filled)
                if V >= max_possible:
                    for i, j in filled:
                        self.matrix[i][j] = next_height
                    V -= max_possible
                else:
                    delta_h = V / len(filled)
                    for i, j in filled:
                        self.matrix[i][j] += delta_h
                    V = 0


def test_implementations():
    # Тестовая матрица
    matrix = [
        [3, 3, 3, 3, 3],
        [3, 1, 2, 1, 3],
        [3, 2, 1, 2, 3],
        [3, 1, 2, 1, 3],
        [3, 3, 3, 3, 3]
    ]
    
    # Создаем экземпляры каждой реализации
    array_impl = BodyArray(matrix)
    linked_list_impl = BodyLinkedList(matrix)
    stl_impl = BodySTL(matrix)
    
    # Тестируем часть a)
    print("Testing part a)...")
    start = time.time()
    vol_a = array_impl.calculate_water_volume_a()
    array_time = time.time() - start
    
    start = time.time()
    vol_b = linked_list_impl.calculate_water_volume_a()
    linked_list_time = time.time() - start
    
    start = time.time()
    vol_c = stl_impl.calculate_water_volume_a()
    stl_time = time.time() - start
    
    print(f"Array: volume = {vol_a}, time = {array_time:.6f}s")
    print(f"Linked List: volume = {vol_b}, time = {linked_list_time:.6f}s")
    print(f"STL: volume = {vol_c}, time = {stl_time:.6f}s")
    
    # Тестируем часть b)
    print("\nTesting part b)...")
    V = 5.0
    i0, j0 = 2, 2
    
    start = time.time()
    array_impl.pour_water_b(i0, j0, V)
    array_time = time.time() - start
    
    start = time.time()
    linked_list_impl.pour_water_b(i0, j0, V)
    linked_list_time = time.time() - start
    
    start = time.time()
    stl_impl.pour_water_b(i0, j0, V)
    stl_time = time.time() - start
    
    print(f"Array: time = {array_time:.6f}s")
    print(f"Linked List: time = {linked_list_time:.6f}s")
    print(f"STL: time = {stl_time:.6f}s")

if __name__ == "__main__":
    test_implementations()
