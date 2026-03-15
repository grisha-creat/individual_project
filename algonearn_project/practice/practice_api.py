"""
Модуль с алгоритмами сортировки и подсчетом критериев
"""

class SortMetrics:
    """Класс для хранения метрик сортировки"""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.steps = []

def bubble_sort(arr):
    """Пузырьковая сортировка с подсчетом метрик"""
    metrics = SortMetrics()
    array = arr.copy()
    n = len(array)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            metrics.comparisons += 1
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                metrics.swaps += 1
                swapped = True
                metrics.steps.append(f"Обмен {array[j+1]} и {array[j]}")
        
        if not swapped:
            break
    
    return array, metrics

def insertion_sort(arr):
    """Сортировка вставками с подсчетом метрик"""
    metrics = SortMetrics()
    array = arr.copy()
    
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        
        while j >= 0:
            metrics.comparisons += 1
            if array[j] > key:
                array[j + 1] = array[j]
                metrics.swaps += 1
                j -= 1
            else:
                break
        
        if j + 1 != i:
            array[j + 1] = key
            metrics.steps.append(f"Вставка {key} на позицию {j + 1}")
    
    return array, metrics

def quick_sort(arr):
    """Быстрая сортировка с подсчетом метрик"""
    metrics = SortMetrics()
    array = arr.copy()
    
    def _quick_sort(items, low, high):
        if low < high:
            pi, _ = _partition(items, low, high)
            _quick_sort(items, low, pi - 1)
            _quick_sort(items, pi + 1, high)
    
    def _partition(items, low, high):
        pivot = items[high]
        i = low - 1
        
        for j in range(low, high):
            metrics.comparisons += 1
            if items[j] <= pivot:
                i += 1
                if i != j:
                    items[i], items[j] = items[j], items[i]
                    metrics.swaps += 1
        
        if i + 1 != high:
            items[i + 1], items[high] = items[high], items[i + 1]
            metrics.swaps += 1
        
        metrics.steps.append(f"Опорный элемент {pivot} на позиции {i + 1}")
        return i + 1, metrics
    
    _quick_sort(array, 0, len(array) - 1)
    return array, metrics

def get_sort_info(sort_type):
    """Получить информацию о типе сортировки"""
    sort_info = {
        'bubble': {
            'name': 'Пузырьковая сортировка',
            'complexity': 'O(n²)',
            'description': 'Простой алгоритм, сравнивает соседние элементы и меняет их местами',
            'icon': '🫧'
        },
        'insertion': {
            'name': 'Сортировка вставками',
            'complexity': 'O(n²)',
            'description': 'Строит отсортированный массив, вставляя элементы в правильную позицию',
            'icon': '📌'
        },
        'quick': {
            'name': 'Быстрая сортировка',
            'complexity': 'O(n log n)',
            'description': 'Разделяет массив на подмассивы относительно опорного элемента',
            'icon': '⚡'
        }
    }
    return sort_info.get(sort_type, {})