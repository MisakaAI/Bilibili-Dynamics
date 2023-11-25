from django.contrib import admin

# Register your models here.
from .models import followings
admin.site.register(followings)
from .models import follow_class
admin.site.register(follow_class)