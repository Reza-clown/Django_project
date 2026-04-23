# NUGASin Model Migration TODO

**Status: [0/5]**

### Phase 1: Replace models.py [1/1] ✅
- [x] SIAKAD + old Tugas → new Tugas w/ prioritas choices + sisa_waktu property

### Phase 2: Replace admin.py [1/1] ✅
- [x] TugasAdmin w/ list_display=['nama_tugas','deadline','prioritas','status','sisa_waktu','user'] + filters/search

### Phase 3: Database Cleanup [0/3]
- [ ] Delete migrations/*
- [ ] Delete db.sqlite3
- [ ] python manage.py makemigrations aplikasi

### Phase 4: Migrate [0/1]
- [ ] python manage.py migrate

### Phase 5: Verify [0/1]
- [ ] Check admin + test data

