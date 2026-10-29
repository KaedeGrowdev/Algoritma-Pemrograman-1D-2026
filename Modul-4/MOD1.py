baris = int(input("Jumlah baris lampu: "))
lampu = int(input("Jumlah lampu per baris: "))
angka = 1

for b in range(1, baris + 1):
    print(f"Baris {b}")
    for l in range(1, lampu + 1):
        if l % 3 == 0:
            print(f"  Lampu {angka}: mengalami gangguan")
        else:
            print(f"  Lampu {angka}: berfungsi normal")
        angka += 1
print("Periksa sumber listrik utama taman.") if l % 3 == 0 else print("Listrik aman")