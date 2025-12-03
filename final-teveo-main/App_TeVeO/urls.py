
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('camaras', views.camaras, name='camaras'),
    path('comentario', views.create_comentario, name='comentario'),
    path('configuracion', views.configuracion, name='configuracion'),
    path('help', views.help, name='help'),
    path('logout', views.logout_view, name='logout'),
    path('json/<str:id>', views.camara_json, name='camara_json'),
    path('dynamic.css', views.get_css, name='dynamic_css'),
    path('<str:id_camara>dyn', views.dynamic, name='dynamic'),
    path('<str:id>', views.camara, name='camara'),
] + static(settings.STATIC_URL)
