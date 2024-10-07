from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Categories)
admin.site.register(CompanyNews)
admin.site.register(CompanyPost)
admin.site.register(User)
admin.site.register(Reviews)
admin.site.register(BannerPhoto)
admin.site.register(BannerVideo)

# admin.site.register(CustomUser)