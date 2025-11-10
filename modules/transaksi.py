import datetime
import os
from tkinter import messagebox
from fpdf import FPDF
import csv
from modules.database import read_csv, write_csv

BARANG_FILE = "barang.csv"
TRANS_FILE = "transaksi.csv"

def proses_transaksi(kode_barang, jumlah):
    barang = read_csv(BARANG_FILE)
    transaksi = read_csv(TRANS_FILE)

    for brg in barang:
        if brg["kode"].lower() == kode_barang.lower():
            stok = int(brg["stok"])
            jumlah = int(jumlah)

            if jumlah > stok:
                messagebox.showerror("Stok Tidak Cukup", "Jumlah beli melebihi stok!")
                return

            total = jumlah * int(brg["harga_jual"])
            brg["stok"] = str(stok - jumlah)

            kode_transaksi = f"TRX{len(transaksi)+1:03}"
            tanggal = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            transaksi.append({
                "kode_transaksi": kode_transaksi,
                "tanggal": tanggal,
                "kode_barang": brg["kode"],
                "nama_barang": brg["nama"],
                "jumlah": jumlah,
                "total": total
            })

            write_csv(BARANG_FILE, barang, list(brg.keys()))
            write_csv(TRANS_FILE, transaksi, list(transaksi[0].keys()))

            messagebox.showinfo("Transaksi Berhasil",
                f"Transaksi berhasil!\nNota PDF akan dibuat otomatis."
            )

            # ✅ Cetak nota PDF
            cetak_nota_pdf(kode_transaksi, tanggal, brg, jumlah, total)
            return

    messagebox.showerror("Tidak Ditemukan", "Kode barang tidak ditemukan!")


def cetak_nota_pdf(kode_transaksi, tanggal, brg, jumlah, total):
    # Folder penyimpanan
    folder = "nota"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file = os.path.join(folder, f"{kode_transaksi}.pdf")

    # PDF ukuran 80mm x panjang otomatis
    pdf = FPDF("P", "mm", (80, 200))
    pdf.set_auto_page_break(auto=True, margin=5)
    pdf.add_page()

    # Header Toko
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "TOKO SPAREPART LAPTOP", ln=True, align="C")

    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 4, "Jl. Teknologi No. 88, Jakarta", ln=True, align="C")
    pdf.cell(0, 4, "Telp: 0812-3456-7890", ln=True, align="C")
    pdf.ln(2)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "NOTA PENJUALAN", ln=True, align="C")
    pdf.ln(2)

    # Info Transaksi
    pdf.set_font("Arial", "", 9)
    pdf.cell(40, 4, f"Kode : {kode_transaksi}")
    pdf.cell(0, 4, f"{tanggal}", ln=True)

    pdf.ln(3)

    # Garis pemisah
    pdf.cell(0, 1, "-" * 32, ln=True)

    # Detail barang
    pdf.set_font("Arial", "B", 9)
    pdf.cell(35, 5, "Nama Barang")
    pdf.cell(10, 5, "Qty", align="C")
    pdf.cell(0, 5, "Subtotal", align="R", ln=True)

    pdf.set_font("Arial", "", 9)
    pdf.cell(35, 5, brg["nama"])
    pdf.cell(10, 5, str(jumlah), align="C")
    pdf.cell(0, 5, f"Rp {total:,}", align="R", ln=True)

    pdf.ln(3)
    pdf.cell(0, 1, "-" * 32, ln=True)

    # Total bayar
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, f"TOTAL : Rp {total:,}", ln=True, align="R")

    pdf.ln(3)
    pdf.cell(0, 1, "-" * 32, ln=True)

    pdf.ln(4)
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 4, "Terima kasih telah berbelanja!", ln=True, align="C")
    pdf.cell(0, 4, "*** Barang yang sudah dibeli", ln=True, align="C")
    pdf.cell(0, 4, "tidak dapat dikembalikan ***", ln=True, align="C")

    pdf.output(file)

    messagebox.showinfo("Nota Disimpan", f"Nota struk berhasil dibuat!\nLokasi: {file}")
