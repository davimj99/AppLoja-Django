from django.urls import path
from . import views
from core.views import index , contato , produto 


urlpatterns = [
    path('', views.index , name='index'),
    path('contato/', views.contato, name='contato'),
    path('produto/<int:pk>/', views.produto, name='produto'),
    path('carrinho/', views.carrinho_view, name='carrinho'),
]

