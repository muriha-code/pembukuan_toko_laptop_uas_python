import tkinter as tk
from tkinter import ttk, messagebox
from modules import barang, transaksi, laporan
from modules.database import read_csv, write_csv
import fpdf, fpdf.fpdf  # paksa terdeteksi saat build


# =====================================================
#                 BUKA MENU UTAMA LANGSUNG
# =====================================================
def buka_menu():
    root = tk.Tk()
    root.title("Aplikasi Pembukuan Toko Sparepart Laptop")
    root.geometry("1000x550")


    # ------------------ LAYOUT ------------------
    sidebar = tk.Frame(root, bg="#2C3E50", width=220)
    sidebar.pack(side="left", fill="y")
    container = tk.Frame(root, bg="white")
    container.pack(side="right", fill="both", expand=True)

    frames = {}
    def show_frame(name: str):
        frames[name].tkraise()

    # =====================================================
    #                   DATA BARANG
    # =====================================================
    def init_frame_barang(frame):
        for w in frame.winfo_children():
            w.destroy()

        tk.Label(frame, text="Data Barang (Inventory)", font=("Arial", 16, "bold")).pack(pady=10)

        frame_tabel = tk.Frame(frame)
        frame_tabel.pack(fill="both", expand=True)

        tabel = ttk.Treeview(frame_tabel,
                             columns=("kode", "nama", "kategori", "stok", "harga"),
                             show="headings")
        tabel.pack(fill="both", expand=True)

        for col in ("kode", "nama", "kategori", "stok", "harga"):
            tabel.heading(col, text=col.capitalize())

        def load():
            tabel.delete(*tabel.get_children())
            data = barang.read_csv("barang.csv")
            for b in data:
                tabel.insert("", tk.END, values=(b["kode"], b["nama"], b["kategori"], b["stok"], b["harga_jual"]))
        load()

        panel = tk.Frame(frame)
        panel.pack(fill="x")

        # Tambah Barang
        def tambah():
            pop = tk.Toplevel(root)
            pop.title("Tambah Barang")
            pop.geometry("300x300")

            entries = {}
            for f in barang.FIELDS:
                tk.Label(pop, text=f.capitalize()).pack()
                e = tk.Entry(pop)
                e.pack()
                entries[f] = e

            def simpan():
                data = barang.read_csv("barang.csv")
                data.append({f: entries[f].get() for f in barang.FIELDS})
                barang.write_csv("barang.csv", data, barang.FIELDS)
                pop.destroy()
                load()
                messagebox.showinfo("Sukses", "Barang ditambahkan.")
            tk.Button(pop, text="Simpan", bg="#00A86B", fg="white", command=simpan).pack(pady=10)

        # Ubah Barang
        def ubah():
            sl = tabel.focus()
            if not sl:
                return messagebox.showwarning("Pilih", "Pilih barang dulu.")
            val = tabel.item(sl, "values")
            kode = val[0]

            pop = tk.Toplevel(root)
            pop.title("Ubah Barang")
            pop.geometry("300x300")

            fields = ["nama", "kategori", "stok", "harga_beli", "harga_jual"]
            entries = {}
            for f in fields:
                tk.Label(pop, text=f.capitalize()).pack()
                e = tk.Entry(pop)
                e.pack()
                entries[f] = e

            def simpan():
                data = barang.read_csv("barang.csv")
                for b in data:
                    if b["kode"] == kode:
                        for f in fields:
                            b[f] = entries[f].get() or b[f]
                barang.write_csv("barang.csv", data, barang.FIELDS)
                pop.destroy()
                load()
                messagebox.showinfo("Sukses", "Barang diubah.")
            tk.Button(pop, text="Simpan Perubahan", bg="#FFA500", command=simpan).pack(pady=10)

        # Hapus Barang
        def hapus():
            sl = tabel.focus()
            if not sl:
                return messagebox.showwarning("Pilih", "Pilih barang dulu.")
            kode = tabel.item(sl, "values")[0]
            data = barang.read_csv("barang.csv")
            data = [b for b in data if b["kode"] != kode]
            barang.write_csv("barang.csv", data, barang.FIELDS)
            load()
            messagebox.showinfo("Sukses", "Barang dihapus.")

        tk.Button(panel, text="Tambah", command=tambah, bg="#007BFF", fg="white").pack(side="left", padx=5, pady=5)
        tk.Button(panel, text="Ubah", command=ubah, bg="#FFA500").pack(side="left", padx=5)
        tk.Button(panel, text="Hapus", command=hapus, bg="#FF3B30", fg="white").pack(side="left", padx=5)

    # =====================================================
    #                 TRANSAKSI KERANJANG
    # =====================================================
    def init_frame_transaksi(frame):
        for w in frame.winfo_children():
            w.destroy()

        tk.Label(frame, text="Transaksi Penjualan (Keranjang)", font=("Arial", 16, "bold")).pack(pady=10)

        data_barang = barang.read_csv("barang.csv")
        pilihan = [f"{b['kode']} - {b['nama']}" for b in data_barang]

        form = tk.Frame(frame)
        form.pack(pady=5)

        tk.Label(form, text="Pilih Barang").grid(row=0, column=0, sticky="w")
        cb = ttk.Combobox(form, values=pilihan, width=30)
        cb.grid(row=0, column=1)

        tk.Label(form, text="Jumlah").grid(row=1, column=0, sticky="w")
        qty = tk.Entry(form, width=10)
        qty.grid(row=1, column=1)
        qty.insert(0, "1")

        tabel = ttk.Treeview(frame, columns=("nama", "qty", "harga", "subtotal"), show="headings")
        tabel.pack(fill="both", expand=True, padx=10, pady=10)
        for c, t in zip(("nama", "qty", "harga", "subtotal"), ("Nama", "Qty", "Harga", "Subtotal")):
            tabel.heading(c, text=t)

        keranjang = []

        def refresh():
            tabel.delete(*tabel.get_children())
            total = 0
            for i, item in enumerate(keranjang):
                tabel.insert("", tk.END, values=item)
                total += item[3]
            lbl.config(text=f"TOTAL : Rp {total:,}")

        def tambah():
            if not cb.get():
                return
            try:
                j = int(qty.get())
            except ValueError:
                return messagebox.showwarning("Input salah", "Jumlah harus angka.")
            kode = cb.get().split(" - ")[0]
            for b in data_barang:
                if b["kode"] == kode:
                    subtotal = j * int(b["harga_jual"])
                    keranjang.append([b["nama"], j, int(b["harga_jual"]), subtotal])
                    refresh()

        tk.Button(form, text="Tambah ke Keranjang", bg="#007BFF", fg="white", command=tambah)\
            .grid(row=2, column=1, pady=5, sticky="e")

        lbl = tk.Label(frame, text="TOTAL : Rp 0", font=("Arial", 12, "bold"), fg="green")
        lbl.pack()

        def bayar():
            if not keranjang:
                return messagebox.showwarning("Kosong", "Keranjang kosong")
            for nama, j, h, sub in keranjang:
                for b in data_barang:
                    if b["nama"] == nama:
                        transaksi.proses_transaksi(b["kode"], j)
                        break
            keranjang.clear()
            refresh()
            init_frame_barang(frames["barang"])
            messagebox.showinfo("OK", "Transaksi selesai!")

        tk.Button(frame, text="BAYAR", width=20, bg="#28A745", fg="white", command=bayar).pack(pady=10)

    # =====================================================
    #                     LAPORAN
    # =====================================================
    def init_frame_laporan(frame):
        for w in frame.winfo_children():
            w.destroy()

        tk.Label(frame, text="Laporan Penjualan", font=("Arial", 16, "bold")).pack(pady=10)

        tabel = ttk.Treeview(frame, columns=("kode", "tgl", "nama", "qty", "total"), show="headings")
        tabel.pack(fill="both", expand=True, padx=10, pady=10)

        for c in ("kode", "tgl", "nama", "qty", "total"):
            tabel.heading(c, text=c.upper())

        data = laporan.read_csv("transaksi.csv")
        total = sum(int(t["total"]) for t in data)

        for t in data:
            tabel.insert("", tk.END, values=(t["kode_transaksi"], t["tanggal"], t["nama_barang"], t["jumlah"], t["total"]))

        tk.Label(frame, text=f"TOTAL PENDAPATAN : Rp {total:,}", fg="green", font=("Arial", 12, "bold")).pack(pady=5)

    # =====================================================
    #                  INISIALISASI FRAME
    # =====================================================
    frame_barang = tk.Frame(container); frame_barang.place(relwidth=1, relheight=1); frames["barang"] = frame_barang
    frame_transaksi = tk.Frame(container); frame_transaksi.place(relwidth=1, relheight=1); frames["transaksi"] = frame_transaksi
    frame_laporan = tk.Frame(container); frame_laporan.place(relwidth=1, relheight=1); frames["laporan"] = frame_laporan

    init_frame_barang(frame_barang)
    init_frame_transaksi(frame_transaksi)
    init_frame_laporan(frame_laporan)

    # =====================================================
    #                  SIDEBAR MENU
    # =====================================================
    menu_items = [
        ("Data Barang", lambda: show_frame("barang")),
        ("Transaksi", lambda: show_frame("transaksi")),
        ("Laporan Penjualan", lambda: show_frame("laporan")),
        ("Export Excel", laporan.export_laporan_excel),
        ("Keluar", root.destroy)
    ]

    for text, cmd in menu_items:
        tk.Button(sidebar, text=text, bg="#34495E", fg="white", relief="flat", command=cmd)\
          .pack(fill="x", pady=2)

    show_frame("barang")
    root.mainloop()


# ====== ENTRY POINT (LANGSUNG BUKA MENU UTAMA TANPA LOGIN) ======
if __name__ == "__main__":
    buka_menu()
