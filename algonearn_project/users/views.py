from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile,  UserAchievement
# from.models UserProgress,
# from learn.models import Lesson

class RegisterView(CreateView):
    """Регистрация пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/auth.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматический вход после регистрации
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        
        messages.success(self.request, 
            f'Добро пожаловать, {username}! Ваш аккаунт создан.')
        return response

class CustomLoginView(LoginView):
    """Кастомизированный вход"""
    template_name = 'users/auth.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, 
            f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    """Кастомизированный выход"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    """Просмотр профиля"""
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Прогресс пользователя
        completed_lessons = UserProgress.objects.filter(
            user=user, completed=True
        ).count()
        total_lessons = Lesson.objects.count()
        
        context.update({
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'progress_percentage': (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0,
            'recent_progress': UserProgress.objects.filter(user=user).order_by('-completed_at')[:5],
            'achievements': UserAchievement.objects.filter(user=user),
            'user_progress': UserProgress.objects.filter(user=user),
        })
        return context

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    """Редактирование профиля"""
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserUpdateForm(
                self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        
        if user_form.is_valid():
            user_form.save()
            messages.success(self.request, 'Профиль успешно обновлен!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def mark_lesson_completed(request, lesson_id):
    """Отметить урок как пройденный"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': False}
    )
    
    if progress.mark_completed():
        messages.success(request, f'Урок "{lesson.title}" отмечен как пройденный!')
        
        # Проверяем достижения
        check_achievements(request.user)
    else:
        messages.info(request, f'Вы уже прошли урок "{lesson.title}"')
    
    return redirect('lesson_detail', pk=lesson_id)

def check_achievements(user):
    """Проверка и выдача достижений"""
    from .models import Achievement, UserAchievement
    
    achievements = Achievement.objects.all()
    for achievement in achievements:
        if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            # Здесь можно добавить логику проверки условий
            # Например, если пройдено 5 уроков
            completed_count = UserProgress.objects.filter(user=user, completed=True).count()
            if completed_count >= 5:
                UserAchievement.objects.create(user=user, achievement=achievement)