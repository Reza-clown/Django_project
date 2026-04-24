from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin

from .models import Kategori, Tugas, Notifikasi, Message

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama_kategori']
    search_fields = ['nama_kategori']

@admin.register(Tugas)
class TugasAdmin(admin.ModelAdmin):
    list_display = ['judul', 'user', 'kategori', 'status', 'deadline']
    list_filter = ['status', 'kategori', 'deadline']
    search_fields = ['judul', 'deskripsi']
    date_hierarchy = 'deadline'
    raw_id_fields = ['user', 'kategori']

@admin.register(Notifikasi)
class NotifikasiAdmin(admin.ModelAdmin):
    list_display = ['pesan', 'user', 'status_baca', 'created_at']
    list_filter = ['status_baca']
    search_fields = ['pesan', 'user__username']
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'isi_pesan', 'created_at']
    list_filter = ['sender', 'receiver']
    search_fields = ['isi_pesan', 'sender__username', 'receiver__username']
    date_hierarchy = 'created_at'
    raw_id_fields = ['sender', 'receiver']


