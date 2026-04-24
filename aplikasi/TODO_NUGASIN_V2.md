# NUGASin V2 Model Migration TODO

**Status: [0/6]**

### Phase 1: Replace models.py [1/1] ✅
- [x] Added Kategori, Tugas (w/ status choices), Notifikasi, Message

### Phase 2: Admin registration [1/1] ✅
- [x] KategoriAdmin, TugasAdmin, NotifikasiAdmin, MessageAdmin registered

### Phase 3: Cleanup DB [3/3] ✅
- [x] rmdir aplikasi\migrations + recreate __init__.py
- [x] del db.sqlite3
- [x] makemigrations aplikasi → 0001_initial.py

### Phase 4: Migrate [1/1] ✅
- [x] migrate aplikasi executed

### Phase 5: Superuser [0/1]
- [ ] createsuperuser

### Phase 6: Verify [0/1]
- [ ] Admin UI + test data

