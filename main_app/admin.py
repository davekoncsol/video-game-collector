from django.contrib import admin

from .models import Game, Playing, Char, Photo

# Register your models here.

admin.site.register(Game)
admin.site.register(Playing)
admin.site.register(Char)
admin.site.register(Photo)
