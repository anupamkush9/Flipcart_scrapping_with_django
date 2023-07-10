from django.urls import path
from . import views


urlpatterns = [
    path("", views.search_key, name='search'),
    path("show-data", views.show_data, name='show-data'),
    path("show-individual/<int:id>",views.show_individual,name='show-individual')
]
    
