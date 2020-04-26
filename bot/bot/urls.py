from django.contrib import admin
from django.urls import path
import botvk.views as bot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('botVK/', bot.bot)
]
