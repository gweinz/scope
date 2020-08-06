from django.contrib import admin

# Register your models here.

from .models import Bet, Match

admin.site.register(Bet)
admin.site.register(Match)

