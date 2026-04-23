from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrinho, name='carrinho'),
    path('add/<int:produto_id>/', views.adicionar_ao_carrinho),
    path('checkout/', views.checkout),
]