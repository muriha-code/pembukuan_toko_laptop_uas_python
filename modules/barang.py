from modules.database import read_csv, write_csv

FILENAME = "barang.csv"
FIELDS = ["kode", "nama", "kategori", "stok", "harga_beli", "harga_jual"]

def tampilkan_barang():
    data = read_csv(FILENAME)
    print("\n=== DAFTAR BARANG ===")
    if not data:
        print("Tidak ada data barang.")
    else:
        for brg in data:
            print(f"{brg['kode']} - {brg['nama']} ({brg['kategori']}) | Stok: {brg['stok']} | Harga jual: {brg['harga_jual']}")

def cari_barang(kode_barang):
    """Mencari barang berdasarkan kode"""
    data = read_csv(FILENAME)
    for brg in data:
        if brg["kode"].lower().replace("brg", "") == kode_barang.lower().replace("brg", ""):
            return brg
    return None

def tambah_barang():
    while True:
        data = read_csv(FILENAME)
        print("\n=== TAMBAH BARANG ===")
        kode = input("Kode Barang: ")
        nama = input("Nama Barang: ")
        kategori = input("Kategori: ")
        stok = input("Stok: ")
        harga_beli = input("Harga Beli: ")
        harga_jual = input("Harga Jual: ")

        data.append({
            "kode": kode,
            "nama": nama,
            "kategori": kategori,
            "stok": stok,
            "harga_beli": harga_beli,
            "harga_jual": harga_jual
        })
        write_csv(FILENAME, data, FIELDS)
        print("Barang berhasil ditambahkan!")

        lagi = input("Tambah barang lagi? (y/n): ").strip().lower()
        if lagi != "y":
            print("Kembali ke menu utama...")
            break

def ubah_barang():
    while True:
        data = read_csv(FILENAME)
        print("\n=== UBAH DATA BARANG ===")
        kode = input("Masukkan kode barang yang ingin diubah: ")
        ditemukan = False

        for brg in data:
            if brg["kode"] == kode:
                ditemukan = True
                print(f"\nData lama: {brg['nama']} ({brg['kategori']}) | Stok: {brg['stok']} | Harga jual: {brg['harga_jual']}")
                print("--- Ubah Data ---")
                brg["nama"] = input(f"Nama baru ({brg['nama']}): ") or brg["nama"]
                brg["kategori"] = input(f"Kategori baru ({brg['kategori']}): ") or brg["kategori"]
                brg["stok"] = input(f"Stok baru ({brg['stok']}): ") or brg["stok"]
                brg["harga_beli"] = input(f"Harga beli baru ({brg['harga_beli']}): ") or brg["harga_beli"]
                brg["harga_jual"] = input(f"Harga jual baru ({brg['harga_jual']}): ") or brg["harga_jual"]

                write_csv(FILENAME, data, FIELDS)
                print("✅ Data barang berhasil diperbarui!")
                break

        if not ditemukan:
            print("⚠️ Barang tidak ditemukan!")

        lagi = input("Ubah barang lain? (y/n): ").strip().lower()
        if lagi != "y":
            print("Kembali ke menu utama...")
            break


def hapus_barang():
    while True:
        data = read_csv(FILENAME)
        print("\n=== HAPUS BARANG ===")
        kode = input("Masukkan kode barang yang ingin dihapus: ")

        ditemukan = False
        baru = []
        for brg in data:
            if brg["kode"] == kode:
                ditemukan = True
                print(f"Barang ditemukan: {brg['nama']} ({brg['kategori']})")
                konfirmasi = input("Yakin ingin menghapus? (y/n): ").strip().lower()
                if konfirmasi != "y":
                    baru.append(brg)
                    print("Penghapusan dibatalkan.")
            else:
                baru.append(brg)

        if ditemukan:
            write_csv(FILENAME, baru, FIELDS)
            print("Barang berhasil dihapus!" if konfirmasi == "y" else "")
        else:
            print("Barang tidak ditemukan!")

        lagi = input("Hapus barang lagi? (y/n): ").strip().lower()
        if lagi != "y":
            print("Kembali ke menu utama...")
            break

