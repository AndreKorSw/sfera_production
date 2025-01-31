from autoslug.fields import AutoSlugField
# from django_extensions.db.fields import AutoSlugField
# from django_autoslug.fields import AutoSlugField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
# from .utils import stations
stations = (
    ("Академическая", "Академическая"),
    ("Александровский сад", "Александровский сад"),
    ("Алтуфьево", "Алтуфьево"),
    ("Арбатская", "Арбатская"),
    ("Баррикадная", "Баррикадная"),
    ("Белорусская", "Белорусская"),
    ("Библиотека имени Ленина", "Библиотека имени Ленина"),
    ("Борисово", "Борисово"),
    ("Ботанический сад", "Ботанический сад"),
    ("Варшавская", "Варшавская"),
    ("ВДНХ", "ВДНХ"),
    ("Владыкино", "Владыкино"),
    ("Волжская", "Волжская"),
    ("Воробьёвы горы", "Воробьёвы горы"),
    ("Деловой центр", "Деловой центр"),
    ("Дмитровская", "Дмитровская"),
    ("Дубровка", "Дубровка"),
    ("Европейская", "Европейская"),
    ("Жулебино", "Жулебино"),
    ("Зеленоградская", "Зеленоградская"),
    ("Зябликово", "Зябликово"),
    ("Калужская", "Калужская"),
    ("Киевская", "Киевская"),
    ("Китай-город", "Китай-город"),
    ("Киностудия имени Горького", "Киностудия имени Горького"),
    ("Кожуховская", "Кожуховская"),
    ("Коломенская", "Коломенская"),
    ("Коньково", "Коньково"),
    ("Краснопресненская", "Краснопресненская"),
    ("Краснополянская", "Краснополянская"),
    ("Кубинка", "Кубинка"),
    ("Кузнецкий мост", "Кузнецкий мост"),
    ("Кутузовская", "Кутузовская"),
    ("Ленинский проспект", "Ленинский проспект"),
    ("Лубянка", "Лубянка"),
    ("Маяковская", "Маяковская"),
    ("Медведково", "Медведково"),
    ("Москва-сити", "Москва-сити"),
    ("Митино", "Митино"),
    ("Мытищи", "Мытищи"),
    ("Нагорная", "Нагорная"),
    ("Нагатинская", "Нагатинская"),
    ("Наливная", "Наливная"),
    ("Нижегородская", "Нижегородская"),
    ("Новогиреево", "Новогиреево"),
    ("Новокосино", "Новокосино"),
    ("Новоясеневская", "Новоясеневская"),
    ("Октябрьская", "Октябрьская"),
    ("Озерная", "Озерная"),
    ("Орехово", "Орехово"),
    ("Павелецкая", "Павелецкая"),
    ("Панфиловская", "Панфиловская"),
    ("Печерская", "Печерская"),
    ("Планерная", "Планерная"),
    ("Площадь Революции", "Площадь Революции"),
    ("Пушкинская", "Пушкинская"),
    ("Раменки", "Раменки"),
    ("Рижская", "Рижская"),
    ("Румянцево", "Румянцево"),
    ("Савеловская", "Савеловская"),
    ("Семеновская", "Семеновская"),
    ("Серпуховская", "Серпуховская"),
    ("Скобелевская", "Скобелевская"),
    ("Славянский бульвар", "Славянский бульвар"),
    ("Смоленская", "Смоленская"),
    ("Сокол", "Сокол"),
    ("Старокачаловская", "Старокачаловская"),
    ("Студенческая", "Студенческая"),
    ("Таганская", "Таганская"),
    ("Тверская", "Тверская"),
    ("Тимирязевская", "Тимирязевская"),
    ("Тульская", "Тульская"),
    ("Улица 1905 года", "Улица 1905 года"),
    ("Удальцова", "Удальцова"),
    ("Ульяновская", "Ульяновская"),
    ("Фрунзенская", "Фрунзенская"),
    ("Хорошёво", "Хорошёво"),
    ("ЦДК", "ЦДК"),
    ("Черкизовская", "Черкизовская"),
    ("Чистые пруды", "Чистые пруды"),
    ("Шаболовская", "Шаболовская"),
    ("Шелепиха", "Шелепиха"),
    ("Щелковская", "Щелковская"),
    ("Электрозаводская", "Электрозаводская"),
    ("Юго-Западная", "Юго-Западная"),
    ("Южная", "Южная"),
    ("Ясенево", "Ясенево"),

    # Станции МЦК
    ("Киевская", "Киевская"),
    ("Кунцевская", "Кунцевская"),
    ("Славянский бульвар", "Славянский бульвар"),
    ("Студенческая", "Студенческая"),
    ("Шелепиха", "Шелепиха"),
    ("Лужники", "Лужники"),
    ("Кропоткинская", "Кропоткинская"),
    ("Краснопресненская", "Краснопресненская"),
    ("Звенигородская", "Звенигородская"),
    ("Каширская", "Каширская"),
    ("Таганская", "Таганская"),
    ("Нагорная", "Нагорная"),
    ("Фрунзенская", "Фрунзенская"),
)
events_options = (
    ("FIRE_FUN", "FIRE_FUN"),
    ("FOR_LIFE", "FOR_LIFE"),
)
class CompanyPost(models.Model):
    title = models.CharField(max_length=40, db_index=True, verbose_name="Заголовок")
    address = models.CharField(max_length=50, db_index=True, verbose_name="Aдрес")
    metro = models.CharField(max_length=255, choices=stations, verbose_name="Станция метро")
    latitude = models.FloatField(max_length=255, db_index=True, verbose_name="Широта")
    longitude = models.FloatField(max_length=255, db_index=True, verbose_name="Долгота")
    company_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Название компании")
    # slug = models.SlugField(unique=True, db_index=True, verbose_name="Ссылка")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, verbose_name="Ссылка")
    phone = PhoneNumberField(blank=False,verbose_name="Телефон")
    photo = models.ImageField(upload_to='photos/posts/%Y/%m/%d/', blank=False, verbose_name="Главное фото")
    pic_1 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/', blank=True, verbose_name="Фото")
    pic_2 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/', blank=True, verbose_name="Фото")
    pic_3 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/', blank=True, verbose_name="Фото")
    content = models.TextField(verbose_name="Контент")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='favourites', verbose_name='Избранное')
    cat = models.ForeignKey('Categories', on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        verbose_name = 'Заведение компаний'
        verbose_name_plural = 'Заведения компаний'


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_slug': self.slug})


class CompanyNews(models.Model):
    title = models.CharField(max_length=40, db_index=True, verbose_name="Заголовок")
    # address = models.CharField(max_length=255, db_index=True, verbose_name="Aдрес")
    company_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Название компании")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, verbose_name="Ссылка")
    # slug = models.SlugField(unique=True, db_index=True, verbose_name="Ссылка")
    # phone = PhoneNumberField(null=True, blank=False, verbose_name="Телефон")
    photo = models.ImageField(upload_to='photos/news/%Y/%m/%d/', blank=False, verbose_name="Фото")
    content = models.TextField(verbose_name="Контент")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='blog_posts')
    class Meta:
        verbose_name = 'Посты от компаний и пользователей'
        verbose_name_plural = "Посты от компаний и пользователей"

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()



    def get_absolute_url(self):
        return reverse('show_new', kwargs={'new_slug': self.slug})


class Reviews(models.Model):
    title = models.CharField(max_length=40, db_index=True, verbose_name="Заголовок")
    event_option = models.CharField(max_length= 255, choices=events_options,verbose_name="Опции")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, verbose_name="Ссылка")
    photo = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/', blank=False, verbose_name="Фото")
    content = models.TextField(verbose_name="Контент")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")


    def get_absolute_url(self):
        return reverse('show_review', kwargs={'review_slug': self.slug})

    class Meta:
        verbose_name = 'Обзор (афиша, не на карту)'
        verbose_name_plural = "Обзоры (афиша, не на карту)"
        
    def __str__(self):
        return '%s - %s' % (self.title, self.time_created)



class Events(models.Model):
    title = models.CharField(max_length=40, db_index=True, verbose_name="Заголовок")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, verbose_name="Ссылка")
    photo = models.ImageField(upload_to='photos/events/%Y/%m/%d/', blank=False, verbose_name="Фото")
    content = models.TextField(verbose_name="Контент")
    latitude = models.FloatField(max_length=40, db_index=True, verbose_name="Широта")
    longitude = models.FloatField(max_length=40, db_index=True, verbose_name="Долгота")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def get_absolute_url(self):
        return reverse('show_event', kwargs={'event_slug': self.slug})
    class Meta:
        verbose_name = 'Событие (афиша событий, на карту)'
        verbose_name_plural = "События (афиша событий, идет на карту)"

    def __str__(self):
        return '%s - %s' % (self.title, self.time_created)


class Categories(models.Model):
    name = models.CharField(max_length=40, db_index=True, verbose_name="Название категории")
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True, verbose_name="Ссылка")
    # slug = models.SlugField(max_length=50, db_index=True, unique=True, verbose_name="Ссылка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория заведения'
        verbose_name_plural = "Категории для заведений"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE, null=True, verbose_name="Имя профиля")
    bio=models.TextField(null=True, blank=True,verbose_name="О себе")#auto_created
    profile_pic=models.ImageField(upload_to=f'photos/profile_images/%Y/%m/%d/', null=True, blank=True, verbose_name="Фото профиля")
    profile_pic_1 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', blank=True, verbose_name="Фото")
    profile_pic_2 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', blank=True, verbose_name="Фото")
    profile_pic_3 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', blank=True, verbose_name="Фото")
    tg_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Телеграмм")
    vk_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="ВК")
    web_site_url=models.CharField(max_length=255, blank=True, null=True,verbose_name="Сайт")
    instagram_url=models.CharField(max_length=255, blank=True, null=True,verbose_name="Инстаграмм")

    class Meta:
        verbose_name = 'Профиль пользователя/компании'
        verbose_name_plural = "Профили пользователей/компаний"

    def __str__(self):
        return str(self.user)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True,)
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="Телефон")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи и компании"

    def __str__(self):
        return '%s - %s' % (self.username, self.email)

class Comments(models.Model):
    article = models.ForeignKey(CompanyPost, related_name='comments', on_delete=models.CASCADE, verbose_name="Обсуждение")
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_comment', on_delete=models.CASCADE, verbose_name= "Комментатор")
    body = models.TextField(verbose_name="Комментарий")
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    class Meta:
        verbose_name = 'Комментарий к заведению'
        verbose_name_plural = "Комментарии к заведениям"


    def __str__(self):
        return '%s - %s' % (self.article.title, self.comment_author)




class NewsComments(models.Model):
    article = models.ForeignKey(CompanyNews, related_name='news_comments', on_delete=models.CASCADE,verbose_name="Обсуждение")
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news_user_comment',on_delete=models.CASCADE, verbose_name="Комментатор")
    body = models.TextField(verbose_name="Комментарий")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Время изменения")


    def __str__(self):
        return '%s - %s - %s' % (self.article.title, self.comment_author, self.body)

    def total_comments(self):
        return self.article.count()

    class Meta:
        verbose_name = 'Комментарий к постам(новостям)'
        verbose_name_plural = "Комментарии к постам(новостям)"

class BannerPhoto(models.Model):
    img = models.ImageField(upload_to='photos/main_banner_photos/%Y/%m/%d/', null=True, blank=True, verbose_name="Баннер главный")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    class Meta:
        verbose_name = 'Реклама (баннер 1270/960px)'
        verbose_name_plural = "Реклама (баннер 1270/960px)"
    def __str__(self):
        return '%s' % (self.time_created)

class BannerVideo(models.Model):
    video = models.FileField(upload_to='videos/main_banner_videos/%Y/%m/%d/', null=True, blank=True, verbose_name="Баннер главный")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        verbose_name = 'Видео (баннер с надписью sfera и соцсетями)'
        verbose_name_plural = 'Видео (баннер с надписью sfera и соцсетями)'
    def __str__(self):
        return '%s' % (self.time_created)









