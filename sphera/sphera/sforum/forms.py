from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, AuthenticationForm, UsernameField
from django.db.models import Q
from django.forms import SelectDateWidget

from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth.models import Group
User = get_user_model()



class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = CompanyPost
        fields = ['title', 'photo','pic_1', 'pic_2', 'pic_3', 'address','metro', 'content', 'phone', 'cat', 'latitude', 'longitude', ]

class AddNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = CompanyNews
        fields = ['title','photo','content',]


class AddReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Reviews
        fields = ['title','photo','event_option','content',]


class AddEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Events
        fields = ['title','photo','content','latitude', 'longitude']

class UserCreationForm(UserCreationForm):
    username = UsernameField(label="Имя")
    email=forms.EmailField(label= 'Почта', max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email'}))
    groups = forms.ModelChoiceField(queryset=Group.objects.filter(Q(name = "Компания") | Q(name = "Пользователь")), label="Регистрируем как:")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = None#forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields =('username', 'email', 'phone')
        field_classes = {"username": UsernameField}

class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields = ('body',)

class AddNewsCommentForm(forms.ModelForm):
    class Meta:
        model= NewsComments
        fields = ('body',)

class AddBannerPhotoForm(forms.ModelForm):
    class Meta:
        model = BannerPhoto
        fields = ('img',)

class AddBannerVideoForm(forms.ModelForm):
    class Meta:
        model = BannerVideo
        fields = ('video',)

        # 'comment_author'

        # widgets={'comment_author':forms.TextInput(attrs={'class':'form-control', 'value':"", "id":"notshow", "type":'hidden'}),}



# class CustomUserRegistrationForm(UserCreationForm):
#
#     username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
#     groups=forms.ModelChoiceField(queryset=Group.objects.all())
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email", 'groups', 'number', "password1", "password2",)

# class CustomUserAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
# class ProfileCreationForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('bio','profile_pic', "profile_pic_1", "profile_pic_2", "profile_pic_3", "tg_url", "vk_url", "web_site_url", "instagram_url",)

