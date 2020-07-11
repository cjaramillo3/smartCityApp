from django.urls import path
from smart_cityapp import views

app_name = 'smart_cityapp'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('economia/',views.economia, name = 'economia'),
    path('turismo/',views.turismo, name = 'turismo'),
    path('seguridad/',views.seguridad, name = 'seguridad'),
    path('trafico/',views.trafico, name = 'trafico'),
    path('ambiente/',views.ambiente, name = 'ambiente'),
    path('salud/',views.salud, name = 'salud'),
]
