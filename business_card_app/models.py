from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class BusinessCard(models.Model):
    """
    Модель визитка
    объединены данные работника и компании все данные не проверяются на корректность только проверка на типы данных
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                                related_name='business_card')
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия', blank=True)
    patronymic = models.CharField(max_length=255, blank=True, verbose_name='Отчество')
    work_email = models.EmailField(verbose_name='Рабочая почта')
    position = models.CharField(max_length=200, verbose_name='Должность')

    company_name = models.TextField(verbose_name='Название компании', blank=True)
    field_of_activity = models.CharField(max_length=255, verbose_name='Сфеера деятельности', blank=True)
    city = models.CharField(max_length=255, verbose_name='Город', blank=True)
    address = models.TextField(verbose_name='Адрес', blank=True)
    short_description = models.TextField(verbose_name='Краткая информация о компании', blank=True)
    site = models.URLField(verbose_name='Сайт', blank=True)

    # favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Избранные', related_name='favorite')
    registration = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Визитка'
        verbose_name_plural = 'Визитки'
        ordering = ('user', '-registration')

    def __str__(self):
        return f'{self.user.username}'


class Telephone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Работник',
                             related_name='telephone')
    telephone = models.CharField(max_length=15, verbose_name='Номер телефона')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        ordering = ('user', '-add_date',)

    def __str__(self):
        return f'{self.user} {self.telephone}'


class Social(models.Model):
    """
    Социальные сети
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    url = models.URLField(verbose_name='Базовая ссылка')
    icon = models.CharField(max_length=255, verbose_name='Иконка')

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class SocialNetworks(models.Model):
    """
    Социальные сети работников
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Работник',
                             related_name='social_networks')
    social = models.ForeignKey(Social, on_delete=models.SET_NULL, null=True, verbose_name="Социальная сеть")
    username = models.CharField(max_length=15, verbose_name='Ник в соц сети')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Социальная сеть работника'
        verbose_name_plural = 'Социальные сети работников'
        ordering = ('user', '-add_date',)

    def __str__(self):
        return f'{self.user} {self.social}'


#


class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follow {self.user_to}'


User.add_to_class('following', models.ManyToManyField('self',
                                                      through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))
