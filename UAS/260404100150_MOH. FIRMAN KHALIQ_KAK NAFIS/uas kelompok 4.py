from datetime import date

# ======================= MAIN INPUT =======================
PIN_ADMIN = "1234"
MAKS_PERCOBAAN_PIN = 3
PERSEN_JAMINAN = 20
PERSEN_RUSAK = 80
TIER_DISKON = ((7, 20), (6, 15), (3, 5)) 
KONDISI_VALID = ("baik", "rusak")
HINT_BATAL = "(ketik 'kembali' untuk batal)"
PESAN_BATAL = "  Dibatalkan, kembali ke menu sebelumnya."


# ======================= DATA =======================
def data_awal():
    return {
        "alat": {
            "1": {"nama": "Tenda", "harga_sewa": 30000, "harga_barang": 500000, "stok": 5},
            "2": {"nama": "Carrier 65L", "harga_sewa": 20000, "harga_barang": 400000, "stok": 4},
            "3": {"nama": "Sepatu Hiking", "harga_sewa": 100000, "harga_barang": 3000000, "stok": 2},
        },
        "sewa": {},        
        "riwayat": [],     
        "pendapatan": 0, 
        "counter_alat": 3,
        "counter_kode": 0,
    }


db = data_awal()


# ======================= HELPER 1 =======================
def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return "kembali"
        if teks != "":
            return teks
        print(f"  Tidak boleh kosong. {HINT_BATAL}")


def input_pilihan(pesan, pilihan):
    while True:
        teks = input(pesan).strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return "kembali"
        if teks.lower() in pilihan:
            return teks.lower()
        print(f"  Isi salah satu: {' / '(pilihan)}.")


def input_tanggal(pesan):
    """Enter = hari ini. Format lain selain YYYY-MM-DD ditolak."""
    while True:
        teks = input(pesan).strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return "kembali"
        if teks == "":
            return date.today()
        if len(teks) == 10:
            try:
                return date.fromisoformat(teks)
            except ValueError:
                pass
        print("  Format tanggal salah (contoh: 2026-11-28).")


# ======================= HELPER 2=======================
def rp(n):
    return f"Rp{n:,.0f}".replace(",", ".")


def tabel_alat():
    if not db["alat"]:
        print("  (Belum ada alat)")
        return
    print(f"\n  {'ID':<4}{'Nama Alat':<20}{'Harga Sewa/hari':>17}{'Harga Barang':>16}{'Stok':>6}")
    print("  " + "-" * 63)
    for id_alat, a in db["alat"].items():
        print(f"  {id_alat:<4}{a['nama']:<20}{rp(a['harga_sewa']):>17}"
              f"{rp(a['harga_barang']):>16}{a['stok']:>6}")


def pilih_alat(aksi):
    """Tampilkan tabel lalu minta ID alat sampai valid. Return ID, atau 'kembali'."""
    tabel_alat()
    while True:
        id_alat = input(f"\n  ID alat yang {aksi} {HINT_BATAL}: ").strip()
        if id_alat.lower() == "kembali":
            print(PESAN_BATAL)
            return "kembali"
        if id_alat in db["alat"]:
            return id_alat
        print("  ID tidak ditemukan.")


def bayar(total, keterangan="Total bayar"):
    """Return True kalau lunas, False kalau user membatalkan."""
    while True:
        print(f"\n  {keterangan}: {rp(total)}")
        teks = input(f"  Masukkan uang {HINT_BATAL}: Rp").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return False
        try:
            uang = int(teks)
        except ValueError:
            print(f"  Input harus angka bulat. {HINT_BATAL}")
            continue
        if uang >= total:
            if uang > total:
                print(f"  Kembalian: {rp(uang - total)}")
            print("  Pembayaran berhasil.")
            return True
        print(f"  Uang kurang {rp(total - uang)}. Pembayaran ditolak, silakan input lagi.")


def hitung_diskon(hari):
    for min_hari, persen in TIER_DISKON:
        if hari >= min_hari:
            return persen
    return 0


def hitung_denda_telat(subtotal, hari_telat):
    """1 hari telat = 3%, lalu naik 2% tiap kelipatan 2 hari (hari 2, 4, 6, ...)."""
    if hari_telat <= 0:
        return 0, 0
    persen = 3 + 2 * (hari_telat // 2)
    return persen, subtotal * persen // 100


def kode_baru():
    db["counter_kode"] += 1
    return f"SW-{db['counter_kode']:04d}" #Contoh 0001


def cetak_riwayat(r):
    print(f"\n  Kode        : {r['kode']}")
    print(f"  Penyewa     : {r['nama']}")
    print(f"  Alat        : {r['nama_alat']} x{r['jumlah']} ({r['hari']} hari)")
    print(f"  Tgl sewa    : {r['tgl_sewa']}   Kembali: {r['tgl_kembali']}")
    print(f"  Biaya sewa  : {rp(r['total_sewa'])} (diskon {r['diskon']}%)")
    print(f"  Denda telat : {rp(r['denda_telat'])}   Denda rusak: {rp(r['denda_rusak'])}")
    print(f"  Status alat : {r['kondisi']}   Jaminan dikembalikan: {rp(r['jaminan'])}")


def cetak_sewa_aktif(kode, s):
    print(f"\n  Kode        : {kode}")
    print(f"  Penyewa     : {s['nama']}")
    print(f"  Alat        : {s['nama_alat']} x{s['jumlah']} ({s['hari']} hari)")
    print(f"  Tgl sewa    : {s['tgl_sewa']}   Jatuh tempo: {s['jatuh_tempo']}")
    print(f"  Biaya sewa  : {rp(s['total_sewa'])} (diskon {s['diskon']}%)")
    print(f"  Status      : belum dikembalikan   Jaminan: {rp(s['jaminan'])}")


def jalankan_menu(judul, menu, tampilkan_alat=False, teks_keluar="Kembali"):
    while True:
        print(f"\n===== {judul} =====")
        if tampilkan_alat:
            tabel_alat()
            print()
        for nomor, (nama_menu, _) in menu.items():
            print(f"  {nomor}. {nama_menu}")
        print(f"  0. {teks_keluar}")
        pilih = input("Pilih: ").strip()
        if pilih == "0":
            return
        elif pilih in menu:
            menu[pilih][1]()
        else:
            print("  Pilihan tidak valid.")


# ======================= ADMIN =======================
def admin_tambah_alat():
    print("  (ketik 'kembali' kapan saja untuk batal)")
    nama = input_teks("  Nama alat: ")
    if nama == "kembali":
        return

    while True:
        teks = input("  Harga sewa per hari: Rp").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1  
        if angka >= 1:
            harga_sewa = angka
            break
        print(f"  Harga harus angka bulat, minimal 1. {HINT_BATAL}")

    while True:
        teks = input("  Harga barang: Rp").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1  
        if angka >= 1:
            harga_barang = angka
            break
        print(f"  Harga harus angka bulat, minimal 1. {HINT_BATAL}")

    while True:
        teks = input("  Stok: ").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1  
        if angka >= 0:
            stok = angka
            break
        print(f"  Stok harus angka bulat, minimal 0. {HINT_BATAL}")

    db["counter_alat"] += 1
    db["alat"][str(db["counter_alat"])] = {
        "nama": nama, "harga_sewa": harga_sewa, "harga_barang": harga_barang, "stok": stok}
    print("  Alat berhasil ditambahkan.")


def admin_ubah_alat():
    id_alat = pilih_alat("diubah")
    if id_alat == "kembali":
        return
    a = db["alat"][id_alat]

    while True:
        teks = input(f"  Harga sewa baru (lama {rp(a['harga_sewa'])}): Rp").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1  
        if angka >= 1:
            harga_baru = angka
            break
        print(f"  Harga harus angka bulat, minimal 1. {HINT_BATAL}")

    while True:
        teks = input(f"  Stok baru (lama {a['stok']}): ").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1  
        if angka >= 0:
            stok_baru = angka
            break
        print(f"  Stok harus angka bulat, minimal 0. {HINT_BATAL}")

    a["harga_sewa"] = harga_baru
    a["stok"] = stok_baru
    print("  Harga dan stok berhasil diubah.")


def admin_hapus_alat():
    id_alat = pilih_alat("dihapus")
    if id_alat == "kembali":
        return

    masih_dipakai = False
    for s in db["sewa"].values():
        if s["id_alat"] == id_alat:
            masih_dipakai = True
    if masih_dipakai:
        print("  Alat masih tercatat di kode penyewaan, tidak bisa dihapus.")
        return

    yakin = input(f"  Yakin hapus '{db['alat'][id_alat]['nama']}'? (y/n): ").strip()
    if yakin.lower() == "kembali":
        print(PESAN_BATAL)
        return
    if yakin.lower() == "y":
        del db["alat"][id_alat]
        print("  Alat dihapus.")
    else:
        print("  Penghapusan dibatalkan.")


def admin_lihat_key():
    if not db["sewa"]:
        print("  (Belum ada kode penyewaan)")
        return
    print(f"\n  {'Kode':<10}{'Penyewa':<18}{'Alat':<16}{'Jml':>4}{'Hari':>5}  {'Jatuh Tempo':<12}Status")
    print("  " + "-" * 76)
    for kode, s in db["sewa"].items():
        print(f"  {kode:<10}{s['nama']:<18}{s['nama_alat']:<16}{s['jumlah']:>4}{s['hari']:>5}  "
              f"{s['jatuh_tempo']:<12}{s['status']}")


def admin_hapus_key():
    if not db["sewa"]:
        print("  (Belum ada kode penyewaan)")
        return
    admin_lihat_key()
    kode = input(f"\n  Kode yang dihapus {HINT_BATAL}: ").strip()
    if kode.lower() == "kembali":
        print(PESAN_BATAL)
        return
    kode = kode.upper()
    if kode not in db["sewa"]:
        print("  Kode tidak ditemukan.")
        return
    if db["sewa"][kode]["status"] != "selesai":
        print("  Kode masih aktif (barang belum dikembalikan), tidak bisa dihapus.")
        return
    del db["sewa"][kode]
    print("  Kode penyewaan dihapus.")


def admin_pendapatan():
    print(f"\n  Total uang hasil sewa (sewa + denda, tanpa jaminan): {rp(db['pendapatan'])}")


def admin_riwayat():
    if not db["riwayat"]:
        print("  (Belum ada riwayat)")
        return
    for r in db["riwayat"]:
        cetak_riwayat(r)


def admin_rekap():
    rekap = {}
    for id_alat in db["alat"]:
        rekap[id_alat] = {"kali": 0, "unit": 0, "aktif": 0}


    penyewa_unik = []
    for r in db["riwayat"]:
        if r["id_alat"] in rekap:
            rekap[r["id_alat"]]["kali"] += 1
            rekap[r["id_alat"]]["unit"] += r["jumlah"]
        nama = r["nama"].lower()
        if nama not in penyewa_unik:
            penyewa_unik.append(nama)

    for s in db["sewa"].values():
        if s["status"] == "aktif" and s["id_alat"] in rekap:
            rekap[s["id_alat"]]["aktif"] += s["jumlah"]

    print(f"\n  {'Alat':<20}{'Kali disewa':>12}{'Total unit':>12}{'Sedang aktif':>14}")
    print("  " + "-" * 58)
    for id_alat, a in db["alat"].items():
        baris = rekap[id_alat]
        print(f"  {a['nama']:<20}{baris['kali']:>12}{baris['unit']:>12}{baris['aktif']:>14}")
    print(f"\n  Jumlah penyewa unik (dari riwayat): {len(penyewa_unik)}")


def login_admin():
    for sisa in range(MAKS_PERCOBAAN_PIN - 1, -1, -1):
        pin = input(f"Masukkan PIN admin {HINT_BATAL}: ").strip()
        if pin.lower() == "kembali":
            print(PESAN_BATAL)
            return False
        if pin == PIN_ADMIN:
            return True
        print(f"PIN salah. Sisa percobaan: {sisa}")
    print("Akses ditolak.")
    return False


def menu_admin():
    if not login_admin():
        return
    jalankan_menu("MENU ADMIN", {
        "1": ("Lihat alat", tabel_alat),
        "2": ("Tambah alat", admin_tambah_alat),
        "3": ("Ubah harga dan stok", admin_ubah_alat),
        "4": ("Hapus alat", admin_hapus_alat),
        "5": ("Lihat kode penyewaan (key)", admin_lihat_key),
        "6": ("Hapus kode penyewaan (yang sudah selesai)", admin_hapus_key),
        "7": ("Uang hasil sewa", admin_pendapatan),
        "8": ("Riwayat sewa", admin_riwayat),
        "9": ("Rekap per alat", admin_rekap),
    })


# ======================= PENYEWA =======================
def penyewa_sewa():
    print("  (ketik 'kembali' kapan saja untuk batal)")
    nama = input_teks("  Nama penyewa: ")
    if nama == "kembali":
        return

    id_alat = pilih_alat("disewa")
    if id_alat == "kembali":
        return
    alat = db["alat"][id_alat]
    if alat["stok"] <= 0:
        print("  Stok alat habis.")
        return

    print(f"\n  Alat        : {alat['nama']}")
    print(f"  Harga sewa  : {rp(alat['harga_sewa'])} / hari   (stok {alat['stok']})")

    while True:
        teks = input("  Jumlah unit: ").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1  
        if 1 <= angka <= alat["stok"]:
            jumlah = angka
            break
        print(f"  Jumlah harus angka 1 sampai {alat['stok']}. {HINT_BATAL}")

    while True:
        teks = input("  Lama sewa (hari): ").strip()
        if teks.lower() == "kembali":
            print(PESAN_BATAL)
            return
        try:
            angka = int(teks)
        except ValueError:
            angka = -1
        if angka >= 1:
            hari = angka
            break
        print(f"  Lama sewa harus angka bulat, minimal 1. {HINT_BATAL}")


    subtotal = alat["harga_sewa"] * jumlah * hari
    persen = hitung_diskon(hari)
    potongan = subtotal * persen // 100
    total_sewa = subtotal - potongan
    jaminan = alat["harga_barang"] * jumlah * PERSEN_JAMINAN // 100

    print("\n  ----- RINCIAN PEMBAYARAN -----")
    print(f"  Harga sewa  : {rp(alat['harga_sewa'])} x {jumlah} unit x {hari} hari = {rp(subtotal)}")
    print(f"  Diskon {persen}%  : -{rp(potongan)}")
    print(f"  Biaya sewa  : {rp(total_sewa)}")
    print(f"  Jaminan     : {rp(jaminan)} (dikembalikan saat alat dikembalikan)")
    if not bayar(total_sewa + jaminan, "Total yang harus dibayar"):
        print("  Penyewaan dibatalkan.")
        return

    kode = kode_baru()
    tgl_sewa = date.today()
    jatuh_tempo = date.fromordinal(tgl_sewa.toordinal() + hari)
    db["sewa"][kode] = {
        "nama": nama, "id_alat": id_alat, "nama_alat": alat["nama"], "jumlah": jumlah,
        "hari": hari, "tgl_sewa": tgl_sewa.isoformat(), "jatuh_tempo": jatuh_tempo.isoformat(),
        "subtotal": subtotal, "diskon": persen, "total_sewa": total_sewa,
        "jaminan": jaminan, "harga_barang": alat["harga_barang"], "status": "aktif",
    }
    alat["stok"] -= jumlah
    db["pendapatan"] += total_sewa
    print(f"\n  Penyewaan berhasil! KODE PENYEWAAN ANDA: {kode}")
    print(f"  Jatuh tempo pengembalian: {jatuh_tempo.isoformat()}")


def penyewa_kembali():
    kode = input(f"  Kode penyewaan {HINT_BATAL}: ").strip()
    if kode.lower() == "kembali":
        print(PESAN_BATAL)
        return
    kode = kode.upper()
    if kode not in db["sewa"]:
        print("  Kode tidak ditemukan.")
        return
    s = db["sewa"][kode]
    if s["status"] != "aktif":
        print("  Kode ini sudah dikembalikan.")
        return
    print(f"  Penyewa: {s['nama']} | Alat: {s['nama_alat']} x{s['jumlah']} | "
          f"Jatuh tempo: {s['jatuh_tempo']}")

    tgl_kembali = input_tanggal("  Tanggal kembali (YYYY-MM-DD, Enter = hari ini): ")
    if tgl_kembali == "kembali":
        return
    kondisi = input_pilihan("  Status barang (baik/rusak): ", KONDISI_VALID)
    if kondisi == "kembali":
        return

    jatuh_tempo = date.fromisoformat(s["jatuh_tempo"])
    hari_telat = (tgl_kembali - jatuh_tempo).days
    if hari_telat < 0:
        hari_telat = 0
    persen_telat, denda_telat = hitung_denda_telat(s["subtotal"], hari_telat)

    if kondisi == "rusak":
        denda_rusak = s["harga_barang"] * s["jumlah"] * PERSEN_RUSAK // 100
    else:
        denda_rusak = 0
    total_denda = denda_telat + denda_rusak

    print("\n  ----- RINCIAN PENGEMBALIAN -----")
    print(f"  Terlambat   : {hari_telat} hari -> denda {persen_telat}% = {rp(denda_telat)}")
    print(f"  Barang {kondisi}: denda {rp(denda_rusak)}")
    print(f"  Total denda : {rp(total_denda)}")
    if total_denda > 0:
        if not bayar(total_denda, "Denda yang harus dibayar"):
            print("  Pengembalian dibatalkan.")
            return

    print(f"\n  Jaminan {rp(s['jaminan'])} dikembalikan otomatis.")

    if kondisi == "baik":
        db["alat"][s["id_alat"]]["stok"] += s["jumlah"]
    db["pendapatan"] += total_denda
    s["status"] = "selesai"
    db["riwayat"].append({
        "kode": kode, "nama": s["nama"], "id_alat": s["id_alat"], "nama_alat": s["nama_alat"],
        "jumlah": s["jumlah"], "hari": s["hari"], "tgl_sewa": s["tgl_sewa"],
        "tgl_kembali": tgl_kembali.isoformat(), "total_sewa": s["total_sewa"],
        "diskon": s["diskon"], "denda_telat": denda_telat, "denda_rusak": denda_rusak,
        "kondisi": kondisi, "jaminan": s["jaminan"],
    })
    print("  Pengembalian selesai. Terima kasih!")


def penyewa_histori():
    """Histori: yang masih disewa + yang sudah dikembalikan."""
    ada_aktif = False
    for kode, s in db["sewa"].items():
        if s["status"] == "aktif":
            if not ada_aktif:
                print("\n  ----- SEDANG DISEWA (belum dikembalikan) -----")
                ada_aktif = True
            cetak_sewa_aktif(kode, s)

    if db["riwayat"]:
        print("\n  ----- SUDAH DIKEMBALIKAN -----")
        admin_riwayat()

    if not ada_aktif and not db["riwayat"]:
        print("  (Belum ada histori penyewaan)")


def penyewa_info_diskon():
    tier = sorted(TIER_DISKON) 

    print("\n  ----- DISKON SEWA -----")
    print(f"  {'1-' + str(tier[0][0] - 1) + ' hari':<22}: tanpa diskon")
    for i in range(len(tier)):
        mulai, persen = tier[i]
        if i == len(tier) - 1:
            rentang = f"{mulai} hari atau lebih"
        else:
            akhir = tier[i + 1][0] - 1
            if akhir == mulai:
                rentang = f"{mulai} hari"
            else:
                rentang = f"{mulai}-{akhir} hari"
        print(f"  {rentang:<22}: {persen}%")

    print("\n  ----- DENDA KETERLAMBATAN -----")
    print("  Telat 1 hari = 3% dari harga sewa, lalu naik 2% tiap kelipatan 2 hari")
    print("  (hari ke-1: 3%, ke-2: 5%, ke-4: 7%, ke-6: 9%, dst.)")
    print(f"  Barang rusak = denda {PERSEN_RUSAK}% dari harga barang")
    print(f"  Jaminan = {PERSEN_JAMINAN}% dari harga barang, dikembalikan saat pengembalian")


def menu_penyewa():
    jalankan_menu("MENU PENYEWA", {
        "1": ("Sewa alat", penyewa_sewa),
        "2": ("Pengembalian", penyewa_kembali),
        "3": ("Histori penyewaan", penyewa_histori),
        "4": ("Info diskon & denda", penyewa_info_diskon),
    }, tampilkan_alat=True)


# ======================= MAIN =======================
def main():
    jalankan_menu("SISTEM PENYEWAAN ALAT", {
        "1": ("Admin", menu_admin),
        "2": ("Penyewa", menu_penyewa),
    }, teks_keluar="Keluar")
    print("Sampai jumpa!")


if __name__ == "__main__":
    main()
