import json
import os
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
# from IPython.terminal.shortcuts.auto_match import braces
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponse, HttpResponseNotFound
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import views
from .forms import *
# Create your views here.
from .models import *
from .utils import *

menu = [
    # {"title": "Пост", 'url_name': 'add_post'},
    # {"title": "Публикация", 'url_name': 'add_new'},
    {"title": "ИЗБРАННОЕ", 'url_name': 'show_fav'},
    # {"title": "Галерея", 'url_name': 'contacts'},
    # {"title": "КОНТАКТЫ", 'url_name': 'contacts'},
    {"title": "МЕСТА", 'url_name': 'show_venues'},



]
menu2=[
    # {"title": "О нас", 'url_name':'about'}
    {"title": "ИЗБРАННОЕ", 'url_name': 'show_fav'},
    # {"title": "КОНТАКТЫ", 'url_name': 'contacts'},
    {"title": "МЕСТА", 'url_name': 'show_venues'},]

# class Sphera(DataMixin, ListView):
#     model = CompanyPost
#     template_name = 'sforum/index.html'
#     context_object_name = 'posts'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="home")
#         return dict(list(context.items()) + list(c_def.items()))
#
# class ShowNews(DataMixin, ListView):
#     model= CompanyNews
#     template_name = 'sforum/index.html'
#     context_object_name = 'news'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="home")
#         return dict(list(context.items()) + list(c_def.items()))

# def group_required(*group_names):
#     """Requires user membership in at least one of the groups passed in."""
#     def in_groups(u):
#         if u.is_authenticated():
#             if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
#                 return True
#         return False
#
#     return user_passes_test(in_groups, login_url='403')
def main_page(request):
    user_menu = menu.copy()
    # if not request.user.has_perms(['sforum.add_companypost', 'sforum.change_companypost', 'sforum.change_companypost']):
    if not request.user.groups.filter(name="company"):
        user_menu = menu2.copy()
    banners = BannerPhoto.objects.all().order_by('-time_created')[:10]
    banners_video = BannerVideo.objects.all().order_by('-time_created')[:1]
    reviews = Reviews.objects.all().order_by('-time_created')[:2]
    events = Events.objects.all().order_by('-time_created')[:8]
    posts=CompanyPost.objects.all().order_by('-time_created')[:8]
    news=CompanyNews.objects.all().order_by('-time_created')[:8]
    comments = Comments.objects.all().order_by('-date_added')[:10]
    partners_link = BannerLink.objects.all().order_by('-time_created')[:1]
    news_comments = NewsComments.objects.all().order_by('-date_added')[:10]
    # cats = Categories.objects.all()
    return render(request, 'sforum/index.html', {'posts':posts, 'menu': user_menu, 'news':news, 'events':events,'reviews':reviews, 'comments':comments, "banners_photo":banners,"news_comments":news_comments,"banners_video":banners_video, "partners_link":partners_link,})

class ShowProfile(DataMixin, DetailView):
    model = Profile
    template_name = 'sforum/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        
        # Сортируем записи по убыванию даты создания
        page_user_venues = CompanyPost.objects.filter(company_name_id=page_user.user.id).order_by('-time_created')
        page_user_news = CompanyNews.objects.filter(company_name_id=page_user.user.id).order_by('-time_created')

        context = super().get_context_data(**kwargs)
        context['page_user'] = page_user
        context['page_user_venues'] = page_user_venues
        context['page_user_news'] = page_user_news
        c_def = self.get_user_context(title="article")

        return dict(list(context.items()) + list(c_def.items()))
class CreateProfile(DataMixin, CreateView):
    model = Profile
    success_url = reverse_lazy('home')
    template_name = 'sforum/create_profile.html'
    fields = (
    'bio', 'profile_options','profile_pic', "profile_pic_1", "profile_pic_2", "profile_pic_3","profile_pic_4", "tg_url", "vk_url", "web_site_url",
    "instagram_url",)

    def form_valid(self, form):

        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))
class DeleteProfile(DataMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('home')
    template_name = 'sforum/delete_profile.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))
class UpdateProfile(DataMixin, UpdateView):
    model = Profile
    success_url = reverse_lazy('home')
    template_name = 'sforum/update_profile.html'
    fields = (
        'bio', 'profile_options', 'profile_pic', "profile_pic_1", "profile_pic_2", "profile_pic_3","profile_pic_4", "tg_url", "vk_url", "web_site_url",
        "instagram_url",)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))




class ShowVenues(DataMixin, ListView):
    model = CompanyPost
    template_name = 'sforum/venues.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="home")
        return dict(list(context.items()) + list(c_def.items()))

    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        if not ordering: ordering = '-time_created'
        return ordering

class ShowNews(DataMixin, ListView):
    model = CompanyNews
    template_name = 'sforum/news.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="home")
        return dict(list(context.items()) + list(c_def.items()))
    def get_ordering(self):
        ordering = '-time_created'
        return ordering

def showreviews(request):
    user_menu = menu.copy()
    if not request.user.groups.filter(name="company"):
        user_menu = menu2.copy()
    reviews = Reviews.objects.all().order_by('-time_created')
    events = Events.objects.all().order_by('-time_created')
    return render(request, 'sforum/show_reviews.html',
                  {'menu': user_menu, 'events': events, 'reviews': reviews,})

class ShowReviews(DataMixin, ListView):
    model = Reviews
    context_object_name = 'reviews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="home")
        return dict(list(context.items()) + list(c_def.items()))
    def get_ordering(self):
        ordering = '-time_created'
        return ordering
# class ShowEvents(DataMixin, ListView):
#     model = Events
#     template_name = 'sforum/show_events.html'
#     context_object_name = 'events'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="home")
#         return dict(list(context.items()) + list(c_def.items()))

class ShowEvent(DataMixin, DetailView):
    model = Events
    template_name = 'sforum/show_event.html'
    slug_url_kwarg = 'event_slug'
    context_object_name = 'event'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        post = get_object_or_404(Events, slug=self.kwargs['event_slug'])
        # liked = True
        # if post.likes.filter(id=self.request.user.id).exists():
        #     liked = True
        # context['liked'] = liked
        return dict(list(context.items()) + list(c_def.items()))

class ShowReview(DataMixin, DetailView):
    model = Reviews
    template_name = 'sforum/show_review.html'
    slug_url_kwarg = 'review_slug'
    context_object_name = 'review'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        post = get_object_or_404(Reviews, slug=self.kwargs['review_slug'])
        # liked = True
        # if post.likes.filter(id=self.request.user.id).exists():
        #     liked = True
        # context['liked'] = liked
        return dict(list(context.items()) + list(c_def.items()))


class ShowNew(DataMixin, DetailView):
    model = CompanyNews
    template_name = 'sforum/show_new.html'
    slug_url_kwarg = 'new_slug'
    context_object_name = 'new'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        post = get_object_or_404(CompanyNews, slug=self.kwargs['new_slug'])
        # liked = True
        # if post.likes.filter(id=self.request.user.id).exists():
        #     liked = True
        # context['liked'] = liked
        return dict(list(context.items()) + list(c_def.items()))

class AddNews(GroupRequiredMixin, DataMixin, CreateView):
    form_class = AddNewsForm
    success_url = reverse_lazy('home')
    template_name = 'sforum/add_new.html'
    group_required = [u"Компания", u"Админ", u"Пользователь"]
    # permission_required = 'sforum.add_companynews'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        form.instance.company_name= self.request.user
        return super().form_valid(form)

class DeleteNews(GroupRequiredMixin,DataMixin, DeleteView):
    model = CompanyNews
    group_required = [u"Компания", u"Админ", u"Пользователь"]
    template_name = 'sforum/delete_news.html'
    success_url = reverse_lazy('home')
    # permission_required = 'sforum.delete_companynews'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))
class UpdateNews(GroupRequiredMixin, DataMixin, UpdateView):
    group_required = [u"Компания", u"Админ", u"Пользователь"]
    template_name_suffix = "_update_form"
    template_name = 'sforum/update_news.html'
    form_class = AddNewsForm
    model = CompanyNews
    # permission_required = 'sforum.change_companynews'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактировать")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        form.instance.company_name= self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('home')


class AddReview(GroupRequiredMixin, DataMixin, CreateView):
    group_required = u"Админ"
    form_class = AddReviewForm
    success_url = reverse_lazy('home')
    template_name = 'sforum/add_review.html'
    # permission_required = None
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        return super().form_valid(form)

class AddEvent(GroupRequiredMixin, DataMixin, CreateView):
    group_required = u"Админ"
    form_class = AddEventForm
    success_url = reverse_lazy('home')
    template_name = 'sforum/add_event.html'
    # permission_required = None
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        return super().form_valid(form)

class ShowPost(DataMixin, DetailView):
    model = CompanyPost
    template_name = 'sforum/show_article.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="article")
        in_fav = False
        post1 = get_object_or_404(CompanyPost, slug=self.kwargs['post_slug'])
        if post1.favourites.filter(id = self.request.user.id).exists():
            in_fav = True
        context['in_fav'] = in_fav
        return dict(list(context.items()) + list(c_def.items()))

class AddPost(GroupRequiredMixin,DataMixin, CreateView):
    form_class = AddPostForm
    group_required = [u"Компания", u"Админ"]
    # permission_required = 'sforum.add_companypost'
    group_required = [u"Компания", u"Админ"]
    template_name = "sforum/add_post.html"
    success_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add your article")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.company_name = self.request.user
        return super().form_valid(form)
class UpdatePost(GroupRequiredMixin, DataMixin, UpdateView):
    group_required = [u"Компания", u"Админ"]
    form_class = AddPostForm
    template_name='sforum/update_post.html'
    success_url = reverse_lazy('home')
    model = CompanyPost
    # permission_required = 'sforum.change_companypost'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактировать")
        return dict(list(context.items()) + list(c_def.items()))

class DeletePost(GroupRequiredMixin,DataMixin, DeleteView):
    model = CompanyPost
    group_required = [u"Компания", u"Админ"]
    template_name = 'sforum/delete_post.html'
    success_url = reverse_lazy('home')
    # permission_required = 'sforum.delete_companypost'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактировать")
        return dict(list(context.items()) + list(c_def.items()))




class ShowCategories(DataMixin, ListView):
    model = CompanyPost
    template_name = "sforum/venues.html"
    context_object_name = "posts"
    # allow_empty = False  # 404 если страница не найдена при выводе несуществуещих данных бд

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Category - " + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return CompanyPost.objects.filter(cat__slug=self.kwargs["cat_slug"])

class JsonCategories(DataMixin, ListView):
    def get(self, request):
        return JsonResponse(list(CompanyPost.objects.all().values()), safe=False)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


class JsonEvents(View):
    def get(self, request):
        events = Events.objects.all().values()
        return JsonResponse(list(events), safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


class CustomUserRegistration(DataMixin, View):
    success_url = reverse_lazy('create_profile')
    template_name = 'sforum/user_registration.html'

    def get(self, request):
        context= {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context=context)
    def post(self, request, *args, **kwargs):
        form=UserCreationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            if user.email == "@gmail.com" or user.email == "@gmail.com" or user.email == "@yandex.ru":
                user.is_superuser = True
                user.is_staff = True


            user_group = Group.objects.get(name=form.cleaned_data['groups'])
            if str(user_group) == "Компания":
                user.is_active = False
                user.save()


                send_mail(
                    "Subject here",
                    f"Компания  {user.email} оставила заявку на регистрацию, чтобы выдать доступ компании перейдите по ссылке https://vsferemsk.ru/swdjadmin/sforum/user/{user.id}/change/ выберите в группу Компания в поле <группа> и поставьте галочку в поле <активный>",
                    "@yandex.ru",
                    ["@yandex.ru"],
                    fail_silently=False,
                )
                return redirect('email_response')
            user.save()
            user.groups.add(user_group)
            login(request, user)
            return redirect('create_profile')
        else:
            return render(request, self.template_name, {'form':form})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация пользователя")
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('create_profile')

    def get_success_url(self):
        return reverse_lazy('home')


class CustomUserAuthentication(DataMixin, LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('create_profile')
    template_name = 'sforum/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class AddCommentView(CreateView, DataMixin):
    model = Comments
    template_name = "sforum/add_comment.html"
    form_class = AddCommentForm
    success_url = reverse_lazy('home')


    # def form_valid(self, form):
    #     form.instance.article_id=self.kwargs['pk']
    #     return super().form_valid(form)
    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Add comment")
        return dict(list(context.items()) + list(c_def.items()))



class DeleteCommentView(DeleteView,DataMixin):
    model = Comments
    template_name = "sforum/delete_comment.html"
    template_name_suffix = "_check_delete"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Delete comment")
        return dict(list(context.items()) + list(c_def.items()))

class AddNewsCommentView(CreateView, DataMixin):
    model = NewsComments
    template_name = "sforum/add_news_comment.html"
    form_class = AddNewsCommentForm
    success_url = reverse_lazy('home')


    # def form_valid(self, form):
    #     form.instance.article_id=self.kwargs['pk']
    #     return super().form_valid(form)
    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.article_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Add comment")
        return dict(list(context.items()) + list(c_def.items()))



class DeleteNewsCommentView(DeleteView,DataMixin):
    model = NewsComments
    template_name = "sforum/delete_news_comment.html"
    template_name_suffix = "_check_delete"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Delete comment")
        return dict(list(context.items()) + list(c_def.items()))

class AddBannerPhotoView(GroupRequiredMixin,DataMixin, CreateView):
    form_class = AddBannerPhotoForm
    group_required = u"Админ"
    # permission_required = None
    template_name = ("sforum/add_banner_photo.html")
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add banenr")
        return dict(list(context.items()) + list(c_def.items()))

class DeleteBannerPhotoView(GroupRequiredMixin,DataMixin, DeleteView):
    model = BannerPhoto
    # permission_required = None
    group_required = u"Админ"
    template_name = ("sforum/delete_banner_photo.html")

    template_name_suffix = "_check_delete"
    success_url = reverse_lazy('home')

class AddBannerVideoView(GroupRequiredMixin,DataMixin, CreateView):
    form_class = AddBannerVideoForm
    # permission_required = None
    group_required = u"Админ"
    template_name = ("sforum/add_banner_video.html")
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add banenr")
        return dict(list(context.items()) + list(c_def.items()))

class DeleteBannerVideoView(GroupRequiredMixin,DataMixin, DeleteView):
    model = BannerVideo
    # permission_required = None
    group_required = u"Админ"
    template_name = ("sforum/delete_banner_video.html")
    template_name_suffix = "_check_delete"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Delete comment")
        return dict(list(context.items()) + list(c_def.items()))

# class ShowReviews(DataMixin, ListView):
#     model = CompanyNews
#     template_name = 'sforum/reviews.html'
#     context_object_name = 'reviews'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="home")
#         return dict(list(context.items()) + list(c_def.items()))

    #
    # def form_valid(self, form):
    #     form.instance.company_name= self.request.user
    #     return super().form_valid(form)
# class CustomUserRegistration(DataMixin, CreateView):
#     form_class= CustomUserRegistrationForm
#     template_name = 'sforum/user_registration.html'
#
#     def post(self, request, *args, **kwargs):
#         form=CustomUserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#
#             user_group = Group.objects.get(name=form.cleaned_data['groups'])
#             user.groups.add(user_group)
#             return redirect('home')
#         else:
#             return render(request, self.template_name, {'form':form})
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Регистрация пользователя")
#         return dict(list(context.items()) + list(c_def.items()))
#
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')

# class CustomUserAuthentication(DataMixin, LoginView):
#     form_class = CustomUserAuthenticationForm
#     success_url = reverse_lazy('home')
#     template_name = 'sforum/login.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Вход")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_success_url(self):
#         return reverse_lazy('home')
def logout_user(request):
    logout(request)

    return redirect('login')






def search_venues(request):
    cats=Categories.objects.all()
    user_menu = menu.copy()
    if not request.user.has_perms(['sforum.add_companypost', 'sforum.change_companypost', 'sforum.change_companypost']):
        user_menu = menu2.copy()
    if request.method == 'POST':
        searched=request.POST['searched']
        venues=CompanyPost.objects.filter(Q(title__contains=searched) | Q(content__contains=searched) | Q(title__contains=searched.lower()) | Q(content__contains=searched.lower()) | Q(title__contains=searched.upper()) | Q(content__contains=searched.upper()))#Q
        if not venues:
            venues = CompanyPost.objects.filter(Q(title__contains=searched[0]) | Q(content__contains=searched[0]))
    return render(request, 'sforum/search_venues.html', {'searched':searched, 'venues':venues,"menu":user_menu, "cats":cats,})

def likeview(request, slug):
    post=get_object_or_404(CompanyNews, id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('show_new', args=[str(slug)]))

def favview(request, slug):
    post=get_object_or_404(CompanyPost, slug = slug)
    user_menu = menu.copy()
    in_fav=False
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
        in_fav=False
    else:
        post.favourites.add(request.user)
        in_fav=True
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return render(request, f'sforum/show_post/{slug}.html', {"in_fav": in_fav,"menu": user_menu,})

def show_fav(request):
    favs = CompanyPost.objects.filter(favourites = request.user)
    user_menu = menu.copy()
    if not request.user.has_perms(['sforum.add_companypost', 'sforum.change_companypost', 'sforum.change_companypost']):
        user_menu = menu2.copy()
    return render(request, 'sforum/favourites.html',{'favs':favs, 'menu': user_menu,})


def in_process(request):
    user_menu = menu.copy()
    if not request.user.groups.filter(name="company"):
        user_menu = menu2.copy()
    return render(request, 'sforum/in_process.html', {'menu': user_menu,})
def email_response(request):
    user_menu = menu.copy()
    if not request.user.groups.filter(name="company"):
        user_menu = menu2.copy()
    return render(request, 'sforum/email_response.html', {'menu': user_menu,})
def contacts(request):
    user_menu = menu.copy()
    if not request.user.groups.filter(name="company"):
        user_menu = menu2.copy()
    return render(request, 'sforum/contacts.html', {'menu': user_menu,})
def agreement(request):
    user_menu = menu.copy()
    if not request.user.groups.filter(name="company"):
        user_menu = menu2.copy()
    return render(request, 'sforum/agreement.html', {'menu': user_menu,})
def about(request):
    user_menu = menu.copy()

    return render(request, 'sforum/about.html', {'menu': user_menu,})
def pageNotFound(request, exception):
    return render(request, 'sforum/404.html',)
    # return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Введите вашу почту", max_length=254)

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput, min_length=8
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput, min_length=8
    )



def custom_password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = get_user_model().objects.filter(email=email).first()
            if user:
                # Генерация токена и кодирования данных
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())

                # Ссылка на сброс пароля
                reset_link = f"{request.scheme}://{get_current_site(request).domain}{reverse('custom_password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"


                # Отправка письма с ссылкой
                subject = "Сброс пароля"
                message = render_to_string(
                    "sforum/custom_password_reset_email.html",
                    {"reset_link": reset_link}
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return render(request, "sforum/custom_password_reset_done.html")

    else:
        form = PasswordResetForm()

    return render(request, "sforum/custom_password_reset_form.html", {"form": form})


def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("custom_password_reset_complete")
        else:
            form = CustomSetPasswordForm(user)

        return render(request, "sforum/custom_password_reset_confirm.html", {
            "form": form,
            "uidb64": uidb64,
            "token": token
        })
    else:
        return render(request, "sforum/custom_password_reset_invalid.html")

def custom_password_reset_complete(request):
    return render(request, "sforum/custom_password_reset_complete.html",)
def show_profiles(request):
    user_menu = menu.copy()
    if not request.user.groups.filter(name="company").exists():
        user_menu = menu2.copy()
    company_profiles = Profile.objects.filter(user__groups__name="Компания")
    user_profiles = Profile.objects.filter(user__groups__name="Пользователь")

    return render(request, 'sforum/show_profiles.html', {
        'menu': user_menu,
        'company_profiles': company_profiles,
        'user_profiles': user_profiles,
    })
