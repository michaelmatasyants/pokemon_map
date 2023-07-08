from django.db import models
from django.utils.timezone import localtime


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название:',
                             max_length=200)
    title_en = models.CharField(verbose_name='Название на английском:',
                                max_length=200,
                                blank=True)
    title_jp = models.CharField(verbose_name='Название на японском:',
                                max_length=200,
                                blank=True)
    description = models.TextField(verbose_name='Описание:',
                                   blank=True)
    next_evolution = models.ForeignKey("self",
                                       verbose_name='В кого эволюционирует',
                                       null=True,
                                       blank=True,
                                       related_name="previous_evolutions",
                                       on_delete=models.SET_NULL)
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='',
                              null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                verbose_name='Покемон',
                                related_name='entities',
                                on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился',
                                       null=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчез',
                                          null=True)
    level = models.IntegerField(verbose_name='Уровень',
                                null=True)
    health = models.IntegerField(verbose_name='Здоровье',
                                 null=True)
    strength = models.IntegerField(verbose_name='Сила',
                                   null=True)
    defence = models.IntegerField(verbose_name='Защита',
                                  null=True)
    stamina = models.IntegerField(verbose_name='Выносливость',
                                  null=True)

    def __str__(self):
        return f"{self.pokemon} Широта: {self.lat} Долгота: {self.lon}"
