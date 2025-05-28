from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('oxidation/', views.oxidation, name='oxidation'),
    path('photo/', views.photo, name='photo'),
    path('etching/', views.etching, name='etching'),
    path('deposition/', views.deposition, name='deposition'),
    path("ai_chat/", views.ai_chat, name="ai_chat")
]