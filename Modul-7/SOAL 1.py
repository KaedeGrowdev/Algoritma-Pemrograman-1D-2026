tugas = {} 

while True:
    print()
    print("===== MENU TO-DO LIST =====")
    print("1. Tambah tugas")
    print("2. Tampilkan semua tugas")
    print("3. Tandai tugas selesai")
    print("4. Hapus tugas")
    print("5. Lihat jumlah tugas selesai dan belum")
    print("0. Keluar")
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        if nama in tugas:
            print("Tugas itu sudah ada.")
        else:
            tugas[nama] = "Belum selesai"
            print("Tugas berhasil ditambahkan.")

    elif pilihan == "2":
        if len(tugas) == 0:
            print("Belum ada tugas.")
        else:
            for nama in tugas:
                print("Nama", nama, ":", tugas[nama])

    elif pilihan == "3":
        nama = input("Nama tugas yang sudah selesai: ")
        if nama in tugas:          
            tugas[nama] = "Selesai"
            print("Tugas ditandai selesai.")
        else:
            print("Tugas tidak ditemukan.")

    elif pilihan == "4":
        nama = input("Nama tugas yang dihapus: ")
        if nama in tugas:         
            del tugas[nama]
            print("Tugas dihapus.")
        else:
            print("Tugas tidak ditemukan.")

    elif pilihan == "5":
        selesai = 0
        belum = 0
        for nama in tugas:
            if tugas[nama] == "Selesai":
                selesai = selesai + 1
            else:
                belum = belum + 1
        print("Tugas selesai       :", selesai)
        print("Tugas belum selesai :", belum)

    elif pilihan == "0":
        print("Terima kasih!")
        break

    else:
        print("Pilihan tidak valid.")
