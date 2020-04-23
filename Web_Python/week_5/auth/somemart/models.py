from django.db import models


class Item(models.Model):
    """Модель товара."""
    title = models.CharField(max_length=64, verbose_name='Название')
    description = models.CharField(max_length=1024, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Оценка')


class Review(models.Model):
    """Модель отзыва о товаре."""
    grade = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=1024)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
