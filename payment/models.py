from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=80, verbose_name="Наименование", blank=True)
    price = models.PositiveIntegerField(verbose_name="Цена")

    def __str__(self):
        return self.title
