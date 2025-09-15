from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='applications/', verbose_name='Изображение', blank=True, null=True)
    image_design = models.ImageField(upload_to='designs/', verbose_name='Дизайн', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    def set_in_progress(self):
        self.status = 'in_progress'
        self.save()

    def set_completed(self):
        self.status = 'completed'
        self.save()

    def can_change_status(self, user):
        return True

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']