import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

# Реалізація Splay Tree (спрощена версія для кешування)
class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTreeCache:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def get(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def put(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if key < self.root.key:
            node = SplayTreeNode(key, value)
            node.left = self.root.left
            node.right = self.root
            self.root.left = None
            self.root = node
        elif key > self.root.key:
            node = SplayTreeNode(key, value)
            node.right = self.root.right
            node.left = self.root
            self.root.right = None
            self.root = node
        else:
            self.root.value = value

# LRU-кешована функція
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Splay Tree кешована функція
def fibonacci_splay(n, tree):
    cached = tree.get(n)
    if cached is not None:
        return cached
    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.put(n, result)
    return result

# Порівняння
fib_values = list(range(0, 1000, 50))
lru_times = []
splay_times = []

for n in fib_values:
    # Час для LRU Cache
    time_lru = timeit.timeit(lambda: fibonacci_lru(n), number=10)
    lru_times.append(time_lru / 10)

    # Час для Splay Tree
    tree = SplayTreeCache()
    time_splay = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
    splay_times.append(time_splay / 10)

# Таблиця результатів
print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}")
print("-" * 55)
for i in range(len(fib_values)):
    print(f"{fib_values[i]:<10}{lru_times[i]:<25.8f}{splay_times[i]:.8f}")

# Побудова графіка
plt.plot(fib_values, lru_times, marker='o', label='LRU Cache')
plt.plot(fib_values, splay_times, marker='x', label='Splay Tree')
plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
plt.xlabel('Число Фібоначчі (n)')
plt.ylabel('Середній час виконання (секунди)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# Загальний висновок:
# LRU Cache — найкращий вибір для задач із повторюваними обчисленнями, такими як обрахунок чисел Фібоначчі,
# завдяки своїй простоті, низькому часу доступу й стабільній продуктивності.
#
# Splay Tree має теоретичні переваги в інших типах задач (де важливо автоматично "підтягувати" найчастіше
# використовувані елементи), але для задачі обрахунку чисел Фібоначчі вона виявилась менш ефективною.