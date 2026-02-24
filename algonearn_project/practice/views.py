from django.shortcuts import render
from .forms import ArrayForm, SearchForm
from . import practice_api  # ← импортируем наш файл

def practice_page(request):
    # Инициализация
    current_array = []
    
    # Получаем массив из сессии
    if 'current_array' in request.session:
        current_array = request.session['current_array']
    else:
        current_array = [64, 34, 25, 12, 22, 11, 90]
        request.session['current_array'] = current_array
    
    # Обработка форм
    array_form = ArrayForm(request.POST or None)
    search_form = SearchForm(request.POST or None)
    
    if request.method == 'POST':
        # Генерация нового массива
        if 'generate' in request.POST and array_form.is_valid():
            size = array_form.cleaned_data['size']
            min_val = array_form.cleaned_data['min_val']
            max_val = array_form.cleaned_data['max_val']
            # Используем функцию из practice_api
            current_array = practice_api.generate_array(size, min_val, max_val)
            request.session['current_array'] = current_array
        
        # Поиск минимума
        elif 'find_min' in request.POST:
            if current_array:
                min_val, indices = practice_api.find_min(current_array)
                request.session['min_result'] = min_val
                request.session['highlight_indices'] = indices
                request.session['highlight_type'] = 'min'
        
        # Поиск максимума
        elif 'find_max' in request.POST:
            if current_array:
                max_val, indices = practice_api.find_max(current_array)
                request.session['max_result'] = max_val
                request.session['highlight_indices'] = indices
                request.session['highlight_type'] = 'max'
        
        # Сумма
        elif 'find_sum' in request.POST:
            if current_array:
                sum_val = practice_api.find_sum(current_array)
                request.session['sum_result'] = sum_val
        
        # Поиск элемента
        elif 'search' in request.POST and search_form.is_valid():
            if current_array:
                search_value = search_form.cleaned_data['search_value']
                indices = practice_api.search_element(current_array, search_value)
                if indices:
                    request.session['search_result'] = f"Элемент {search_value} найден на позициях: {indices}"
                    request.session['highlight_indices'] = indices
                    request.session['highlight_type'] = 'search'
                else:
                    request.session['search_result'] = f"Элемент {search_value} не найден"
    
    context = {
        'array_form': array_form,
        'search_form': search_form,
        'current_array': current_array,
        'min_result': request.session.get('min_result'),
        'max_result': request.session.get('max_result'),
        'sum_result': request.session.get('sum_result'),
        'search_result': request.session.get('search_result'),
        'highlight_indices': request.session.get('highlight_indices', []),
        'highlight_type': request.session.get('highlight_type'),
        'array_length': len(current_array),
    }
    
    return render(request, 'practice.html', context)