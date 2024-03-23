from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('snps/', views.snps, name='snps'),
    path('snps/annotations', views.annotations, name='annotations'),
    path('snps/search', views.save_snp, name='save_snp'),
]
