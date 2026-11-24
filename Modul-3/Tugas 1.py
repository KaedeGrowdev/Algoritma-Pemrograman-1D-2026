jumlah = 0
total = 0
terjauh = 0
total_jarak = 0
tarif = 0

while True:
    jarak = int(input("Masukkan Jarak (0 untuk selesai): "))
    if jarak == 0:
        break
    if jarak < 0:
        print("Jarak tak valid")
        continue

    jumlah = jumlah + 1
    if jarak < 5:
        tarif = 3000
    elif jarak < 15:
        tarif = 3000 + 1000 * (jarak - 5)
    else:
        tarif = 13000 + 500 * (jarak - 15)

    if jumlah % 5 == 0:
        tarif *= 0.5
        print("Diskon 50%")

    print("Tarif Rp:", tarif)
    total += tarif
    total_jarak += jarak

    if jarak > terjauh:
        terjauh = jarak

print("Jumlah penumpang:", jumlah)
print("Total Pendapatan: Rp", total)
print("Jarak terjauh:", terjauh, "Km")
if jumlah > 0:
    print(f"Rata-rata jarak: {total_jarak / jumlah}")
else:
    print("Rata-rata jarak : 0 Km") 