from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index',views.index, name='home'),
    url(r'^analysis', views.analysis, name='analysis'),
    url(r'^upload_script',views.upload_file, name='upload'),
    url(r'^results/json',views.resultsJson, name='results'),
]