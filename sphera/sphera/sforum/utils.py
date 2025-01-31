from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
import inspect
import datetime
import urllib.parse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login, logout_then_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import (
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    Http404,
    HttpResponse,
    StreamingHttpResponse,
)
from django.shortcuts import resolve_url
from django.utils.encoding import force_str
from django.utils.timezone import now
from .models import *

menu = [
    # {"title": "О нас", 'url_name': 'about'},
    # {"title": "Пост", 'url_name': 'add_post'},
    # {"title": "Публикация", 'url_name': 'add_new'},
    {"title": "ИЗБРАННОЕ", 'url_name': 'show_fav'},
    # {"title": "Галерея", 'url_name': 'contacts'},
    # {"title": "КОНТАКТЫ", 'url_name': 'contacts'},
    {"title": "МЕСТА", 'url_name': 'show_venues'},

]

menu2= [
    # {"title": "О нас", 'url_name':'about'},
    {"title": "ИЗБРАННОЕ", 'url_name': 'show_fav'},
    # {"title": "КОНТАКТЫ", 'url_name': 'contacts'},
    {"title": "МЕСТА", 'url_name': 'show_venues'},

]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.has_perms(['sforum.add_companypost', 'sforum.change_companypost', 'sforum.change_companypost']):
            user_menu = menu2.copy()
        context['menu'] = user_menu
        cats = Categories.objects.all()
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected']=0
        return context
class AccessMixin:
    """
    Base access mixin. All other access mixins should extend this one.
    """

    login_url = None
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    redirect_unauthenticated_users = False

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get_login_url(self):
        """
        Override this method to customize the login_url.
        """
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                f"Define {self._class_name}.login_url or settings.LOGIN_URL or "
                f"override {self._class_name}.get_login_url()."
            )

        return force_str(login_url)

    def get_redirect_field_name(self):
        """
        Override this method to customize the redirect_field_name.
        """
        if self.redirect_field_name is None:
            raise ImproperlyConfigured(
                f"{self._class_name} is missing the redirect_field_name. "
                f"Define {self._class_name}.redirect_field_name or "
                f"override {self._class_name}.get_redirect_field_name()."
            )
        return self.redirect_field_name

    def handle_no_permission(self, request):
        """What should happen if the user doesn't have permission?"""
        if self.raise_exception:
            if (
                self.redirect_unauthenticated_users
                and not request.user.is_authenticated
            ):
                return self.no_permissions_fail(request)
            else:
                if inspect.isclass(self.raise_exception) and issubclass(
                    self.raise_exception, Exception
                ):
                    raise self.raise_exception
                if callable(self.raise_exception):
                    ret = self.raise_exception(request)
                    if isinstance(ret, (HttpResponse, StreamingHttpResponse)):
                        return ret
                raise PermissionDenied

        return self.no_permissions_fail(request)

    def no_permissions_fail(self, request=None):
        """
        Called when the user has no permissions and no exception was raised.
        This should only return a valid HTTP response.

        By default we redirect to login.
        """
        return redirect_to_login(
            request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

class GroupRequiredMixin(AccessMixin):
    group_required = None

    def get_group_required(self):
        """Get which group's membership is required"""
        if any([
            self.group_required is None,
            not isinstance(self.group_required, (list, tuple, str))
        ]):

            raise ImproperlyConfigured(
                f'{self._class_name} requires the `group_required` attribute '
                "to be set and be a string, list, or tuple."
            )
        if not isinstance(self.group_required, (list, tuple)):
            self.group_required = (self.group_required,)
        return self.group_required

    def check_membership(self, groups):
        """Check for user's membership in required groups. Superusers are
        automatically members"""
        if self.request.user.is_superuser:
            return True

        user_groups = self.request.user.groups.values_list("name", flat=True)
        return set(groups).intersection(set(user_groups))

    def dispatch(self, request, *args, **kwargs):
        """Call the appropriate handler if the user is a group member"""
        self.request = request
        in_group = False
        if request.user.is_authenticated:
            in_group = self.check_membership(self.get_group_required())

        if not in_group:
            return self.handle_no_permission(request)

        return super().dispatch(request, *args, **kwargs)
#
# stations = (
#     ("Akademicheskaya", "Академическая"),
#     ("Alexandrovsky Sad", "Александровский сад"),
#     ("Altufyevo", "Алтуфьево"),
#     ("Arbatskaya", "Арбатская"),
#     ("Barrikadnaya", "Баррикадная"),
#     ("Belorusskaya", "Белорусская"),
#     ("Biblioteka imeni Lenina", "Библиотека имени Ленина"),
#     ("Borovskoye Shosse", "Борисово"),
#     ("Botanichesky Sad", "Ботанический сад"),
#     ("Varshavskaya", "Варшавская"),
#     ("VDNKh", "ВДНХ"),
#     ("Vladikino", "Владыкино"),
#     ("Volzhskaya", "Волжская"),
#     ("Vorobyovy Gory", "Воробьёвы горы"),
#     ("Delovoy Tsentr", "Деловой центр"),
#     ("Dmitrovskaya", "Дмитровская"),
#     ("Dubrovka", "Дубровка"),
#     ("Yevropeyskaya", "Европейская"),
#     ("Zhulebino", "Жулебино"),
#     ("Zelenogradskaya", "Зеленоградская"),
#     ("Zyablikovo", "Зябликово"),
#     ("Kaluzhskaya", "Калужская"),
#     ("Kievskaya", "Киевская"),
#     ("Kitay-Gorod", "Китай-город"),
#     ("Kinostudiya imeni Gorkogo", "Киностудия имени Горького"),
#     ("Kozhukhovskaya", "Кожуховская"),
#     ("Kolomenskaya", "Коломенская"),
#     ("Konkovo", "Коньково"),
#     ("Krasnopresnenskaya", "Краснопресненская"),
#     ("Krasnopolyanaya", "Краснополянская"),
#     ("Kubinka", "Кубинка"),
#     ("Kuznetsky Most", "Кузнецкий мост"),
#     ("Kutuzovskaya", "Кутузовская"),
#     ("Leninskiy Prospekt", "Ленинский проспект"),
#     ("Lubyanka", "Лубянка"),
#     ("Mayakovskaya", "Маяковская"),
#     ("Medvedkovo", "Медведково"),
#     ("Moscow-City", "Москва-сити"),
#     ("Mitino", "Митино"),
#     ("Mytishchi", "Мытищи"),
#     ("Nagornaya", "Нагорная"),
#     ("Nagatino", "Нагатинская"),
#     ("Nalivnaya", "Наливная"),
#     ("Nizhegorodskaya", "Нижегородская"),
#     ("Novogireyevo", "Новогиреево"),
#     ("Novokosino", "Новокосино"),
#     ("Novoyasenevskaya", "Новоясеневская"),
#     ("Oktyabrskaya", "Октябрьская"),
#     ("Ozyornaya", "Озерная"),
#     ("Orechovo", "Орехово"),
#     ("Paveletskaya", "Павелецкая"),
#     ("Panfilovskaya", "Панфиловская"),
#     ("Pecherskaya", "Печерская"),
#     ("Planernaya", "Планерная"),
#     ("Ploshchad Revolyutsii", "Площадь Революции"),
#     ("Pushkinskaya", "Пушкинская"),
#     ("Ramenki", "Раменки"),
#     ("Rizhskaya", "Рижская"),
#     ("Rumyantsevo", "Румянцево"),
#     ("Savelyovskaya", "Савеловская"),
#     ("Semenovskaya", "Семеновская"),
#     ("Serpukhovskaya", "Серпуховская"),
#     ("Skobelevskaya", "Скобелевская"),
#     ("Slavyansky Bulvar", "Славянский бульвар"),
#     ("Smolenskaya", "Смоленская"),
#     ("Sokol", "Сокол"),
#     ("Starokachalovskaya", "Старокачаловская"),
#     ("Studencheskaya", "Студенческая"),
#     ("Taganskaya", "Таганская"),
#     ("Tverskaya", "Тверская"),
#     ("Timiryazevskaya", "Тимирязевская"),
#     ("Tulskaya", "Тульская"),
#     ("Ulitsa 1905 Goda", "Улица 1905 года"),
#     ("Udaltsova", "Удальцова"),
#     ("Ulyanovskaya", "Ульяновская"),
#     ("Frunzenskaya", "Фрунзенская"),
#     ("Khoroshevo", "Хорошёво"),
#     ("TsDK", "ЦДК"),
#     ("Cherkizovskaya", "Черкизовская"),
#     ("Chistye Prudy", "Чистые пруды"),
#     ("Shabolovskaya", "Шаболовская"),
#     ("Shchelopekha", "Шелепиха"),
#     ("Shchelkovskaya", "Щелковская"),
#     ("Elektrozavodskaya", "Электрозаводская"),
#     ("Yugo-Zapadnaya", "Юго-Западная"),
#     ("Yuzhnaya", "Южная"),
#     ("Yasenevo", "Ясенево"),
#
#     # Станции МЦК
#     ("Kiyevskaya (MCK)", "Киевская"),
#     ("Kuntsevskaya", "Кунцевская"),
#     ("Slavyansky Bulvar (MCK)", "Славянский бульвар"),
#     ("Studencheskaya (MCK)", "Студенческая"),
#     ("Shchelopekha (MCK)", "Шелепиха"),
#     ("Luzhniki", "Лужники"),
#     ("Kropotkinskaya", "Кропоткинская"),
#     ("Krasnopresnenskaya (MCK)", "Краснопресненская"),
#     ("Zvenigorodskaya", "Звенигородская"),
#     ("Kashirskaya (MCK)", "Каширская"),
#     ("Taganskaya (MCK)", "Таганская"),
#     ("Nagornaya (MCK)", "Нагорная"),
#     ("Frunzenskaya (MCK)", "Фрунзенская"),
# )
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