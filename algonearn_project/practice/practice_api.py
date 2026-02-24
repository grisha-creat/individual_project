import random

def generate_array(size, min_val=1, max_val=100):
    """Генерирует случайный массив"""
    return [random.randint(min_val, max_val) for _ in range(size)]

def find_min(arr):
    """Находит минимальный элемент и его индексы"""
    if not arr:
        return None, []
    min_val = min(arr)
    indices = [i for i, val in enumerate(arr) if val == min_val]
    return min_val, indices

def find_max(arr):
    """Находит максимальный элемент и его индексы"""
    if not arr:
        return None, []
    max_val = max(arr)
    indices = [i for i, val in enumerate(arr) if val == max_val]
    return max_val, indices

def find_sum(arr):
    """Находит сумму элементов"""
    return sum(arr) if arr else 0

def search_element(arr, target):
    """Ищет элемент в массиве, возвращает индексы вхождений"""
    if not arr:
        return []
    return [i for i, val in enumerate(arr) if val == target]