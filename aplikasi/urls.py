from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Halaman utama
    path('', views.index, name='index'),
    path('charts/', views.charts, name='charts'),
    path('tables/', views.tables, name='tables'),

    # CRUD Tugas
    path('tugas/tambah/', views.tugas_tambah, name='tugas_tambah'),
    path('tugas/edit/<int:pk>/', views.tugas_edit, name='tugas_edit'),
    path('tugas/hapus/<int:pk>/', views.tugas_hapus, name='tugas_hapus'),
    path('tugas/toggle/<int:pk>/', views.tugas_toggle, name='tugas_toggle'),
]
