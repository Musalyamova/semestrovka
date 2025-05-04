import random
import os
import time
import matplotlib.pyplot as plt


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def tree_sort(arr):
    iterations = [0]  # Используем список для mutable counter

    def insert(root, value):
        node = TreeNode(value)
        current = root
        while True:
            iterations[0] += 1
            if value < current.value:
                if current.left is None:
                    current.left = node
                    break
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = node
                    break
                else:
                    current = current.right
        return root

    def in_order_traversal(root):
        result = []
        stack = []
        current = root
        while True:
            if current is not None:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                result.append(current.value)
                current = current.right
            else:
                break
        return result

    if not arr:
        return [], 0

    root = TreeNode(arr[0])
    for item in arr[1:]:
        insert(root, item)

    sorted_arr = in_order_traversal(root)
    return sorted_arr, iterations[0]


def generate_data():
    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    for size in sizes:
        random_data = [random.randint(0, 10000) for _ in range(size)]
        sorted_data = sorted(random_data)
        reverse_sorted = sorted(random_data, reverse=True)

        with open(f'datasets/random_{size}.txt', 'w') as f:
            f.write(','.join(map(str, random_data)))
        with open(f'datasets/sorted_{size}.txt', 'w') as f:
            f.write(','.join(map(str, sorted_data)))
        with open(f'datasets/reverse_sorted_{size}.txt', 'w') as f:
            f.write(','.join(map(str, reverse_sorted)))


def load_dataset(filename):
    with open(f'datasets/{filename}', 'r') as f:
        return list(map(int, f.read().split(',')))


def measure_performance():
    results = []
    files = os.listdir('datasets')
    sizes = sorted(list({int(f.split('_')[-1].split('.')[0]) for f in files}))

    for size in sizes:
        for data_type in ['random', 'sorted', 'reverse_sorted']:
            filename = f"{data_type}_{size}.txt"
            if filename not in files:
                continue

            data = load_dataset(filename)

            start_time = time.perf_counter()
            _, iterations = tree_sort(data.copy())
            end_time = time.perf_counter()

            results.append({
                'size': size,
                'type': data_type,
                'time': end_time - start_time,
                'iterations': iterations
            })

            print(f"Size: {size}, Type: {data_type}, Time: {end_time - start_time:.6f}s, Iterations: {iterations}")

    return results


def draw_plots(results):
    if not results:
        print("Нет данных для построения графиков")
        return

    plt.figure(figsize=(14, 6))

    # График времени выполнения
    plt.subplot(1, 2, 1)
    for data_type in ['random', 'sorted', 'reverse_sorted']:
        type_data = [r for r in results if r['type'] == data_type]
        if not type_data:
            continue
        plt.plot([r['size'] for r in type_data],
                 [r['time'] * 1000 for r in type_data],
                 label=data_type)
    plt.xlabel('Размер массива')
    plt.ylabel('Время (мс)')
    plt.title('Время выполнения Tree Sort')
    plt.legend()
    plt.grid(True)

    # График итераций
    plt.subplot(1, 2, 2)
    for data_type in ['random', 'sorted', 'reverse_sorted']:
        type_data = [r for r in results if r['type'] == data_type]
        if not type_data:
            continue
        plt.plot([r['size'] for r in type_data],
                 [r['iterations'] for r in type_data],
                 label=data_type)
    plt.xlabel('Размер массива')
    plt.ylabel('Количество итераций')
    plt.title('Сложность Tree Sort')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    if not os.path.exists('datasets'):
        print("Генерация тестовых данных...")
        generate_data()

    print("Измерение производительности...")
    results = measure_performance()

    print("Построение графиков...")
    draw_plots(results)


if __name__ == '__main__':
    main()