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
stations = (("Автозаводская", "Автозаводская"),
    ("Академическая", "Академическая"),
    ("Александровский сад", "Александровский сад"),
    ("Алексеевская", "Алексеевская"),
    ("Алтуфьево", "Алтуфьево"),
    ("Андроновка", "Андроновка"),
    ("Аннино", "Аннино"),
    ("Арбатская (Синяя линия)", "Арбатская (Синяя линия)"),
    ("Арбатская (Фиолетовая линия)", "Арбатская (Фиолетовая линия)"),
    ("Аэропорт", "Аэропорт"),
    ("Бабушкинская", "Бабушкинская"),
    ("Багратионовская", "Багратионовская"),
    ("Баррикадная", "Баррикадная"),
    ("Бауманская", "Бауманская"),
    ("Беговая", "Беговая"),
    ("Белорусская (Кольцевая)", "Белорусская (Кольцевая)"),
    ("Белорусская (Зеленая линия)", "Белорусская (Зеленая линия)"),
    ("Беляево", "Беляево"),
    ("Бибирево", "Бибирево"),
    ("Библиотека имени Ленина", "Библиотека имени Ленина"),
    ("Борисово", "Борисово"),
    ("Боровицкая", "Боровицкая"),
    ("Ботанический сад", "Ботанический сад"),
    ("Братиславская", "Братиславская"),
    ("Бульвар Адмирала Ушакова", "Бульвар Адмирала Ушакова"),
    ("Бульвар Дмитрия Донского", "Бульвар Дмитрия Донского"),
    ("Бульвар Рокоссовского", "Бульвар Рокоссовского"),
    ("Бунинская аллея", "Бунинская аллея"),
    ("Бутырская", "Бутырская"),
    ("Варшавская", "Варшавская"),
    ("ВДНХ", "ВДНХ"),
    ("Верхние Лихоборы", "Верхние Лихоборы"),
    ("Владыкино", "Владыкино"),
    ("Водный стадион", "Водный стадион"),
    ("Войковская", "Войковская"),
    ("Волгоградский проспект", "Волгоградский проспект"),
    ("Волжская", "Волжская"),
    ("Волхонка", "Волхонка"),
    ("Воробьевы горы", "Воробьевы горы"),
    ("Воронцовская", "Воронцовская"),
    ("Выставочная", "Выставочная"),
    ("Выхино", "Выхино"),
    ("Говорово", "Говорово"),
    ("Деловой центр (Большая кольцевая)", "Деловой центр (Большая кольцевая)"),
    ("Деловой центр (Голубая линия)", "Деловой центр (Голубая линия)"),
    ("Динамо", "Динамо"),
    ("Дмитровская", "Дмитровская"),
    ("Добрынинская", "Добрынинская"),
    ("Домодедовская", "Домодедовская"),
    ("Дубровка", "Дубровка"),
    ("Жулебино", "Жулебино"),
    ("Зорге", "Зорге"),
    ("Зябликово", "Зябликово"),
    ("Зюзино", "Зюзино"),
    ("Измайловская", "Измайловская"),
    ("Калужская", "Калужская"),
    ("Кантемировская", "Кантемировская"),
    ("Каховская", "Каховская"),
    ("Каширская", "Каширская"),
    ("Киевская (Кольцевая)", "Киевская (Кольцевая)"),
    ("Киевская (Голубая линия)", "Киевская (Голубая линия)"),
    ("Киевская (Арбатско-Покровская)", "Киевская (Арбатско-Покровская)"),
    ("Китай-город", "Китай-город"),
    ("Кожуховская", "Кожуховская"),
    ("Комсомольская (Кольцевая)", "Комсомольская (Кольцевая)"),
    ("Комсомольская (Красная линия)", "Комсомольская (Красная линия)"),
    ("Коньково", "Коньково"),
    ("Красногвардейская", "Красногвардейская"),
    ("Краснопресненская", "Краснопресненская"),
    ("Красносельская", "Красносельская"),
    ("Красные Ворота", "Красные Ворота"),
    ("Крестьянская застава", "Крестьянская застава"),
    ("Кропоткинская", "Кропоткинская"),
    ("Крылатское", "Крылатское"),
    ("Кузнецкий мост", "Кузнецкий мост"),
    ("Кузьминки", "Кузьминки"),
    ("Кунцевская (Синяя линия)", "Кунцевская (Синяя линия)"),
    ("Кунцевская (Большая кольцевая)", "Кунцевская (Большая кольцевая)"),
    ("Курская (Кольцевая)", "Курская (Кольцевая)"),
    ("Курская (Синяя линия)", "Курская (Синяя линия)"),
    ("Кутузовская", "Кутузовская"),
    ("Ленинский проспект", "Ленинский проспект"),
    ("Лермонтовский проспект", "Лермонтовский проспект"),
    ("Лесопарковая", "Лесопарковая"),
    ("Лубянка", "Лубянка"),
    ("Люблино", "Люблино"),
    ("Марксистская", "Марксистская"),
    ("Марьина Роща", "Марьина Роща"),
    ("Марьино", "Марьино"),
    ("Маяковская", "Маяковская"),
    ("Медведково", "Медведково"),
    ("Международная", "Международная"),
    ("Менделеевская", "Менделеевская"),
    ("Минская", "Минская"),
    ("Митино", "Митино"),
    ("Молодежная", "Молодежная"),
    ("Нагатинская", "Нагатинская"),
    ("Нагорная", "Нагорная"),
    ("Нахимовский проспект", "Нахимовский проспект"),
    ("Некрасовка", "Некрасовка"),
    ("Нижегородская", "Нижегородская"),
    ("Новогиреево", "Новогиреево"),
    ("Новокосино", "Новокосино"),
    ("Новокузнецкая", "Новокузнецкая"),
    ("Новослободская", "Новослободская"),
    ("Новохохловская", "Новохохловская"),
    ("Новые Черемушки", "Новые Черемушки"),
    ("Окружная", "Окружная"),
    ("Октябрьская (Кольцевая)", "Октябрьская (Кольцевая)"),
    ("Октябрьская (Оранжевая линия)", "Октябрьская (Оранжевая линия)"),
    ("Октябрьское поле", "Октябрьское поле"),
    ("Орехово", "Орехово"),
    ("Отрадное", "Отрадное"),
    ("Охотный ряд", "Охотный ряд"),
    ("Павелецкая (Кольцевая)", "Павелецкая (Кольцевая)"),
    ("Павелецкая (Зеленая линия)", "Павелецкая (Зеленая линия)"),
    ("Парк культуры (Кольцевая)", "Парк культуры (Кольцевая)"),
    ("Парк культуры (Красная линия)", "Парк культуры (Красная линия)"),
    ("Парк Победы", "Парк Победы"),
    ("Партизанская", "Партизанская"),
    ("Первомайская", "Первомайская"),
    ("Перово", "Перово"),
    ("Петровско-Разумовская", "Петровско-Разумовская"),
    ("Печатники", "Печатники"),
    ("Пионерская", "Пионерская"),
    ("Планерная", "Планерная"),
    ("Площадь Ильича", "Площадь Ильича"),
    ("Площадь Революции", "Площадь Революции"),
    ("Полежаевская", "Полежаевская"),
    ("Полянка", "Полянка"),
    ("Пражская", "Пражская"),
    ("Преображенская площадь", "Преображенская площадь"),
    ("Пролетарская", "Пролетарская"),
    ("Проспект Вернадского", "Проспект Вернадского"),
    ("Проспект Мира (Кольцевая)", "Проспект Мира (Кольцевая)"),
    ("Проспект Мира (Оранжевая линия)", "Проспект Мира (Оранжевая линия)"),
    ("Профсоюзная", "Профсоюзная"),
    ("Пушкинская", "Пушкинская"),
    ("Раменки", "Раменки"),
    ("Рассказовка", "Рассказовка"),
    ("Речной вокзал", "Речной вокзал"),
    ("Рижская", "Рижская"),
    ("Римская", "Римская"),
    ("Ростокино", "Ростокино"),
    ("Румянцево", "Румянцево"),
    ("Рязанский проспект", "Рязанский проспект"),
    ("Савеловская", "Савеловская"),
    ("Свиблово", "Свиблово"),
    ("Севастопольская", "Севастопольская"),
    ("Селигерская", "Селигерская"),
    ("Семеновская", "Семеновская"),
    ("Серпуховская", "Серпуховская"),
    ("Славянский бульвар", "Славянский бульвар"),
    ("Смоленская (Голубая линия)", "Смоленская (Голубая линия)"),
    ("Смоленская (Синяя линия)", "Смоленская (Синяя линия)"),
    ("Сокол", "Сокол"),
    ("Сокольники", "Сокольники"),
    ("Спартак", "Спартак"),
    ("Спортивная", "Спортивная"),
    ("Сретенский бульвар", "Сретенский бульвар"),
    ("Строгино", "Строгино"),
    ("Студенческая", "Студенческая"),
    ("Сухаревская", "Сухаревская"),
    ("Сходненская", "Сходненская"),
    ("Таганская (Кольцевая)", "Таганская (Кольцевая)"),
    ("Таганская (Фиолетовая линия)", "Таганская (Фиолетовая линия)"),
    ("Тверская", "Тверская"),
    ("Театральная", "Театральная"),
    ("Текстильщики", "Текстильщики"),
    ("Технопарк", "Технопарк"),
    ("Тимирязевская", "Тимирязевская"),
    ("Третьяковская (Оранжевая линия)", "Третьяковская (Оранжевая линия)"),
    ("Третьяковская (Желтая линия)", "Третьяковская (Желтая линия)"),
    ("Тропарево", "Тропарево"),
    ("Трубная", "Трубная"),
    ("Тульская", "Тульская"),
    ("Тургеневская", "Тургеневская"),
    ("Тушинская", "Тушинская"),
    ("Угрешская", "Угрешская"),
    ("Улица 1905 года", "Улица 1905 года"),
    ("Улица Академика Янгеля", "Улица Академика Янгеля"),
    ("Улица Горчакова", "Улица Горчакова"),
    ("Улица Скобелевская", "Улица Скобелевская"),
    ("Улица Старокачаловская", "Улица Старокачаловская"),
    ("Университет", "Университет"),
    ("Филевский парк", "Филевский парк"),
    ("Фили", "Фили"),
    ("Фонвизинская", "Фонвизинская"),
    ("Фрунзенская", "Фрунзенская"),
    ("Ховрино", "Ховрино"),
    ("Царицыно", "Царицыно"),
    ("Цветной бульвар", "Цветной бульвар"),
    ("Чистые пруды", "Чистые пруды"),
    ("Чкаловская", "Чкаловская"),
    ("Шаболовская", "Шаболовская"),
    ("Шелепиха", "Шелепиха"),
    ("Шипиловская", "Шипиловская"),
    ("Шоссе Энтузиастов", "Шоссе Энтузиастов"),
    ("Щелковская", "Щелковская"),
    ("Щукинская", "Щукинская"),
    ("Электрозаводская", "Электрозаводская"),
    ("Юго-Западная", "Юго-Западная"),
    ("Южная", "Южная"),
    ("Ясенево", "Ясенево"),
    ("Аминьевская", "Аминьевская"),
    ("Арбатская (Синяя линия)", "Арбатская (Синяя линия)"),
    ("Баковка", "Баковка"),
    ("Бескудниково", "Бескудниково"),
    ("Внуково", "Внуково"),
    ("Востряково", "Востряково"),
    ("Говорово", "Говорово"),
    ("Давыдково", "Давыдково"),
    ("Дегунино", "Дегунино"),
    ("Ермакова Роща", "Ермакова Роща"),
    ("ЗИЛ", "ЗИЛ"),
    ("Зеленоград-Крюково", "Зеленоград-Крюково"),
    ("Зорге", "Зорге"),
    ("Карачарово", "Карачарово"),
    ("Кокошкино", "Кокошкино"),
    ("Кубанская", "Кубанская"),
    ("Кунцевская", "Кунцевская"),
    ("Лефортово", "Лефортово"),
    ("Лианозово", "Лианозово"),
    ("Люберцы", "Люберцы"),
    ("Марьина Роща", "Марьина Роща"),
    ("Мичуринский проспект", "Мичуринский проспект"),
    ("Мнёвники", "Мнёвники"),
    ("Некрасовка", "Некрасовка"),
    ("Николаевская", "Николаевская"),
    ("Новаторская", "Новаторская"),
    ("Новопеределкино", "Новопеределкино"),
    ("Новохохловская", "Новохохловская"),
    ("Остафьево", "Остафьево"),
    ("Панфиловская", "Панфиловская"),
    ("Пыхтино", "Пыхтино"),
    ("Рублёво-Архангельское", "Рублёво-Архангельское"),
    ("Саларьево", "Саларьево"),
    ("Сколково", "Сколково"),
    ("Славянский бульвар", "Славянский бульвар"),
    ("Солнцево", "Солнцево"),
    ("Тестовская", "Тестовская"),
    ("Тучково", "Тучково"),
    ("Филатов Луг", "Филатов Луг"),
    ("ЦСКА", "ЦСКА"),
    ("Челобитьево", "Челобитьево"),
    ("Щербинка", "Щербинка"),
    ("Яхромская", "Яхромская"),
    ("Нижегородская (БКЛ)", "Нижегородская (БКЛ)"),
    ("Авиамоторная (БКЛ)", "Авиамоторная (БКЛ)"),
    ("Лефортово (БКЛ)", "Лефортово (БКЛ)"),
    ("Электрозаводская (БКЛ)", "Электрозаводская (БКЛ)"),
    ("Сокольники (БКЛ)", "Сокольники (БКЛ)"),
    ("Рижская (БКЛ)", "Рижская (БКЛ)"),
    ("Марьина Роща (БКЛ)", "Марьина Роща (БКЛ)"),
    ("Савёловская (БКЛ)", "Савёловская (БКЛ)"),
    ("Петровский парк (БКЛ)", "Петровский парк (БКЛ)"),
    ("ЦСКА (БКЛ)", "ЦСКА (БКЛ)"),
    ("Хорошёвская (БКЛ)", "Хорошёвская (БКЛ)"),
    ("Народное Ополчение (БКЛ)", "Народное Ополчение (БКЛ)"),
    ("Мнёвники (БКЛ)", "Мнёвники (БКЛ)"),
    ("Терехово (БКЛ)", "Терехово (БКЛ)"),
    ("Кунцевская (БКЛ)", "Кунцевская (БКЛ)"),
    ("Давыдково (БКЛ)", "Давыдково (БКЛ)"),
    ("Аминьевская (БКЛ)", "Аминьевская (БКЛ)"),
    ("Мичуринский проспект (БКЛ)", "Мичуринский проспект (БКЛ)"),
    ("Проспект Вернадского (БКЛ)", "Проспект Вернадского (БКЛ)"),
    ("Новаторская (БКЛ)", "Новаторская (БКЛ)"),
    ("Воронцовская (БКЛ)", "Воронцовская (БКЛ)"),
    ("Зюзино (БКЛ)", "Зюзино (БКЛ)"),
    ("Каховская (БКЛ)", "Каховская (БКЛ)"),
    ("Варшавская (БКЛ)", "Варшавская (БКЛ)"),
    ("Каширская (БКЛ)", "Каширская (БКЛ)"),
    ("Кленовый бульвар (БКЛ)", "Кленовый бульвар (БКЛ)"),
    ("Нагатинский Затон (БКЛ)", "Нагатинский Затон (БКЛ)"),
    ("Печатники (БКЛ)", "Печатники (БКЛ)"),
    ("Текстильщики (БКЛ)", "Текстильщики (БКЛ)"),
    ("Владыкино (МЦК)", "Владыкино (МЦК)"),
    ("Окружная (МЦК)", "Окружная (МЦК)"),
    ("Лихоборы (МЦК)", "Лихоборы (МЦК)"),
    ("Коптево (МЦК)", "Коптево (МЦК)"),
    ("Балтийская (МЦК)", "Балтийская (МЦК)"),
    ("Стрешнево (МЦК)", "Стрешнево (МЦК)"),
    ("Панфиловская (МЦК)", "Панфиловская (МЦК)"),
    ("Зорге (МЦК)", "Зорге (МЦК)"),
    ("Хорошёво (МЦК)", "Хорошёво (МЦК)"),
    ("Шелепиха (МЦК)", "Шелепиха (МЦК)"),
    ("Москва-Сити (МЦК)", "Москва-Сити (МЦК)"),
    ("Кутузовская (МЦК)", "Кутузовская (МЦК)"),
    ("Лужники (МЦК)", "Лужники (МЦК)"),
    ("Площадь Гагарина (МЦК)", "Площадь Гагарина (МЦК)"),
    ("Крымская (МЦК)", "Крымская (МЦК)"),
    ("Верхние Котлы (МЦК)", "Верхние Котлы (МЦК)"),
    ("ЗИЛ (МЦК)", "ЗИЛ (МЦК)"),
    ("Автозаводская (МЦК)", "Автозаводская (МЦК)"),
    ("Дубровка (МЦК)", "Дубровка (МЦК)"),
    ("Угрешская (МЦК)", "Угрешская (МЦК)"),
    ("Новохохловская (МЦК)", "Новохохловская (МЦК)"),
    ("Нижегородская (МЦК)", "Нижегородская (МЦК)"),
    ("Андроновка (МЦК)", "Андроновка (МЦК)"),
    ("Шоссе Энтузиастов (МЦК)", "Шоссе Энтузиастов (МЦК)"),
    ("Соколиная Гора (МЦК)", "Соколиная Гора (МЦК)"),
    ("Измайлово (МЦК)", "Измайлово (МЦК)"),
    ("Локомотив (МЦК)", "Локомотив (МЦК)"),
    ("Бульвар Рокоссовского (МЦК)", "Бульвар Рокоссовского (МЦК)"),
    ("Белокаменная (МЦК)", "Белокаменная (МЦК)"),
    ("Ростокино (МЦК)", "Ростокино (МЦК)"),
    ("Ботанический сад (МЦК)", "Ботанический сад (МЦК)"),
)
events_options = (
    ("FIRE_FUN", "FIRE_FUN"),
    ("FOR_LIFE", "FOR_LIFE"),
)
profile_options = (
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
    pic_1 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/',null=True, blank=True, verbose_name="Фото")
    pic_2 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/',null=True, blank=True, verbose_name="Фото")
    pic_3 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/',null=True, blank=True, verbose_name="Фото")
    pic_4 = models.ImageField(upload_to='photos/posts/%Y/%m/%d/',null=True, blank=True, verbose_name="Фото")
    content = models.TextField(verbose_name="Описание")
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
    pic_1 = models.ImageField(upload_to='photos/news/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_2 = models.ImageField(upload_to='photos/news/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_3 = models.ImageField(upload_to='photos/news/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_4 = models.ImageField(upload_to='photos/news/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    # pic_5 = models.ImageField(upload_to='photos/news/%Y/%m/%d/', blank=True, verbose_name="Доп.фото")
    # pic_6 = models.ImageField(upload_to='photos/news/%Y/%m/%d/', blank=True, verbose_name="Доп.фото")
    # pic_7 = models.ImageField(upload_to='photos/news/%Y/%m/%d/', blank=True, verbose_name="Доп.фото")
    # pic_8 = models.ImageField(upload_to='photos/news/%Y/%m/%d/', blank=True, verbose_name="Доп.фото")
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
    photo = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/', blank=False, verbose_name="Главное Фото")
    pic_1 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_2 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_3 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_4 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_5 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_6 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_7 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_8 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_9 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_10 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_11 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_12 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_13 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_14 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_15 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    pic_16 = models.ImageField(upload_to='photos/reviews/%Y/%m/%d/',null=True, blank=True, verbose_name="Доп.фото")
    content = models.TextField(verbose_name="Описание")
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
    title_link = models.CharField(max_length=40, db_index=True,null=True,blank = True, verbose_name="Ссылка на событие")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, verbose_name="Ссылка")
    photo = models.ImageField(upload_to='photos/events/%Y/%m/%d/', blank=False, verbose_name="Фото")
    content = models.TextField(verbose_name="Описание")
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
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE, null=True, verbose_name="Никнейм")
    bio=models.TextField(null=True, blank=True,verbose_name="О себе")#auto_created
    profile_options = models.CharField(max_length= 255, null = True, blank = True, choices=profile_options,verbose_name="Опции")
    profile_pic=models.ImageField(upload_to=f'photos/profile_images/%Y/%m/%d/', null=True, blank=True, verbose_name="Фото профиля")
    profile_pic_1 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', blank=True, verbose_name="Фото")
    profile_pic_2 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', blank=True, verbose_name="Фото")
    profile_pic_3 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', blank=True, verbose_name="Фото")
    profile_pic_4 = models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/',null=True, blank=True, verbose_name="Фото")
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
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name="Телефон в формате +7")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи и компании"

    def __str__(self):
        group = self.groups.first()
        group_name = group.name if group else "Без группы"
        return f'{self.username} - {self.email} ({group_name})'


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
class BannerLink(models.Model):
    title = models.CharField(max_length=40,null=True, db_index=True, verbose_name="Заголовок")
    body_link = models.TextField(null = True, blank= False, db_index=True, verbose_name="Ссылка на партнеров")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    class Meta:
        verbose_name = 'Партнерская ссылка'
        verbose_name_plural = "Партнерские ссылки"
    def __str__(self):
        return '%s' % (self.title)

class BannerPhoto(models.Model):
    title = models.CharField(max_length=40,null=True, db_index=True, verbose_name="Заголовок")
    img = models.ImageField(upload_to='photos/main_banner_photos/%Y/%m/%d/', null=True, blank=False, verbose_name="Баннер главный")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    class Meta:
        verbose_name = 'Реклама (баннер 1270/960px)'
        verbose_name_plural = "Реклама (баннер 1270/960px)"
    def __str__(self):
        return '%s' % (self.title)

class BannerVideo(models.Model):
    title = models.CharField(max_length=40,null=True, db_index=True, verbose_name="Заголовок")
    video = models.FileField(upload_to='videos/main_banner_videos/%Y/%m/%d/', null=True, blank=False, verbose_name="Баннер главный")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        verbose_name = 'Видео (баннер с надписью sfera и соцсетями)'
        verbose_name_plural = 'Видео (баннер с надписью sfera и соцсетями)'
    def __str__(self):
        return '%s' % (self.title)









