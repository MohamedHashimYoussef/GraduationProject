from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('' , views.index , name='index'),
    path('modelskin/' , views.skin , name='skin') ,
path('modelbrain/' , views.brain , name='brain'),
path('modelmalaria/' , views.malaria , name='malaria')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
