from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produto/<int:pk>/', views.produto_detail, name='produto'),
]