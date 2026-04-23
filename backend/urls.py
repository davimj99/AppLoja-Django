from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('', include('core.urls')),              # 👈 HOME
    path('produtos/', include('produtos.urls')), # 👈 CATÁLOGO
    path('carrinho/', include('carrinho.urls')),
    path('painel/', include('pedidos.urls')),
    path('admin/', admin.site.urls),
]
handler404 = views.error404
handler500 = views.error500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)