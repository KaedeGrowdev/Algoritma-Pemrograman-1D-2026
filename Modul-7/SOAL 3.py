undangan = set()
webinar_a = set()
webinar_b = set()

print("Isi daftar undangan (ketik 'selesai' untuk berhenti)")
while True:
    nama = input("Nama undangan: ")
    if nama == "selesai":
        break
    undangan.add(nama)

print("Isi peserta Webinar A (ketik 'selesai' untuk berhenti)")
while True:
    nama = input("Nama peserta A: ")
    if nama == "selesai":
        break
    webinar_a.add(nama)

print("Isi peserta Webinar B (ketik 'selesai' untuk berhenti)")
while True:
    nama = input("Nama peserta B: ")
    if nama == "selesai":
        break
    webinar_b.add(nama)


semua_peserta = webinar_a.union(webinar_b)             
hadir_keduanya = webinar_a.intersection(webinar_b)     
hanya_satu = webinar_a.symmetric_difference(webinar_b)
tidak_hadir = undangan.difference(semua_peserta)      

print()
print("Semua peserta          :", semua_peserta)
print("Hadir di kedua webinar :", hadir_keduanya)
print("Hanya di satu webinar  :", hanya_satu)
print("Undangan tidak hadir   :", tidak_hadir)
