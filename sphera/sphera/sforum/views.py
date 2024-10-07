import json
import os

# from IPython.terminal.shortcuts.auto_match import braces
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

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
    {"title": "ЗАВЕДЕНИЯ", 'url_name': 'show_venues'},



]
menu2=[
    # {"title": "О нас", 'url_name':'about'}
    {"title": "ИЗБРАННОЕ", 'url_name': 'show_fav'},
    # {"title": "КОНТАКТЫ", 'url_name': 'contacts'},
    {"title": "ЗАВЕДЕНИЯ", 'url_name': 'show_venues'},]

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
    banners = BannerPhoto.objects.all()[:1]
    banners_video = BannerVideo.objects.all()
    reviews = Reviews.objects.all()[:4]
    posts=CompanyPost.objects.all()[:5]
    news=CompanyNews.objects.all()[:8]
    comments = Comments.objects.all()[:10]
    news_comments = NewsComments.objects.all()[:10]
    # cats = Categories.objects.all()
    return render(request, 'sforum/index.html', {'posts':posts, 'menu': user_menu, 'news':news,'reviews':reviews, 'comments':comments, "banners_photo":banners,"news_comments":news_comments,"banners_video":banners_video,})
class ShowProfile(DataMixin, DetailView):
    model = Profile
    template_name = 'sforum/profile.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        page_user_venues = CompanyPost.objects.filter(company_name_id=page_user.user.id)
        page_user_news = CompanyNews.objects.filter(company_name_id=page_user.user.id)
        print(page_user_venues)
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
    fields = ('bio', 'profile_pic', 'web_site_url',  'instagram_url', 'vk_url', 'tg_url',)
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
    fields = ('bio', 'profile_pic', 'web_site_url', 'instagram_url','vk_url', 'tg_url')

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
        # print(ordering)
        return ordering

class ShowNews(DataMixin, ListView):
    model = CompanyNews
    template_name = 'sforum/news.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="home")
        return dict(list(context.items()) + list(c_def.items()))

class ShowReviews(DataMixin, ListView):
    model = Reviews
    template_name = 'sforum/show_reviews.html'
    context_object_name = 'reviews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="home")
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
    model= CompanyPost
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
        # return JsonResponse(list(CompanyPost.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).values()), safe=False)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Category - " + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))





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
            user.save()

            user_group = Group.objects.get(name=form.cleaned_data['groups'])
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
# def likeview(request, slug):
#     post=get_object_or_404(CompanyNews, id=request.POST.get('post_id'))
#     liked=False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         liked=False
#     else:
#         post.likes.add(request.user)
#         liked=True
#     return HttpResponseRedirect(reverse( 'show_new', args=[str(slug)]))

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
