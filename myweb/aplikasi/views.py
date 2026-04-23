import json
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from .models import Tugas, Kategori


# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username atau password salah.')
    return render(request, 'Aplikasi/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Password tidak cocok.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah dipakai.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('index')
    return render(request, 'Aplikasi/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@login_required(login_url='login')
def index(request):
    tugas_qs = Tugas.objects.filter(user=request.user)
    total = tugas_qs.count()
    selesai = tugas_qs.filter(status='selesai').count()
    pending = tugas_qs.filter(status='pending').count()
    progress = round((selesai / total * 100) if total > 0 else 0)

    # Data per kategori untuk pie chart (dikirim ke template sebagai JSON)
    per_kategori = (
        tugas_qs.values('kategori__nama_kategori')
        .annotate(jumlah=Count('id'))
        .order_by('-jumlah')
    )

    context = {
        'total': total,
        'selesai': selesai,
        'pending': pending,
        'progress': progress,
        'per_kategori': list(per_kategori),
    }
    return render(request, 'Aplikasi/index.html', context)


# ─── CHARTS ──────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def charts(request):
    tugas_qs = Tugas.objects.filter(user=request.user)

    # ── 1. Donut: Pending vs Selesai ─────────────────────────────────────────
    selesai_count = tugas_qs.filter(status='selesai').count()
    pending_count = tugas_qs.filter(status='pending').count()
    donut_data = {
        'labels': ['Selesai', 'Pending'],
        'data':   [selesai_count, pending_count],
        'colors': ['#1cc88a', '#f6c23e'],
    }

    # ── 2. Bar: Tugas dibuat per bulan (12 bulan terakhir) ───────────────────
    today = date.today()
    # Buat list 12 bulan terakhir
    months = []
    for i in range(11, -1, -1):
        # Hitung bulan mundur dari bulan ini
        month_date = (today.replace(day=1) - timedelta(days=1) * (i * 30))
        months.append(month_date.replace(day=1))

    bar_raw = (
        tugas_qs
        .annotate(bulan=TruncMonth('created_at'))
        .values('bulan')
        .annotate(jumlah=Count('id'))
        .order_by('bulan')
    )
    bar_map = {item['bulan'].date().replace(day=1): item['jumlah'] for item in bar_raw if item['bulan']}

    BULAN_ID = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
    bar_labels = [f"{BULAN_ID[m.month - 1]} {m.year}" for m in months]
    bar_values = [bar_map.get(m, 0) for m in months]

    bar_data = {
        'labels': bar_labels,
        'data':   bar_values,
    }

    # ── 3. Line/Area: Tugas dibuat per hari (30 hari terakhir) ───────────────
    since = today - timedelta(days=29)
    area_raw = (
        tugas_qs
        .filter(created_at__date__gte=since)
        .annotate(hari=TruncDate('created_at'))
        .values('hari')
        .annotate(jumlah=Count('id'))
        .order_by('hari')
    )
    area_map = {item['hari']: item['jumlah'] for item in area_raw}

    area_labels = []
    area_values = []
    for i in range(30):
        d = since + timedelta(days=i)
        area_labels.append(d.strftime('%d %b'))
        area_values.append(area_map.get(d, 0))

    area_data = {
        'labels': area_labels,
        'data':   area_values,
    }

    # ── 4. Per kategori (untuk card ringkasan) ────────────────────────────────
    per_kategori = list(
        tugas_qs
        .values('kategori__nama_kategori')
        .annotate(
            total=Count('id'),
            selesai=Count('id', filter=Q(status='selesai')),
        )
        .order_by('-total')
    )

    context = {
        'donut_data': json.dumps(donut_data),
        'bar_data':   json.dumps(bar_data),
        'area_data':  json.dumps(area_data),
        'per_kategori': per_kategori,
        'total_tugas': tugas_qs.count(),
    }
    return render(request, 'Aplikasi/charts.html', context)


# ─── CRUD TUGAS ──────────────────────────────────────────────────────────────

@login_required(login_url='login')
def tables(request):
    tugas_list = Tugas.objects.filter(user=request.user).select_related('kategori')
    kategori_list = Kategori.objects.all()
    return render(request, 'Aplikasi/tables.html', {
        'tugas_list': tugas_list,
        'kategori_list': kategori_list,
    })


@login_required(login_url='login')
def tugas_tambah(request):
    if request.method == 'POST':
        judul = request.POST.get('judul', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()
        deadline = request.POST.get('deadline')
        kategori_nama = request.POST.get('kategori', '').strip()

        if not judul or not deadline:
            messages.error(request, 'Judul dan deadline wajib diisi.')
            return redirect('tables')

        kategori = None
        if kategori_nama:
            kategori, _ = Kategori.objects.get_or_create(nama_kategori=kategori_nama)

        Tugas.objects.create(
            user=request.user,
            judul=judul,
            deskripsi=deskripsi,
            deadline=deadline,
            kategori=kategori,
            status='pending',
        )
        messages.success(request, f'Tugas "{judul}" berhasil ditambahkan.')
    return redirect('tables')


@login_required(login_url='login')
def tugas_edit(request, pk):
    tugas = get_object_or_404(Tugas, pk=pk, user=request.user)
    if request.method == 'POST':
        judul = request.POST.get('judul', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()
        deadline = request.POST.get('deadline')
        kategori_nama = request.POST.get('kategori', '').strip()
        status = request.POST.get('status', 'pending')

        if not judul or not deadline:
            messages.error(request, 'Judul dan deadline wajib diisi.')
            return redirect('tables')

        kategori = None
        if kategori_nama:
            kategori, _ = Kategori.objects.get_or_create(nama_kategori=kategori_nama)

        tugas.judul = judul
        tugas.deskripsi = deskripsi
        tugas.deadline = deadline
        tugas.kategori = kategori
        tugas.status = status
        tugas.save()
        messages.success(request, f'Tugas "{judul}" berhasil diperbarui.')
    return redirect('tables')


@login_required(login_url='login')
def tugas_hapus(request, pk):
    tugas = get_object_or_404(Tugas, pk=pk, user=request.user)
    if request.method == 'POST':
        nama = tugas.judul
        tugas.delete()
        messages.success(request, f'Tugas "{nama}" berhasil dihapus.')
    return redirect('tables')


@login_required(login_url='login')
def tugas_toggle(request, pk):
    """Toggle status pending ↔ selesai via AJAX atau redirect."""
    tugas = get_object_or_404(Tugas, pk=pk, user=request.user)
    tugas.status = 'selesai' if tugas.status == 'pending' else 'pending'
    tugas.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': tugas.status})
    return redirect('tables')
