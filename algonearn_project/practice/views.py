import random
import time
from django.shortcuts import render
from django.http import JsonResponse
from . import practice_api

# Константы для сессии
SESSION_ARRAY = 'current_array'
SESSION_RESULTS = 'operation_results'

def practice_page(request):
    """Основная страница практики"""
    
    # Инициализация сессии
    if SESSION_ARRAY not in request.session:
        request.session[SESSION_ARRAY] = []
    if SESSION_RESULTS not in request.session:
        request.session[SESSION_RESULTS] = {
            'min': None,
            'max': None,
            'sum': None,
            'search': None,
            'sort': None
        }
    
    # Обработка POST запросов
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Генерация массива
        if action == 'generate':
            try:
                size = int(request.POST.get('size', 10))
                min_val = int(request.POST.get('min_val', 1))
                max_val = int(request.POST.get('max_val', 100))
                
                if size > 0 and min_val < max_val:
                    array = [random.randint(min_val, max_val) for _ in range(size)]
                    request.session[SESSION_ARRAY] = array
                    request.session[SESSION_RESULTS] = {
                        'min': None, 'max': None, 'sum': None, 
                        'search': None, 'sort': None
                    }
            except ValueError:
                pass
        
        # Очистка
        elif action == 'clear':
            request.session[SESSION_ARRAY] = []
            request.session[SESSION_RESULTS] = {
                'min': None, 'max': None, 'sum': None, 
                'search': None, 'sort': None
            }
        
        # Минимум
        elif action == 'min':
            array = request.session.get(SESSION_ARRAY, [])
            if array:
                request.session[SESSION_RESULTS]['min'] = min(array)
        
        # Максимум
        elif action == 'max':
            array = request.session.get(SESSION_ARRAY, [])
            if array:
                request.session[SESSION_RESULTS]['max'] = max(array)
        
        # Сумма
        elif action == 'sum':
            array = request.session.get(SESSION_ARRAY, [])
            if array:
                request.session[SESSION_RESULTS]['sum'] = sum(array)
        
        # Поиск
        elif action == 'search':
            array = request.session.get(SESSION_ARRAY, [])
            try:
                search_val = int(request.POST.get('search_value', 0))
                if array:
                    indices = [i for i, val in enumerate(array) if val == search_val]
                    if indices:
                        request.session[SESSION_RESULTS]['search'] = f"Найдено на позициях: {indices}"
                    else:
                        request.session[SESSION_RESULTS]['search'] = f"Значение {search_val} не найдено"
            except ValueError:
                pass
        
        # Сортировки
        elif action in ['bubble', 'insertion', 'quick']:
            array = request.session.get(SESSION_ARRAY, [])
            if array:
                start_time = time.time()
                
                # Вызов соответствующей сортировки
                if action == 'bubble':
                    sorted_array, metrics = practice_api.bubble_sort(array)
                elif action == 'insertion':
                    sorted_array, metrics = practice_api.insertion_sort(array)
                else:  # quick
                    sorted_array, metrics = practice_api.quick_sort(array)
                
                exec_time = (time.time() - start_time) * 1000
                
                # Сохраняем отсортированный массив
                request.session[SESSION_ARRAY] = sorted_array
                
                # Сохраняем результаты сортировки
                sort_info = practice_api.get_sort_info(action)
                request.session[SESSION_RESULTS]['sort'] = {
                    'name': sort_info['name'],
                    'comparisons': metrics.comparisons,
                    'swaps': metrics.swaps,
                    'time': round(exec_time, 2),
                    'complexity': sort_info['complexity'],
                    'description': sort_info['description'],
                    'icon': sort_info['icon'],
                    'steps': metrics.steps[-5:]  # Последние 5 шагов
                }
        
        # Сохраняем сессию
        request.session.modified = True
    
    # Подготовка контекста
    context = {
        'array': request.session.get(SESSION_ARRAY, []),
        'array_length': len(request.session.get(SESSION_ARRAY, [])),
        'results': request.session.get(SESSION_RESULTS, {}),
    }
    
    return render(request, 'practice.html', context)


def api_get_array(request):
    """API для получения текущего массива (для AJAX)"""
    return JsonResponse({
        'array': request.session.get(SESSION_ARRAY, []),
        'results': request.session.get(SESSION_RESULTS, {})
    })


def test_page(request):
    context = {}
    
    if request.method == 'POST' and request.POST.get('action') == 'submit_test':
        # Правильные ответы (индексы)
        correct_answers = [0, 1, 1, 0, 2, 0, 2, 1, 1, 1]
        
        # Собираем ответы пользователя
        user_answers = []
        for i in range(1, 11):
            user_answers.append(int(request.POST.get(f'q{i}', -1)))
        
        # Подсчет результатов
        correct_count = 0
        details = []
        
        for i, (user_ans, correct_ans) in enumerate(zip(user_answers, correct_answers)):
            is_correct = (user_ans == correct_ans)
            if is_correct:
                correct_count += 1
            
            # Буквы для ответов
            letters = ['A', 'B', 'C', 'D']
            
            details.append({
                'user_answer': letters[user_ans] if user_ans != -1 else 'Не отвечен',
                'correct_answer': letters[correct_ans],
                'is_correct': is_correct
            })
        
        # Результаты
        context['results'] = {
            'correct': correct_count,
            'incorrect': 10 - correct_count,
            'accuracy': round((correct_count / 10) * 100),
            'details': details
        }
    
    return render(request, 'test.html', context)