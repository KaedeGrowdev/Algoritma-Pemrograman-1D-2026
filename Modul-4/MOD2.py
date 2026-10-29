total = 0
for hari in range(1, 8):
    print(f"Hari ke-{hari}")
    gaji = 100000

    while True:
        lembur = int(input("Jam lembur (0-8): "))
        if lembur in (0, 1, 2, 3, 5, 4, 6, 7, 8):
            break
        elif lembur > 8:
            print("Jumlah lembur melebihi batas yang ditentukan!")
        else:
            print("Jam lembur tidak sesuai ketentuan, ulangi!")
    if lembur == 0:
        upah = 0
    elif lembur <= 3:
        upah = lembur * 25000
    elif lembur == 4:
        upah = 100000
    elif lembur == 5:
        upah = 125000
    elif lembur == 6:
        upah = 200000
    elif lembur == 7:
        upah = 225000
    else:
        upah = 300000

    malam = input("Shift malam? (y/n): ")
    if malam == "y":
        bonus = 50000
    else:
        bonus = 0
    total += gaji + upah + bonus
print(f"Total gaji mingguan: Rp{total:}")