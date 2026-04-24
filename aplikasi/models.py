from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama_kategori
    
    class Meta:
        verbose_name_plural = "Kategori"

class Tugas(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('selesai', 'Selesai'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.judul
    
    class Meta:
        verbose_name_plural = "Tugas"
        ordering = ['-deadline']

class Notifikasi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pesan = models.TextField()
    status_baca = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notif {self.user.username}: {self.pesan[:50]}"
    
    class Meta:
        verbose_name_plural = "Notifikasi"
        ordering = ['-created_at']

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    isi_pesan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"
    
    class Meta:
        verbose_name_plural = "Pesan"
        ordering = ['-created_at']


