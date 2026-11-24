jumlah_A = 0
jumlah_B = 0
jumlah_C = 0
jumlah_D = 0
jumlah_E = 0
total = 0

tertinggi = 0
nama_tertinggi = ""
terendah = 100
nama_terendah = ""

for i in range(10):
    print("Mahasiswa ke-", i + 1)
    nama = input("Nama  : ")
    tugas = float(input("Nilai tugas : "))
    uts = float(input("Nilai UTS   : "))
    uas = float(input("Nilai UAS   : "))

    akhir = tugas * 0.3 + uts * 0.3 + uas * 0.4

    if akhir >= 85:
        kategori = "A"
        jumlah_A = jumlah_A + 1
    elif akhir >= 75:
        kategori = "B"
        jumlah_B = jumlah_B + 1
    elif akhir >= 65:
        kategori = "C"
        jumlah_C = jumlah_C + 1
    elif akhir >= 50:
        kategori = "D"
        jumlah_D = jumlah_D + 1
    else:
        kategori = "E"
        jumlah_E = jumlah_E + 1

    total = total + akhir

    if akhir > tertinggi:
        tertinggi = akhir
        nama_tertinggi = nama

    if akhir < terendah:
        terendah = akhir
        nama_terendah = nama

    print("Nama        :", nama)
    print("Nilai tugas :", tugas)
    print("Nilai UTS   :", uts)
    print("Nilai UAS   :", uas)
    print("Nilai akhir :", akhir)
    print("Kategori    :", kategori)
    print()

rata_rata = total / 10

print("Jumlah nilai A :", jumlah_A)
print("Jumlah nilai B :", jumlah_B)
print("Jumlah nilai C :", jumlah_C)
print("Jumlah nilai D :", jumlah_D)
print("Jumlah nilai E :", jumlah_E)
print("Nilai tertinggi :", tertinggi, "oleh", nama_tertinggi)
print("Nilai terendah  :", terendah, "oleh", nama_terendah)
print("Rata-rata nilai :", rata_rata)