import datetime
from tkinter import messagebox
from modules.database import read_csv
import openpyxl
import os

TRANS_FILE = "transaksi.csv"

def tampilkan_laporan():
    data = read_csv(TRANS_FILE)

    if not data:
        messagebox.showinfo("Laporan", "Belum ada transaksi!")
        return

    total = sum(int(row["total"]) for row in data)

    pesan = "=== LAPORAN PENJUALAN ===\n\n"
    for tr in data:
        pesan += f"{tr['kode_transaksi']} | {tr['tanggal']} | {tr['nama_barang']} | {tr['jumlah']} x Rp{tr['total']}\n"

    pesan += f"\nTotal Penjualan: Rp{total:,}"
    messagebox.showinfo("Laporan Penjualan", pesan)


def export_laporan_excel():
    data = read_csv(TRANS_FILE)

    if not data:
        messagebox.showerror("Error", "Belum ada transaksi!")
        return

    folder = "laporan_excel"
    if not os.path.exists(folder):
        os.makedirs(folder)

    tanggal = datetime.datetime.now().strftime("%d-%m-%Y_%H.%M")
    filename = f"{folder}/Laporan_Penjualan_{tanggal}.xlsx"

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Laporan Penjualan"

    # Header
    header = ["Kode Transaksi", "Tanggal", "Kode Barang", "Nama Barang", "Jumlah", "Total (Rp)"]
    sheet.append(header)

    # Insert Data
    for tr in data:
        sheet.append([
            tr["kode_transaksi"],
            tr["tanggal"],
            tr["kode_barang"],
            tr["nama_barang"],
            tr["jumlah"],
            int(tr["total"])
        ])

    wb.save(filename)
    messagebox.showinfo("Sukses", f"Laporan berhasil diexport ke Excel!\nLokasi:\n{filename}")
