from django import forms

class ArrayForm(forms.Form):
    """Форма для генерации массива"""
    size = forms.IntegerField(
        min_value=1, 
        max_value=15, 
        initial=8,
        label='Размер массива',
        widget=forms.NumberInput(attrs={'class': 'form-input', 'id': 'array-size'})
    )
    min_val = forms.IntegerField(
        initial=1,
        label='Мин. значение',
        widget=forms.NumberInput(attrs={'class': 'form-input', 'id': 'min-value'})
    )
    max_val = forms.IntegerField(
        initial=100,
        label='Макс. значение',
        widget=forms.NumberInput(attrs={'class': 'form-input', 'id': 'max-value'})
    )

class SearchForm(forms.Form):
    """Форма для поиска элемента"""
    search_value = forms.IntegerField(
        label='Число для поиска',
        widget=forms.NumberInput(attrs={'class': 'search-input', 'id': 'search-input', 'placeholder': 'Введите число'})
    )