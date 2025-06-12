from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('phones/', views.phone_list, name='phone_list'),
    path('phones/<int:pk>/', views.phone_detail, name='phone_detail'),
    path('compare/', views.compare, name='compare'),
    path('how-to-use/', views.how_to_use, name='how_to_use'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('admin/backup/', views.backup, name='backup'),
    path('admin/restore/', views.restore, name='restore'),
] 