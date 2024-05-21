from django.urls import path, re_path
from creditcard import views

urlpatterns = [
    re_path('add_card', views.add_card),
    re_path('show_cards', views.show_cards),
]
