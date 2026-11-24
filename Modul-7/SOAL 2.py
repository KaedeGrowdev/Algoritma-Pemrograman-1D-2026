playlist = {} 

while True:
    print()
    print("===== MENU PLAYLIST =====")
    print("1. Buat playlist")
    print("2. Tambah lagu ke playlist")
    print("3. Tampilkan semua playlist")
    print("4. Cari lagu")
    print("5. Hapus lagu dari playlist")
    print("6. Hapus playlist")
    print("0. Keluar")
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        nama = input("Nama playlist: ")
        if nama in playlist:
            print("Playlist sudah ada.")
        else:
            playlist[nama] = {} 
            print("Playlist dibuat.")

    elif pilihan == "2":
        nama = input("Nama playlist: ")
        if nama in playlist:
            judul = input("Judul lagu: ")
            penyanyi = input("Penyanyi: ")
            playlist[nama][judul] = penyanyi
            print("Lagu ditambahkan.")
        else:
            print("Playlist tidak ditemukan.")

    elif pilihan == "3":
        if len(playlist) == 0:
            print("Belum ada playlist.")
        else:
            for nama in playlist:
                print("Playlist:", nama)
                if len(playlist[nama]) == 0:
                    print("   (kosong)")
                for judul in playlist[nama]:
                    print("   -", judul, "oleh", playlist[nama][judul])

    elif pilihan == "4":
        cari = input("Judul lagu yang dicari: ")
        ketemu = False
        for nama in playlist:
            if cari in playlist[nama]:
                print("Ditemukan:", cari, "oleh", playlist[nama][cari],
                      "(di playlist", nama + ")")
                ketemu = True
        if ketemu == False:
            print("Lagu tidak ditemukan.")

    elif pilihan == "5":
        nama = input("Nama playlist: ")
        if nama in playlist:
            judul = input("Judul lagu yang dihapus: ")
            if judul in playlist[nama]:
                del playlist[nama][judul]
                print("Lagu dihapus.")
            else:
                print("Lagu tidak ada di playlist itu.")
        else:
            print("Playlist tidak ditemukan.")

    elif pilihan == "6":
        nama = input("Nama playlist yang dihapus: ")
        if nama in playlist:
            del playlist[nama]
            print("Playlist dihapus.")
        else:
            print("Playlist tidak ditemukan.")

    elif pilihan == "0":
        print("Terima kasih!")
        break

    else:
        print("Pilihan tidak valid.")
