from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    
    # Настройки
    email_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def add_experience(self, amount):
        """Добавление опыта пользователю"""
        self.experience += amount
        # Каждые 100 опыта = 1 уровень
        new_level = self.experience // 100 + 1
        if new_level > self.level:
            self.level = new_level
            # Можно добавить уведомление о новом уровне
        self.save()
    
    def add_points(self, amount):
        """Добавление очков"""
        self.points += amount
        self.save()
    
    @property
    def progress_percentage(self):
        """Процент до следующего уровня"""
        current_level_exp = self.experience % 100
        return current_level_exp

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматическое создание профиля при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля при сохранении пользователя"""
    instance.profile.save()


# class UserProgress(models.Model):
    # """Прогресс пользователя по урокам"""
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    # lesson = models.ForeignKey('learn.Lesson', on_delete=models.CASCADE)
    # completed = models.BooleanField(default=False)
    # completed_at = models.DateTimeField(null=True, blank=True)
    # score = models.IntegerField(default=0)
#     attempts = models.IntegerField(default=0)
    # time_spent = models.IntegerField(default=0)  # в секундах
    
    # class Meta:
        # unique_together = ['user', 'lesson']
        # ordering = ['-completed_at']
    # 
    # def __str__(self):
        # status = "✓" if self.completed else "✗"
        # return f"{self.user.username} - {self.lesson.title} [{status}]"
    
    # def mark_completed(self, score=100):
        # """Отметить урок как пройденный"""
        # from django.utils import timezone
        
        # if not self.completed:
            # self.completed = True
            # self.completed_at = timezone.now()
            # self.score = score
            # self.save()
            
            # Начисляем очки и опыт
            # self.user.profile.add_points(score // 10)
            # self.user.profile.add_experience(score // 20)
            
            # return True
        # return False


class Achievement(models.Model):
    """Достижения пользователей"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    points_reward = models.IntegerField(default=100)
    condition = models.CharField(max_length=200)  # Описание условия
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Достижения, полученные пользователем"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"