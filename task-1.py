import time
import random
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def range_sum_no_cache(array, left, right):
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache: LRUCache):
    key = (left, right)
    cached = cache.get(key)
    if cached != -1:
        return cached
    result = sum(array[left:right + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value, cache: LRUCache):
    array[index] = value
    # інвалідуємо всі ключі, що містять index
    keys_to_delete = [key for key in cache.cache if key[0] <= index <= key[1]]
    for key in keys_to_delete:
        del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


def run_without_cache(array, queries):
    for query in queries:
        if query[0] == "Range":
            _, l, r = query
            range_sum_no_cache(array, l, r)
        elif query[0] == "Update":
            _, i, v = query
            update_no_cache(array, i, v)


def run_with_cache(array, queries):
    cache = LRUCache(capacity=1000)
    for query in queries:
        if query[0] == "Range":
            _, l, r = query
            range_sum_with_cache(array, l, r, cache)
        elif query[0] == "Update":
            _, i, v = query
            update_with_cache(array, i, v, cache)


if __name__ == "__main__":
    n = 100_000
    q = 50_000

    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    # Без кешу
    array_no_cache = array.copy()
    start = time.time()
    run_without_cache(array_no_cache, queries)
    no_cache_time = time.time() - start

    # З кешем
    array_with_cache = array.copy()
    start = time.time()
    run_with_cache(array_with_cache, queries)
    with_cache_time = time.time() - start

    # Виведення результатів
    print(f"Без кешу :  {no_cache_time:.2f} c")
    print(f"LRU-кеш  :  {with_cache_time:.2f} c  (прискорення ×{no_cache_time / with_cache_time:.2f})")
