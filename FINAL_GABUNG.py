import tkinter as tk
from tkinter import ttk, filedialog,messagebox, DoubleVar
from tkinter import *
#import tkinter.font as tkFont
import sqlite3
#from collections import defaultdict
import os
import math #, statistics, pandas as pd
from math import atan2, degrees
import numpy as np
import sympy as sp
from sympy import *
import scipy.linalg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure printing to use plain text output
init_printing(use_unicode=True)

# Inisialisasi aplikasi
win = tk.Tk()
win.title("Calculation of Least Square Prambanan")
win.eval("tk::PlaceWindow . center")
background_color = "#15395b"
win.configure(bg=background_color)

# Membuat Style
style = ttk.Style()

# Variabel global untuk menyimpan referensi ke jendela baru
new_window = None
label_frame = None
# Variabel global untuk koneksi database dan file path
conn = None
cursor = None
newdatabase_db = None  # Menginisialisasi variabel global untuk file database


# Fungsi untuk melanjutkan ke proses dan menghancurkan new_window
def continue_to_process():
    global new_window
    if new_window:
        new_window.destroy()
    new_processing_window()

def data_edit():
    global new_window
    if new_window:
        new_window.destroy()
    #win = tk.Toplevel()
    DatabaseEditor(win)

def pengolahan_1():
    global new_window
    if new_window:
        new_window.destroy()
    #win = tk.Toplevel()
    Pengolahan_matang(win)

def pengolahan_azimuth():
    global new_window
    if new_window:
        new_window.destroy()
    proses_azimuth()

def pengolahan_koordinat():
    global new_window
    if new_window:
        new_window.destroy()
    koord_pendekatan()

def pengolahan_2():
    global new_window
    if new_window:
        new_window.destroy()
    hkt(win)

def _quit():
    win.quit()
    win.destroy()
    exit()

# Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

# Buat menu dan tambahkan item menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_separator()
file_menu.add_command(label="1. Proses Data & Cek Data", command=lambda: continue_to_process())
file_menu.add_separator()
file_menu.add_command(label="2. Pengolahan Data", command=lambda: pengolahan_1())
file_menu.add_separator()
file_menu.add_command(label="3. Pengolahan Azimuth",command=lambda: pengolahan_azimuth())
file_menu.add_separator()
file_menu.add_command(label="4. Koordinat Pendekatan",command=lambda: pengolahan_koordinat())
file_menu.add_separator()
file_menu.add_command(label="5. Pengolahan Hitung Perataan",command=lambda: pengolahan_2())
file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Fungsi untuk membuka dialog pemilihan file
def select_database():
        global selected_file_path
        file_path = filedialog.askopenfilename(
            title="Pilih File Database",
            filetypes=(("SQLite files", "*.db"), ("All files", "*.*"))
            )
        if file_path:
            selected_file_path = file_path
            connect_to_database(file_path)
            window_choice()  

# Fungsi untuk menghubungkan ke database yang dipilih
def connect_to_database(file_path):
    global conn, cursor
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    print(f"Terhubung ke database: {file_path}")
        
def window_choice():
    global new_window
    # Menghancurkan jendela sebelumnya jika ada
    if new_window:
        new_window.destroy()

    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color, font=("Arial", 14))

    label_frame = ttk.Labelframe(win, text=' PENDEFINISIAN TITIK ', padding=(180, 30), style='Custom.TLabelframe')

    def destroy_and_call(func):
        label_frame.destroy()
        func()

    T2 = Button(label_frame, text="TITIK ACUAN 2", font=("Arial", 14), bg="#FFC900", command=lambda: destroy_and_call(new_window_3new))
    T4 = Button(label_frame, text="TITIK ACUAN 4", font=("Arial", 14), bg="#FFC900", command=lambda: destroy_and_call(new_window_3new_T4))
    # Frame baru untuk Informasi
    info_frame = ttk.LabelFrame(label_frame,text="Informasi", style="Custom.TLabelframe")
    info_frame.grid(column=0, row=0, columnspan=3, padx=8, pady=8, sticky="nsew")

    # Label Informasi
    Label(
        info_frame,
        font=("Arial", 12),
        background=background_color,
        foreground="white",
        wraplength=1000,
        text=(
            "NOTE: Pilih titik acuan yang sesuai dengan pengukuran Anda, Anda dapat melihat pada formulir ukur anda (Input satu per satu data).\n"
            "1. Cek data yang anda punya apakah hanya memakai 2 titik berdiri alat, jika iya maka pilih 'TITIK ACUAN 2'.\n"
            "2. Cek data yang anda punya apakah memakai 3 atau 4 titik berdiri alat, jika iya maka pilih 'TITIK ACUAN 4'."
        ),

        justify="left"
    ).grid(column=0, row=0, columnspan=2, sticky="w", padx=10, pady=10)


    label_frame.grid(column=0, row=1, padx=8, pady=8)
    T2.grid(column=0, row=2, padx=8, pady=8, sticky=" ")
    T4.grid(column=1, row=2, padx=8, pady=8, sticky=" ")

    # Membuat Grafik Pertama (Matplotlib)
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    A = (0, 0)
    B = (4, 0)
    TP = (2, 3)

    # Plot garis
    ax1.plot([A[0], TP[0]], [A[1], TP[1]], 'k-', label='D(a-tp)')
    ax1.plot([TP[0], B[0]], [TP[1], B[1]], 'k-', label='D(b-tp)')
    ax1.plot([A[0], B[0]], [A[1], B[1]], 'k--', label='D(a-b)')

    # Plot titik
    ax1.scatter(*A, color='black', label='A (Berdiri Alat)')
    ax1.scatter(*B, color='black', label='B (Berdiri Alat)')
    ax1.scatter(*TP, color='black', label='TP (Titik Pantau)')

    # Plot sudut (alpha dan beta)
    ax1.scatter(0.3, 0.2, color='red', label=r'$\alpha$ (Sudut)')
    ax1.scatter(3.5, 0.2, color='blue', label=r'$\beta$ (Sudut)')

    # Label titik
    ax1.text(A[0] - 0.2, A[1] + 0.2, 'A', fontsize=12)
    ax1.text(B[0] + 0.2, B[1], 'B', fontsize=12)
    ax1.text(TP[0] + 0.2, TP[1], 'TP', fontsize=12)

    # Label sudut
    ax1.text(0.2, 0.3, r'$\alpha$', fontsize=14, color='red')
    ax1.text(3.5, 0.3, r'$\beta$', fontsize=14, color='blue')

    # Panah ke utara
    ax1.arrow(4, 1.5, 0, 0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
    ax1.text(4, 2.5, 'UTARA', fontsize=10, ha='center')

    # Pengaturan grafik
    ax1.set_title('Grafik Pengukuran dengan 2 Titik Acuan')
    ax1.axis('equal')
    ax1.grid(True)
    ax1.legend(loc='best')  # Menampilkan legenda

    # Menambahkan grafik pertama ke dalam tkinter
    canvas1 = FigureCanvasTkAgg(fig1, master=label_frame)
    canvas_widget1 = canvas1.get_tk_widget()
    canvas_widget1.grid(column=0, row=1, padx=8, pady=8)
    plt.close(fig1)

    # Membuat Grafik Kedua (Matplotlib)
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    A = (0, 0)
    B = (4, 0)
    TP = (2, 3)
    P = (-1, 4)
    S = (6, -1)

    # Plot garis
    ax2.plot([A[0], TP[0]], [A[1], TP[1]], label='D(a-tp)')
    ax2.plot([TP[0], B[0]], [TP[1], B[1]], label='D(b-tp)')
    ax2.plot([P[0], A[0]], [P[1], A[1]], label='D(p-a)')
    ax2.plot([B[0], S[0]], [B[1], S[1]], label='D(b-s)')

    # Plot titik
    ax2.scatter(*A, color='black')
    ax2.scatter(*B, color='black')
    ax2.scatter(*TP, color='black')
    ax2.scatter(*P, color='black', label='P (Backsight)')
    ax2.scatter(*S, color='black', label='S (Backsight)')

    # Plot sudut (alpha dan beta)
    ax2.scatter(0.1, 0.3, color='red')
    ax2.scatter(4, 0.3, color='blue')

    # Label titik
    ax2.text(A[0] - 0.5, A[1], 'A', fontsize=12)
    ax2.text(B[0] - 0.5, B[1], 'B', fontsize=12)
    ax2.text(TP[0] + 0.2, TP[1], 'TP', fontsize=12)
    ax2.text(P[0] + 0.2, P[1], 'P', fontsize=12)
    ax2.text(S[0] + 0.2, S[1] - 0.2, 'S', fontsize=12)

    # Label sudut
    ax2.text(0, 0.7, r'$\alpha$', fontsize=14, color='red')
    ax2.text(4.05, 0.3, r'$\beta$', fontsize=14, color='blue')

    # Panah ke utara
    ax2.arrow(0, 2.5, 0, 0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')  # Memindahkan ke kiri
    ax2.text(0, 3.5, 'UTARA', fontsize=12, ha='center')  # Memperbarui posisi teks UTARA

    # Pengaturan grafik
    ax2.set_title('Grafik Pengukuran dengan 3/4 Titik Acuan')
    ax2.axis('equal')
    ax2.grid(True)
    ax2.legend(loc='upper right')  # Menempatkan legenda di pojok kanan atas

    # Menambahkan grafik kedua ke dalam tkinter
    canvas2 = FigureCanvasTkAgg(fig2, master=label_frame)
    canvas_widget2 = canvas2.get_tk_widget()
    canvas_widget2.grid(column=1, row=1, padx=8, pady=8)
    plt.close(fig2)



    def kembali_to_awal():
        label_frame.destroy()
        new_window1()

    Button(label_frame, text="Kembali", font=("Arial", 14), bg="#FFC900", command=kembali_to_awal, width=12).grid(column=0, row=4, padx=8, pady=8)

    new_window = label_frame

def new_window1(): 
    global new_window
    # Menghancurkan jendela sebelumnya jika ada
    if new_window:
        new_window.destroy()
        new_window = None  # Pastikan variabel diatur ulang setelah penghancuran

    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', font=("Calibri", 14, "bold"),background=background_color)

    # Label Frame
    label_frame_win1 = ttk.Labelframe(win, text=' PRAMBANAN ', padding=(160, 60), style='Custom.TLabelframe')
    
    # Label Frame Tambahan
    label_frame_gs = ttk.Labelframe(label_frame_win1, text=' OPSI 1 ',  padding=(60, 40), style='Custom.TLabelframe')
    label_frame_ljt = ttk.Labelframe(label_frame_win1, text= ' OPSI 2 ', padding=(60, 40), style='Custom.TLabelframe')

    #label Frame Dokumentasi
    label_frame_doc = ttk.Labelframe(label_frame_win1, text=' DOKUMENTASI ',  padding=(60, 20), style='Custom.TLabelframe')

    # Tombol
    Gs = Button(label_frame_gs, text="MULAI INPUT DATA...", bg="#FFC900", font=("Calibri", 14, "bold"), command=new_window2)
    Ljt = Button(label_frame_ljt, text="LANJUTKAN INPUT DATA", bg="#FFC900", font=("Calibri", 14, "bold"), command=select_database)

    #Label Dokumentasi
    label_doc = Label(
        label_frame_doc, 
        text=(
            "Selamat Datang di Program Hitungan Perataan Kuadrat Terkecil.\n\n"
            "Proses yang harus dilalui hingga mendapatkan nilai koordinat dan simpangan baku adalah sebagai berikut:\n"
            "1. Memulai Proyek Baru: Pilih opsi 1 untuk memulai perhitungan dari awal dengan data baru.\n"
            "2. Melanjutkan Proyek Sebelumnya: Pilih opsi 2 untuk melanjutkan perhitungan dari proyek yang telah Anda simpan sebelumnya.\n"
            "3. Melakukan Pengecekan data, pengecekan ini dilakukan setelah seluruh data telah diinput. Pada menu 'file' pilih Nomor 1.\n"
            "4. Melakukan Pengolahan data, data yang sudah dicek kemudian diolah. Pada menu 'file' pilih Nomor 2.\n"
            "5. Melakukan pengolahan Azimuth. Azimuth akan diproses secara otomatis. Pada menu 'file' pilih Nomor 3.\n"
            "6. Melakukan pengolahan Koordinat Pendekatan. Koordinat Pendekatan akan diproses secara otomatis. Pada menu 'file' pilih Nomor 4.\n"
            "7. Melakukan pengolahan Hitung Perataan Kuadrat. Perhitungan akan diproses secara otomatis. Pada menu 'file' pilih Nomor 5.\n"
            "Silakan pilih opsi sesuai kebutuhan Anda. Selamat bekerja!"
        ),
        font=("Arial", 12),  # Ukuran font disesuaikan agar teks lebih pas
        wraplength=1000,      # Menyesuaikan lebar teks agar fit di dalam label frame
        justify="left", background=background_color  # Justifikasi teks rata kiri untuk keterbacaan dan background
        , foreground="white" # Warna teks diatur agar lebih terang
    )

    # Label Deskripsi
    label_1 = Label(label_frame_gs, text="Pilih opsi ini untuk memulai proyek baru dari awal.\nAnda dapat memasukkan data baru tanpa mengacu pada proyek sebelumnya.",
                     font=("Arial", 12), wraplength=420, justify="center", background=background_color, foreground="white")
    label_2 = Label(label_frame_ljt, text="Pilih opsi ini untuk melanjutkan proyek yang sudah ada.\nData yang sudah dimasukkan sebelumnya akan dipertahankan dan dapat diperbarui.",
                     font=("Arial", 12), wraplength=420, justify="center", background=background_color, foreground="white")

    # Grid Penempatan
    label_frame_win1.grid(column=0, row=0, padx=2, pady=2)

    # Penempatan Label Frame Tambahan
    label_frame_gs.grid(column=0, row=1, padx=10, pady=2)
    label_frame_ljt.grid(column=1, row=1, padx=10, pady=2)

    # label frame doc
    label_frame_doc.grid(column=0, row=0, columnspan=2,padx=10, pady=2, sticky = "ew")
    label_doc.grid(column=0, row=2, columnspan=2, pady=(10, 10))
    # Penempatan Tombol di dalam Label Frame Tambahan
    Gs.grid(column=0, row=0, columnspan=2, pady=(10, 10))
    Ljt.grid(column=0, row=0, columnspan=2, pady=(10, 10))

    # Penempatan Deskripsi di atas Label Frame Tambahan
    label_1.grid(column=0, row=2, columnspan=2, pady=(10, 10))
    label_2.grid(column=0, row=2, columnspan=2, pady=(10, 10))
    # Menyimpan referensi jendela saat ini ke new_window untuk melacaknya
    new_window = label_frame_win1

def create_database():
    
    global newdatabase_db
    newdatabase = E1.get()
    if newdatabase.strip() == "":
        print("Nama file tidak boleh kosong!")
        messagebox.showwarning('Kesalahan', 'Data tidak boleh kosong')
        return
        
    newdatabase_db = newdatabase + ".db"
    messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")

    connection = sqlite3.connect(newdatabase_db)
    cursor = connection.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Pendefinisian_Titik_T2" (
                   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                   "data_id" TEXT,
                   "Titik_Pantau" TEXT NOT NULL,
                   "STA1" TEXT,
                   "sta1_x" REAL,
                   "sta1_y" REAL,  
                   "STA2" TEXT,
                   "sta2_x" REAL,
                   "sta2_y" REAL
                    )
                ''')
    
    cursor.execute('''
               CREATE TABLE IF NOT EXISTS "Simpangan_Baku_T2"
                   (
                   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                   "STA1" TEXT,
                   "stdev_x_sta1" REAL,
                   "stdev_y_sta1" REAL,
                   "STA2" TEXT,
                   "stdev_x_sta2" REAL,
                   "stdev_y_sta2" REAL
                   )
                ''')
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Pendefinisian_Titik_T4" (
                   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                   "data_id" TEXT,
                   "Titik_Pantau" TEXT NOT NULL,
                   "STA_1" TEXT,
                   "sta_1_x" REAL,
                   "sta_1_y" REAL,  
                   "STA_2" TEXT,
                   "sta_2_x" REAL,
                   "sta_2_y" REAL, 
                   "BS_1" TEXT,
                   "bs_1_x" REAL,
                   "bs_1_y" REAL,  
                   "BS_2" TEXT,
                   "bs_2_x" REAL,
                   "bs_2_y" REAL
                    )
                ''')

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Simpangan_Baku_T4"
                   (
                   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                   "STA_1" TEXT,
                   "stdev_1_x" REAL,
                   "stdev_1_y" REAL,
                   "STA_2" TEXT,
                   "stdev_2_x" REAL,
                   "stdev_2_y" REAL,
                   "BS_1" TEXT,
                   "stdev_i1_x" REAL,
                   "stdev_i1_y" REAL,
                   "BS_2" TEXT,
                   "stdev_i2_x" REAL,
                   "stdev_i2_y" REAL
                   )
                ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Sudut_T2" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "STA_1" TEXT,
            "sudut_biasa" REAL,
            "Titik_Pantau" TEXT,
            "STA_2" TEXT,
            "sudut_luar_biasa" REAL,
            "Titik_Ikat" TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Sudut_T4" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "STA_1" TEXT,
            "sudut_biasa" REAL,
            "Titik_Pantau" TEXT,
            "STA_2" TEXT,
            "sudut_luar_biasa" REAL,
            "Titik_Ikat" TEXT
        )
    ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS "Jarak_T2" (
                   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                   "STA_1" TEXT,
                   "Jarak_P" REAL,
                   "Titik_Pantau" TEXT,
                   "STA_2" TEXT,
                   "Jarak_I" REAL,
                   "Titik_Ikat" TEXT
                )
    ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS "Jarak_T4" (
                   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                   "STA_1" TEXT,
                   "Jarak_P" REAL,
                   "Titik_Pantau" TEXT,
                   "STA_2" TEXT,
                   "Jarak_I" REAL,
                   "Titik_Ikat" TEXT
                )
    ''')

    connection.close()

def new_window2():
    global new_window, newdatabase_db
    # Menghapus jendela yang telah dibuat oleh new_window1()
    if new_window:
        new_window.destroy()

    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)

    # Label Frame
    label_frame = ttk.Labelframe(win, text=' PRAMBANAN ', padding=(100, 50), style='Custom.TLabelframe')

    # Label
    #L1 = Label(label_frame, text="NEW FILE :", background=background_color, font=("calibri", 24, "bold"), foreground="white")
    
    doc = """
    NOTE: Masukan nama file sesuai kebutuhan Anda.
    """
    Label(label_frame, text=doc, background=background_color, font=("calibri", 16), foreground="white").grid(column=2, row=0, padx=8, pady=8, columnspan=2)
    # Entry
    global E1
    E1 = Entry(label_frame, width=30, font=("Arial", 18))

    # Membuat tombol save untuk membuat database
    save = Button(label_frame, text="Simpan", font=("Arial", 14),bg="#FFC900", command=lambda:[create_database()]) 
    
    # Membuat tombol continue untuk beralih ke jendela selanjutnya
    cntn = Button(label_frame, text="Lanjut", font=("Arial", 14),bg="#FFC900", command=new_window_choice)

    # Grid
    label_frame.grid(column=0, row=1, padx=8, pady=8)
    #L1.grid(column=2, row=1, padx=8, pady=8, columnspan=2)
    E1.grid(column=2, row=2, padx=3, pady=3, columnspan=2)
    save.grid(column=1, row=3, padx=3, pady=10)
    cntn.grid(column=4, row=3, padx=3, pady=10)

    # Membuat variabel global untuk menyimpan referensi ke jendela baru
    new_window = label_frame

# Membuat global value1 dan value2 untuk new_window3 dan new_window4
selected_value1 = tk.StringVar()
selected_value2 = tk.StringVar()
selected_value3 = tk.StringVar()
selected_valuei1 = tk.StringVar()
selected_valuei2 = tk.StringVar()

#PROSES 1
# Global variable to store the path of the newly created processed database
new_db_path = None
global_selected_db_path = tk.StringVar()


def new_window_choice():
    global new_window
    if new_window:
        new_window.destroy()

    style.configure('Custom.TLabelframe', background=background_color, font=("Arial", 14))

    label_frame = ttk.Labelframe(win, text=' PENDEFINISIAN TITIK ', padding=(180, 30), style='Custom.TLabelframe')

    def destroy_and_call(func):
        label_frame.destroy()
        func()

    T2 = Button(label_frame, text="TITIK ACUAN 2", font=("Arial", 14), bg="#FFC900", command=lambda: destroy_and_call(new_window3))
    T4 = Button(label_frame, text="TITIK ACUAN 4", font=("Arial", 14), bg="#FFC900", command=lambda: destroy_and_call(new_window3_T4))
    # Frame baru untuk Informasi
    info_frame = ttk.LabelFrame(label_frame,text="Informasi", style="Custom.TLabelframe")
    info_frame.grid(column=0, row=0, columnspan=3, padx=8, pady=8, sticky="nsew")

    # Label Informasi
    Label(
        info_frame,
        font=("Arial", 12),
        background=background_color,
        foreground="white",
        wraplength=1000,
        text=(
            "NOTE: Pilih titik acuan yang sesuai dengan pengukuran Anda, Anda dapat melihat pada formulir ukur anda (Input satu per satu data).\n"
            "1. Cek data yang anda punya apakah hanya memakai 2 titik berdiri alat, jika iya maka pilih 'TITIK ACUAN 2'.\n"
            "2. Cek data yang anda punya apakah memakai 3 atau 4 titik berdiri alat, jika iya maka pilih 'TITIK ACUAN 4'."
        ),
        justify="left"
    ).grid(column=0, row=0, columnspan=2, sticky="w", padx=10, pady=10)


    label_frame.grid(column=0, row=1, padx=8, pady=8)
    T2.grid(column=0, row=2, padx=8, pady=8, sticky=" ")
    T4.grid(column=1, row=2, padx=8, pady=8, sticky=" ")

    # Membuat Grafik Pertama (Matplotlib)
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    A = (0, 0)
    B = (4, 0)
    TP = (2, 3)

    # Plot garis
    ax1.plot([A[0], TP[0]], [A[1], TP[1]], 'k-', label='D(a-tp)')
    ax1.plot([TP[0], B[0]], [TP[1], B[1]], 'k-', label='D(b-tp)')
    ax1.plot([A[0], B[0]], [A[1], B[1]], 'k--', label='D(a-b)')

    # Plot titik
    ax1.scatter(*A, color='black', label='A (Berdiri Alat)')
    ax1.scatter(*B, color='black', label='B (Berdiri Alat)')
    ax1.scatter(*TP, color='black', label='TP (Titik Pantau)')

    # Plot sudut (alpha dan beta)
    ax1.scatter(0.3, 0.2, color='red', label=r'$\alpha$ (Sudut)')
    ax1.scatter(3.5, 0.2, color='blue', label=r'$\beta$ (Sudut)')

    # Label titik
    ax1.text(A[0] - 0.2, A[1] + 0.2, 'A', fontsize=12)
    ax1.text(B[0] + 0.2, B[1], 'B', fontsize=12)
    ax1.text(TP[0] + 0.2, TP[1], 'TP', fontsize=12)

    # Label sudut
    ax1.text(0.2, 0.3, r'$\alpha$', fontsize=14, color='red')
    ax1.text(3.5, 0.3, r'$\beta$', fontsize=14, color='blue')

    # Panah ke utara
    ax1.arrow(4, 1.5, 0, 0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
    ax1.text(4, 2.5, 'UTARA', fontsize=10, ha='center')

    # Pengaturan grafik
    ax1.set_title('Grafik Pengukuran dengan 2 Titik Acuan')
    ax1.axis('equal')
    ax1.grid(True)
    ax1.legend(loc='best')  # Menampilkan legenda

    # Menambahkan grafik pertama ke dalam tkinter
    canvas1 = FigureCanvasTkAgg(fig1, master=label_frame)
    canvas_widget1 = canvas1.get_tk_widget()
    canvas_widget1.grid(column=0, row=1, padx=8, pady=8)
    plt.close(fig1)

    # Membuat Grafik Kedua (Matplotlib)
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    A = (0, 0)
    B = (4, 0)
    TP = (2, 3)
    P = (-1, 4)
    S = (6, -1)

    # Plot garis
    ax2.plot([A[0], TP[0]], [A[1], TP[1]], label='D(a-tp)')
    ax2.plot([TP[0], B[0]], [TP[1], B[1]], label='D(b-tp)')
    ax2.plot([P[0], A[0]], [P[1], A[1]], label='D(p-a)')
    ax2.plot([B[0], S[0]], [B[1], S[1]], label='D(b-s)')

    # Plot titik
    ax2.scatter(*A, color='black')
    ax2.scatter(*B, color='black')
    ax2.scatter(*TP, color='black')
    ax2.scatter(*P, color='black', label='P (Backsight)')
    ax2.scatter(*S, color='black', label='S (Backsight)')

    # Plot sudut (alpha dan beta)
    ax2.scatter(0.1, 0.3, color='red')
    ax2.scatter(4, 0.3, color='blue')

    # Label titik
    ax2.text(A[0] - 0.5, A[1], 'A', fontsize=12)
    ax2.text(B[0] - 0.5, B[1], 'B', fontsize=12)
    ax2.text(TP[0] + 0.2, TP[1], 'TP', fontsize=12)
    ax2.text(P[0] + 0.2, P[1], 'P', fontsize=12)
    ax2.text(S[0] + 0.2, S[1] - 0.2, 'S', fontsize=12)

    # Label sudut
    ax2.text(0, 0.7, r'$\alpha$', fontsize=14, color='red')
    ax2.text(4.05, 0.3, r'$\beta$', fontsize=14, color='blue')

    # Panah ke utara
    ax2.arrow(0, 2.5, 0, 0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')  # Memindahkan ke kiri
    ax2.text(0, 3.5, 'UTARA', fontsize=12, ha='center')  # Memperbarui posisi teks UTARA

    # Pengaturan grafik
    ax2.set_title('Grafik Pengukuran dengan 3/4 Titik Acuan')
    ax2.axis('equal')
    ax2.grid(True)
    ax2.legend(loc='upper right')  # Menempatkan legenda di pojok kanan atas

    # Menambahkan grafik kedua ke dalam tkinter
    canvas2 = FigureCanvasTkAgg(fig2, master=label_frame)
    canvas_widget2 = canvas2.get_tk_widget()
    canvas_widget2.grid(column=1, row=1, padx=8, pady=8)
    plt.close(fig2)



    def kembali_to_awal():
        label_frame.destroy()
        new_window1()

    Button(label_frame, text="Kembali", font=("Arial", 14), bg="#FFC900", command=kembali_to_awal, width=12).grid(column=0, row=4, padx=8, pady=8)

    new_window = label_frame

def new_window3():
    global newdatabase_db, background_color, style, win, selected_value3, selected_value1, selected_value2
    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)

    # Label Frame
    label_frame3 = ttk.Labelframe(win, text=' PENDEFINISIAN TITIK ', padding=(30,60), style='Custom.TLabelframe')

    # Label Frame Dokumen
    label_frame4 = ttk.Labelframe(label_frame3, text=' Dokumen ', padding=(80,5), style='Custom.TLabelframe')
    label_frame4.grid(column=2, row=0, padx=8, pady=8, columnspan=5)

    #doc
    cara = """
    1. Input koordinat berdiri alat dan backsight, sesuai koordinat pada data ukur
    2. Isikan sesuai dengan formulir ukur (semua nilai diisi)
    3. Jika koordinat tidak memiliki simpangan baku, maka kosongkan nilai tersebut.
    """
    # Label
    l2 = Label(label_frame4, text=cara,background=background_color, font=("calibri",14), foreground="white", justify="left")
    l4 = Label(label_frame3, text="TITIK PANTAU", background=background_color, font=("calibri",22), foreground="white")

    l2_1 = Label(label_frame3, text="Berdiri Alat", background=background_color, font=("calibri",16), foreground="white")
    l2_2 = Label(label_frame3, text="Koordinat X", background=background_color, font=("calibri",16), foreground="white")
    l2_3 = Label(label_frame3, text="Koordinat Y", background=background_color, font=("calibri",16), foreground="white")
    l2_4 = Label(label_frame3, text="Simpangan Baku X", background=background_color, font=("calibri",16), foreground="white")
    l2_5 = Label(label_frame3, text="Simpangan Baku Y", background=background_color, font=("calibri",16), foreground="white")

    l3_1 = Label(label_frame3, text="Backsight", background=background_color, font=("calibri",16), foreground="white")
    l3_2 = Label(label_frame3, text="Koordinat X", background=background_color, font=("calibri",16), foreground="white")
    l3_3 = Label(label_frame3, text="Koordinat Y", background=background_color, font=("calibri",16), foreground="white")
    l3_4 = Label(label_frame3, text="Simpangan Baku X", background=background_color, font=("calibri",16), foreground="white")
    l3_5 = Label(label_frame3, text="Simpangan Baku Y", background=background_color, font=("calibri",16), foreground="white")

    def continue_to_new_window3():
        new_window4()
        label_frame3.destroy()

    # Fungsi untuk menyimpan data ke database
    def save_data():
        global newdatabase_db
        try:
            # Mengambil nilai dari entry dan combobox
            sta1_x = float(e1.get())
            sta1_y = float(e2.get())
            sta2_x = float(e3.get())
            sta2_y = float(e4.get())
            stdev_1_x = float(sd1.get())
            stdev_1_y = float(sd2.get())
            stdev_2_x = float(sd3.get())
            stdev_2_y = float(sd4.get())
            titik_pantau = selected_value3.get()
            selected_value_combobox1 = number_chosen1.get()
            selected_value_combobox2 = number_chosen2.get()

            if newdatabase_db is None:
                print("Database belum dipilih atau tidak ada.")
                return

            # Menyimpan ke database
            connection = sqlite3.connect(newdatabase_db)
            cursor = connection.cursor()

            # Membuat data_id otomatis berdasarkan jumlah data di tabel
            connect_id = sqlite3.connect(newdatabase_db)
            curs = connect_id.cursor()
            curs.execute('SELECT COUNT(*) FROM Pendefinisian_Titik_T2')  # Sesuaikan nama tabel
            count = curs.fetchone()[0] + 1
            data_id = f"data{count}"
            connect_id.close()  # Pastikan koneksi ini ditutup

            try:
                # Memeriksa apakah Titik_Pantau sudah ada
                cursor.execute("SELECT 1 FROM Pendefinisian_Titik_T2 WHERE Titik_Pantau = ?", (titik_pantau,))
                exists = cursor.fetchone()

                if exists:
                    print("Titik_Pantau sudah ada. Masukkan nilai yang berbeda.")
                else:
                    cursor.execute("""INSERT INTO Pendefinisian_Titik_T2
                                    (data_id, Titik_Pantau, STA1, sta1_x, sta1_y, STA2, sta2_x, sta2_y)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (data_id, titik_pantau, selected_value_combobox1, sta1_x, sta1_y, selected_value_combobox2, sta2_x, sta2_y))
                    cursor.execute(""" INSERT INTO Simpangan_Baku_T2 
                                (STA1, stdev_x_sta1, stdev_y_sta1, STA2, stdev_x_sta2, stdev_y_sta2)
                                VALUES (?, ?, ?, ?, ?, ?)""",
                                (selected_value_combobox1, stdev_1_x, stdev_1_y, selected_value_combobox2, stdev_2_x, stdev_2_y))
                    connection.commit()

                    print("Data berhasil disimpan.")
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            finally:
                messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
                connection.close()

        except ValueError:
            print("Nilai koordinat harus berupa angka.")

    # Tombol
    save = Button(label_frame3, text="Simpan", font=("calibri",16),bg="#FFC900", command=save_data, width=10) 
    cntn = Button(label_frame3, text="Lanjut", font=("calibri",16),bg="#FFC900", command=lambda:continue_to_new_window3(), width=10)

    # Adding a Text box Entry Widget
    e1 = DoubleVar()
    en1 = Entry(label_frame3, textvariable=e1)
    e2 = DoubleVar()
    en2 = Entry(label_frame3, textvariable=e2)
    e3 = DoubleVar()
    en3 = Entry(label_frame3, textvariable=e3)
    e4 = DoubleVar()
    en4 = Entry(label_frame3, textvariable=e4)

    stdev1 = DoubleVar()
    sd1 = Entry(label_frame3, textvariable=stdev1)
    stdev2 = DoubleVar()
    sd2 = Entry(label_frame3, textvariable=stdev2)
    stdev3 = DoubleVar()
    sd3 = Entry(label_frame3, textvariable=stdev3)
    stdev4 = DoubleVar()
    sd4 = Entry(label_frame3, textvariable=stdev4)

    # Grid
    label_frame3.grid(column=0, row=1, padx=8, pady=8)

    l2.grid(column=2, row=0, padx=3, pady=3, columnspan=5, sticky="w")
    l4.grid(column=4, row=5, padx=3, pady=3, sticky=" ")

    l2_1.grid(column=2, row=1, padx=3, pady=3, sticky=" ")
    l2_2.grid(column=3, row=1, padx=3, pady=3, sticky=" ")
    l2_3.grid(column=4, row=1, padx=3, pady=3, sticky=" ")
    l2_4.grid(column=5, row=1, padx=3, pady=3, sticky=" ")
    l2_5.grid(column=6, row=1, padx=3, pady=3, sticky=" ")

    l3_1.grid(column=2, row=3, padx=3, pady=3, sticky=" ")
    l3_2.grid(column=3, row=3, padx=3, pady=3, sticky=" ")
    l3_3.grid(column=4, row=3, padx=3, pady=3, sticky=" ")
    l3_4.grid(column=5, row=3, padx=3, pady=3, sticky=" ")
    l3_5.grid(column=6, row=3, padx=3, pady=3, sticky=" ")

    save.grid(column=0, row=7, padx=3, pady=3)
    cntn.grid(column=7, row=7, padx=3, pady=3)

    en1.grid(column=3, row=2, padx=3, pady=3)
    en2.grid(column=4, row=2, padx=3, pady=3)
    en3.grid(column=3, row=4, padx=3, pady=3)
    en4.grid(column=4, row=4, padx=3, pady=3)

    sd1.grid(column=5, row=2, padx=3, pady=3)
    sd2.grid(column=6, row=2, padx=3, pady=3)
    sd3.grid(column=5, row=4, padx=3, pady=3)
    sd4.grid(column=6, row=4, padx=3, pady=3)

    # Combobox1
    number1 = tk.StringVar()
    number_chosen1 = ttk.Combobox(label_frame3, width=12, textvariable=number1, font=("calibri",12))
    number_chosen1['values'] = ('W1', 'P8', 'PRB3', 'B5', 'S2', 'S1', 'S8', 'P10', 'Z2', 'PRB2', 'B3')
    number_chosen1.grid(column=2, row=2, padx=3, pady=3)
    number_chosen1.current(0)

    # Combobox2
    number2 = tk.StringVar()
    number_chosen2 = ttk.Combobox(label_frame3, width=12, textvariable=number2, font=("calibri",12))
    number_chosen2['values'] = ('W1', 'P8', 'PRB3', 'B5', 'S2', 'S1', 'S8', 'P10', 'Z2', 'PRB2', 'B3')
    number_chosen2.grid(column=2, row=4, padx=3, pady=3)
    number_chosen2.current(0)
    
    # Update selected values for comboboxes 1 and 2
    def update_selected_values():
        selected_value1.set(number_chosen1.get())
        selected_value2.set(number_chosen2.get())

    number_chosen1.bind("<<ComboboxSelected>>", lambda event: update_selected_values())
    number_chosen2.bind("<<ComboboxSelected>>", lambda event: update_selected_values())

    # Combobox3
    number3 = tk.StringVar()
    number_chosen3 = ttk.Combobox(label_frame3, width=12, textvariable=number3, font=("calibri",12))
    number_chosen3['values'] = ('Nu', 'Gb', 'Gs', 'Nb', 'Au', 'Ab', 'Gt', 'Nt', 'At', 'Wt', 'Ws', 'St', 'Bu', 'Bt', 'Ss', 'Wb', 'Sb', 'Su', 'Bb')
    number_chosen3.grid(column=4, row=6, padx=3, pady=3, sticky=" ")
    number_chosen3.current(0)
    number_chosen3.bind("<<ComboboxSelected>>", lambda event: selected_value3.set(number_chosen3.get()))

    # Menggunakan variabel global untuk menyimpan referensi ke jendela baru
    global new_window
    new_window = label_frame3

def new_window3_T4():
    global newdatabase_db
    #Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background = background_color)

    #Label Frame
    label_frame3 = ttk.Labelframe(win, text=' PENDEFINISIAN TITIK ', padding=(30,40), style= 'Custom.TLabelframe')
    #label frame doc
    label_frame_doc = ttk.Labelframe(label_frame3, text=' Informasi ', padding=(60,10), style= 'Custom.TLabelframe')
    label_frame_doc.grid(column=3, row=0, columnspan=2, pady=10, padx=10)

    #doc
    cara = """
    1. Input koordinat berdiri alat dan backsight, sesuai koordinat pada data ukur
    2. Jika titik berdiri alat yang digunakan hanya 3, maka isikan sesuai dengan formulir ukur (semua nilai diisi)
    3. Jika koordinat tidak memiliki simpangan baku, maka kosongkan nilai tersebut.
    """
    info = Label(label_frame_doc, text=cara, background=background_color, font=("calibri",14), foreground="white", justify="left")
    info.grid(column=0,row=0,padx=5,pady=5, sticky="ew")

    #label frame & grid (untuk memisah pengisian koordinat)
    label_frame4 = ttk.Labelframe(label_frame3, text=' PENDEFINISIAN TITIK ', padding=(30,60), style= 'Custom.TLabelframe')
    label_frame4.grid(column=3, row=1, pady=10, padx=10)

    label_frame5 = ttk.Labelframe(label_frame3, text=' PENDEFINISIAN TITIK ', padding=(30,60), style= 'Custom.TLabelframe')
    label_frame5.grid(column=4, row=1, pady=10, padx=10)

    #Label
    l0 = Label(label_frame4,text="Backsight 1", background=background_color, font=("calibri",14, "bold") , foreground="white")
    l1 = Label(label_frame5,text="Backsight 2", background=background_color, font=("calibri",14, "bold"), foreground="white")

    l0_1 = Label(label_frame4, text="Prisma", background=background_color, font=("calibri",10), foreground="white")
    l0_2 = Label(label_frame4, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l0_3 = Label(label_frame4, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l0_4 = Label(label_frame4, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l0_5 = Label(label_frame4, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")

    l1_1 = Label(label_frame5, text="Prisma", background=background_color, font=("calibri",10), foreground="white")
    l1_2 = Label(label_frame5, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l1_3 = Label(label_frame5, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l1_4 = Label(label_frame5, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l1_5 = Label(label_frame5, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")
    #
    l2 = Label(label_frame4,text="STA 1", background=background_color, font=("calibri",14, "bold"), foreground="white")
    l3 = Label(label_frame5,text="STA 2", background=background_color, font=("calibri",14, "bold"), foreground="white")

    l2_1 = Label(label_frame4, text="Berdiri Alat", background=background_color, font=("calibri",10), foreground="white")
    l2_2 = Label(label_frame4, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l2_3 = Label(label_frame4, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l2_4 = Label(label_frame4, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l2_5 = Label(label_frame4, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")

    l3_1 = Label(label_frame5, text="Berdiri Alat", background=background_color, font=("calibri",10), foreground="white")
    l3_2 = Label(label_frame5, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l3_3 = Label(label_frame5, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l3_4 = Label(label_frame5, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l3_5 = Label(label_frame5, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")

    l4 = Label(label_frame3, text="TITIK PANTAU", background=background_color,font=("calibri",14, "bold"), foreground="white")
    
    def continue_to_new_window3_T4():
        new_window4_T4()
        label_frame3.destroy()

    #Fungsi untuk menyimpan data ke database
    def save_data():
        global newdatabase_db
        # Mengambil nilai dari entry dan combobox
        sta_1_x = float(e1.get())
        sta_1_y = float(e2.get())
        sta_2_x = float(e3.get())
        sta_2_y = float(e4.get())
        bs_1_x = float(e1i.get())
        bs_1_y = float(e2i.get())
        bs_2_x = float(e3i.get())
        bs_2_y = float(e4i.get())
        stdev_1_x = float(sd1.get())
        stdev_1_y = float(sd2.get())
        stdev_2_x = float(sd3.get())
        stdev_2_y = float(sd4.get())
        stdev_i1_x = float(sd1i.get())
        stdev_i1_y = float(sd2i.get())
        stdev_i2_x = float(sd3i.get())
        stdev_i2_y = float(sd4i.get())
        titik_pantau = selected_value3.get()
        selected_value_combobox1 = number_chosen1.get()
        selected_value_combobox2 = number_chosen2.get()
        selected_value_comboboxi1 = number_choseni1.get()
        selected_value_comboboxi2 = number_choseni2.get()

        # Menyimpan ke database
        connection = sqlite3.connect(newdatabase_db)
        cursor = connection.cursor()

        # Menghitung `data_id` dengan mengacu pada jumlah entri di tabel `Pendefinisian_Titik_T4`
        cursor.execute('SELECT COUNT(*) FROM Pendefinisian_Titik_T4')
        count = cursor.fetchone()[0] + 1
        data_id = f"data{count}"
        
        try:
            # Memeriksa apakah `Titik_Pantau` sudah ada
            cursor.execute("SELECT 1 FROM Pendefinisian_Titik_T4 WHERE Titik_Pantau = ?", (titik_pantau,))
            exists = cursor.fetchone()
            
            if exists:
                print("Titik_Pantau sudah ada. Masukkan nilai yang berbeda.")
            else:
                # Menyimpan data ke `Pendefinisian_Titik_T4`
                cursor.execute("""INSERT INTO Pendefinisian_Titik_T4
                                (data_id, Titik_Pantau, STA_1, sta_1_x, sta_1_y, STA_2, sta_2_x, sta_2_y, BS_1, bs_1_x, bs_1_y, BS_2, bs_2_x, bs_2_y)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (data_id, titik_pantau, selected_value_combobox1, sta_1_x, sta_1_y, selected_value_combobox2, sta_2_x, sta_2_y, 
                                selected_value_comboboxi1, bs_1_x, bs_1_y, selected_value_comboboxi2, bs_2_x, bs_2_y))
                
                # Menyimpan data ke `Simpangan_Baku_T4`
                cursor.execute("""INSERT INTO Simpangan_Baku_T4
                                (STA_1, stdev_1_x, stdev_1_y, STA_2, stdev_2_x, stdev_2_y, BS_1, stdev_i1_x, stdev_i1_y, BS_2, stdev_i2_x, stdev_i2_y)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (selected_value_combobox1, stdev_1_x, stdev_1_y, selected_value_combobox2, stdev_2_x, stdev_2_y, 
                                selected_value_comboboxi1, stdev_i1_x, stdev_i1_y, selected_value_comboboxi2, stdev_i2_x, stdev_i2_y))

                connection.commit()
                print("Data berhasil disimpan.")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            messagebox.showinfo("Berhasil", "Informasi Berhasil Disimpan")
            connection.close()

    #Tombol
    save = Button(label_frame3, text="Simpan", command= save_data, font=("arial", 14),bg="#FFC900") 
    cntn = Button(label_frame3, text="Lanjut", command=lambda:continue_to_new_window3_T4(), font=("arial", 14),bg="#FFC900")

    #Adding a Text box Entry Widget
    e1i = DoubleVar()
    en1i = Entry(label_frame4, textvariable = e1i)
    e2i = DoubleVar()
    en2i = Entry(label_frame4, textvariable = e2i)
    e3i = DoubleVar()
    en3i = Entry(label_frame5, textvariable = e3i)
    e4i = DoubleVar()
    en4i = Entry(label_frame5, textvariable = e4i)

    stdev_e1i = DoubleVar()
    sd1i = Entry(label_frame4, textvariable = stdev_e1i)
    stdev_e2i = DoubleVar()
    sd2i = Entry(label_frame4, textvariable = stdev_e2i)
    stdev_e3i = DoubleVar()
    sd3i = Entry(label_frame5, textvariable = stdev_e3i)
    stdev_e4i = DoubleVar()
    sd4i = Entry(label_frame5, textvariable = stdev_e4i)

    e1 = DoubleVar()
    en1 = Entry(label_frame4, textvariable = e1)
    e2 = DoubleVar()
    en2 = Entry(label_frame4, textvariable = e2)
    e3 = DoubleVar()
    en3 = Entry(label_frame5, textvariable = e3)
    e4 = DoubleVar()
    en4 = Entry(label_frame5, textvariable = e4)

    stdev_e1 = DoubleVar()
    sd1 = Entry(label_frame4, textvariable = stdev_e1)
    stdev_e2 = DoubleVar()
    sd2 = Entry(label_frame4, textvariable = stdev_e2)
    stdev_e3 = DoubleVar()
    sd3 = Entry(label_frame5, textvariable = stdev_e3)
    stdev_e4 = DoubleVar()
    sd4 = Entry(label_frame5, textvariable = stdev_e4)
    #Grid
    label_frame3.grid(column=0, row=1, padx=8, pady=8)

    l0.grid(column=3, row=3,padx=3,pady=3, columnspan=3, sticky=" ")
    l0_1.grid(column=2, row=4,padx=3,pady=3, sticky=" ")
    l0_2.grid(column=3, row=4,padx=3,pady=3, sticky=" ")
    l0_3.grid(column=4, row=4,padx=3,pady=3, sticky=" ")
    l0_4.grid(column=5, row=4,padx=3,pady=3, sticky=" ")
    l0_5.grid(column=6, row=4,padx=3,pady=3, sticky=" ")

    l1.grid(column=3, row=9,padx=3,pady=3, columnspan=3, sticky=" ")
    l1_1.grid(column=2, row=10,padx=3,pady=3, sticky=" ")
    l1_2.grid(column=3, row=10,padx=3,pady=3, sticky=" ")
    l1_3.grid(column=4, row=10,padx=3,pady=3, sticky=" ")
    l1_4.grid(column=5, row=10,padx=3,pady=3, sticky=" ")
    l1_5.grid(column=6, row=10,padx=3,pady=3, sticky=" ")

    l2.grid(column=3, row=0,padx=3,pady=3, columnspan=3, sticky=" ")
    l2_1.grid(column=2, row=1,padx=3,pady=3, sticky=" ")
    l2_2.grid(column=3, row=1,padx=3,pady=3, sticky=" ")
    l2_3.grid(column=4, row=1,padx=3,pady=3, sticky=" ")
    l2_4.grid(column=5, row=1,padx=3,pady=3, sticky=" ")
    l2_5.grid(column=6, row=1,padx=3,pady=3, sticky=" ")

    l3.grid(column=3, row=6,padx=3,pady=3, columnspan=3, sticky=" ")
    l3_1.grid(column=2, row=7,padx=3,pady=3, sticky=" ")
    l3_2.grid(column=3, row=7,padx=3,pady=3, sticky=" ")
    l3_3.grid(column=4, row=7,padx=3,pady=3, sticky=" ")
    l3_4.grid(column=5, row=7,padx=3,pady=3, sticky=" ")
    l3_5.grid(column=6, row=7,padx=3,pady=3, sticky=" ")

    l4.grid(column=3, row=12,padx=3,pady=3, columnspan=3, sticky=" ")

    save.grid(column=3,row=12, padx=3, pady=3, sticky='w')
    cntn.grid(column=4,row=12, padx=3, pady=3, sticky='e')

    en1i.grid(column = 3, row = 5, padx=3, pady=3)
    en2i.grid(column = 4, row = 5, padx=3, pady=3)
    sd1i.grid(column = 5, row = 5, padx=3, pady=3)
    sd2i.grid(column = 6, row = 5, padx=3, pady=3)

    en3i.grid(column = 3, row = 11, padx=3, pady=3)
    en4i.grid(column = 4, row = 11, padx=3, pady=3)
    sd3i.grid(column = 5, row = 11, padx=3, pady=3)
    sd4i.grid(column = 6, row = 11, padx=3, pady=3)

    en1.grid(column = 3, row = 2, padx=3, pady=3)
    en2.grid(column = 4, row = 2, padx=3, pady=3)
    sd1.grid(column = 5, row = 2, padx=3, pady=3)
    sd2.grid(column = 6, row = 2, padx=3, pady=3)

    en3.grid(column = 3, row = 8, padx=3, pady=3)
    en4.grid(column = 4, row = 8, padx=3, pady=3)
    sd3.grid(column = 5, row = 8, padx=3, pady=3)
    sd4.grid(column = 6, row = 8, padx=3, pady=3)

    #Combobox1
    number1 = tk.StringVar()
    number_chosen1 = ttk.Combobox(label_frame4, width = 8, textvariable=number1, font=("calibri",12))
    number_chosen1['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_chosen1.grid(column=2,row=2,padx=3,pady=3)
    number_chosen1.current(0)

    #Combobox2
    number2 = tk.StringVar()
    number_chosen2 = ttk.Combobox(label_frame5, width = 8, textvariable=number2, font=("calibri",12))
    number_chosen2['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_chosen2.grid(column=2,row=8,padx=3,pady=3)
    number_chosen2.current(0)

    #Combobox ikat 1
    number_i1 = tk.StringVar()
    number_choseni1 = ttk.Combobox(label_frame4, width = 8, textvariable=number_i1, font=("calibri",12))
    number_choseni1['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_choseni1.grid(column=2,row=5,padx=3,pady=3)
    number_choseni1.current(0)

    #Combobox ikat 2
    number_i2 = tk.StringVar()
    number_choseni2 = ttk.Combobox(label_frame5, width = 8, textvariable=number_i2, font=("calibri",12))
    number_choseni2['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_choseni2.grid(column=2,row=11,padx=3,pady=3)
    number_choseni2.current(0)
    

    def update_selected_values():
        selected_value1.set(number_chosen1.get())
        selected_value2.set(number_chosen2.get())

    number_chosen1.bind("<<ComboboxSelected>>", lambda event: update_selected_values())
    number_chosen2.bind("<<ComboboxSelected>>", lambda event: update_selected_values())

    def update_selected_values_ikat():
        selected_valuei1.set(number_choseni1.get())
        selected_valuei2.set(number_choseni2.get())

    number_choseni1.bind("<<ComboboxSelected>>", lambda event: update_selected_values_ikat())
    number_choseni2.bind("<<ComboboxSelected>>", lambda event: update_selected_values_ikat())

    #Combobox3
    number3 = tk.StringVar()
    number_chosen3 = ttk.Combobox(label_frame3, width = 12, textvariable=number3, font=("calibri",12))
    number_chosen3['values'] = ('Nu','Gb','Gs','Nb','Au','Ab','Gt','Nt','At','Wt','Ws','St','Bu','Bt','Ss','Wb','Sb','Su','Bb')
    number_chosen3.grid(column=3,row=13,padx=3, columnspan=3, sticky=" ")
    number_chosen3.current(0)
    number_chosen3.bind("<<ComboboxSelected>>", lambda event: selected_value3.set(number_chosen3.get()))

    # Menggunakan variabel global untuk menyimpan referensi ke jendela baru
    global new_window
    new_window = label_frame3 

def new_window4():
    #Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background = background_color)
    
    def convert_to_decimal_degree(degree1, degree2, minute1, minute2, second1, second2):
        DD_t = degree1 + (minute1 / 60) + (second1 / 3600)
        DD_i = degree2 + (minute2 / 60) + (second2 / 3600)

        if DD_i > DD_t:
            delta = DD_i - DD_t
            if delta > 180:
                delta = 360 - delta
        else:
            delta = DD_t - DD_i
            if delta > 180:
                delta = 360 - delta

        print(f"Nilai Sudut: {delta}")
        return delta
    
    # Definisi fungsi save_data di sini
    def save_data():
        # Mengambil nilai dari entry dan mengonversinya ke Decimal Degree
        sudut_biasa = convert_to_decimal_degree(float(en1.get()), float(enf1.get()), float(en3.get()), float(enf3.get()), float(en5.get()), float(enf5.get())) 
        sudut_luar_biasa = convert_to_decimal_degree(float(en2.get()), float(enf2.get()), float(en4.get()), float(enf4.get()), float(en6.get()), float(enf6.get())) 

        # Menentukan nilai Titik_Pantau
        selected_value = number_chosen4.get()
        value_pantau = selected_value3.get()

        # Menentukan nilai other_value berdasarkan selected_value
        selected_value_1 = selected_value1.get()
        selected_value_2 = selected_value2.get()

        if selected_value == selected_value_1 + "_1":
            other_value = selected_value_2 + "_1"
        elif selected_value == selected_value_2 + "_1":
            other_value = selected_value_1 + "_1"
        elif selected_value == selected_value_1 + "_2":
            other_value = selected_value_2 + "_2"
        elif selected_value == selected_value_2 + "_2":
            other_value = selected_value_1 + "_2"
        else:
            other_value = ""

        # Menyimpan data ke dalam tabel Sudut
        connection = sqlite3.connect(newdatabase_db)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Sudut_T2 (STA_1, sudut_biasa, Titik_Pantau, STA_2, sudut_luar_biasa, Titik_Ikat ) VALUES (?, ?, ?, ?, ?, ?)",
                        (selected_value, sudut_biasa, value_pantau, selected_value, sudut_luar_biasa, other_value))
            connection.commit()
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            print("Data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        connection.close()

    # Label Frame
    label_frame4 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(30, 60), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK PANTAU", style='Custom.TLabelframe')
    input_frame2 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK BACKSIGHT", style='Custom.TLabelframe')
    input_frame3 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 1", padding=(3, 35), style='Custom.TLabelframe')
    input_frame4 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 2", padding=(3, 35), style='Custom.TLabelframe')

    # Label
    # Frame dan Label Informasi
    label_frame5 = ttk.Labelframe(label_frame4, text=' INFORMASI ', padding=(30, 30), style='Custom.TLabelframe')
    label_frame5.grid(column=1, row=1,rowspan=4, padx=8, pady=9)
    # Langkah-langkah input program
    
    steps = """
    NOTE: CARA INPUT DATA HASIL BACAAN SUDUT DAN JARAK
     

    1. Pilih combobox Berdiri Alat mulai dari Berdiri Alat 1 (Berdiri Alat 2 Tidak Dipilih).

    2. Pilih "kode Pantau_1", lalu input bacaan sudut ke Titik Pantau dan Titik Backsight.
    
    3. Klik "Simpan" untuk menyimpan data.
    
    4. Ulangi langkah nomor 1,2 dan 3 untuk "kode Pantau_2" hingga semua selesai.
    
    5. Pindah ke Berdiri Alat 2 dan ulangi langkah yang sama.
    
    6. Setelah seluruh data bacaan sudut pada satu titik pantau telah diisi. klik "lanjut"
    
    7. Isi data jarak pada tampilan berikutnya, lalu sesuaikan seri 1 dan 2 
    """

    # Tambahkan langkah-langkah ke dalam label baru
    label_steps = Label(label_frame5, text=steps, font=("Arial", 12,"bold"), justify="left", foreground="white", background=background_color)
    label_steps.grid(row=1, column=0, padx=10, pady=3, rowspan=5)

    # Label Frame 3
    kosong1 = Label(input_frame1, text=' ', background=background_color)
    derajat1 = Label(input_frame1, text='DERAJAT', font=("Arial", 14))
    menit1 = Label(input_frame1, text='MENIT', font=("Arial", 14))
    detik1 = Label(input_frame1, text='DETIK', font=("Arial", 14))
    B1 = Label(input_frame1, text="Biasa", background=background_color, font=("Arial", 14), foreground="white")
    Lb1 = Label(input_frame1, text="Luar Biasa", background=background_color, font=("Arial", 14), foreground="white")

    # Label Frame Input 2
    kosong2 = Label(input_frame2, text=' ', background=background_color)
    derajat2 = Label(input_frame2, text='DERAJAT', font=("Arial", 14))
    menit2 = Label(input_frame2, text='MENIT', font=("Arial", 14))
    detik2 = Label(input_frame2, text='DETIK', font=("Arial", 14))
    B2 = Label(input_frame2, text="Biasa", background=background_color, font=("Arial", 14), foreground="white")
    Lb2 = Label(input_frame2, text="Luar Biasa", background=background_color, font=("Arial", 14), foreground="white")

    # Tombol
    # Pindahkan pemanggilan save_data ke bawah definisi fungsi save_data
    save = Button(label_frame4, text="Simpan", command=save_data, font=("Arial", 14),bg="#FFC900")

    def continue_to_new_window4():
        new_window5()
        label_frame4.destroy()

    spasi = Label(label_frame4, text=" ", background=background_color)
    cntn = Button(label_frame4, text="Lanjut", command=lambda: continue_to_new_window4(), font=("Arial", 14),bg="#FFC900")

    # Adding a Text box Entry Widget

    # Degree, Minute, Second F1
    # Data input untuk PB
    e1 = tk.IntVar()
    en1 = Entry(input_frame1, textvariable=e1)
    e3 = tk.IntVar()
    en3 = Entry(input_frame1, textvariable=e3)
    e5 = tk.IntVar()
    en5 = Entry(input_frame1, textvariable=e5)

    # Data input untuk PLB
    e2 = tk.IntVar()
    en2 = Entry(input_frame1, textvariable=e2)
    e4 = tk.IntVar()
    en4 = Entry(input_frame1, textvariable=e4)
    e6 = tk.IntVar()
    en6 = Entry(input_frame1, textvariable=e6)

    # Degree, Minute, Second F2
    # Data input untuk IB
    ef1 = tk.IntVar()
    enf1 = Entry(input_frame2, textvariable=ef1)
    ef3 = tk.IntVar()
    enf3 = Entry(input_frame2, textvariable=ef3)
    ef5 = tk.IntVar()
    enf5 = Entry(input_frame2, textvariable=ef5)

    # Data input untuk ILB
    ef2 = tk.IntVar()
    enf2 = Entry(input_frame2, textvariable=ef2)
    ef4 = tk.IntVar()
    enf4 = Entry(input_frame2, textvariable=ef4)
    ef6 = tk.IntVar()
    enf6 = Entry(input_frame2, textvariable=ef6)

    # Grid
    label_frame4.grid(column=0, row=1, padx=8, pady=8)
    input_frame1.grid(column=4, row=1)
    input_frame2.grid(column=4, row=2)
    input_frame3.grid(column=3, row=1, padx=8, pady=9)
    input_frame4.grid(column=3, row=2, padx=8, pady=9)

    save.grid(column=1, row=5, padx=3, pady=3,sticky="w")
    spasi.grid(column=5, row=1, padx=3)
    cntn.grid(column=4, row=5, padx=3, pady=10, sticky="e")

    # Entry Grid F1
    B1.grid(column=0, row=1, padx=3, pady=3)
    Lb1.grid(column=0, row=3, padx=3, pady=3)
    en1.grid(column=1, row=1, padx=3, pady=3)
    en2.grid(column=1, row=3, padx=3, pady=3)
    en3.grid(column=2, row=1, padx=3, pady=3)
    en4.grid(column=2, row=3, padx=3, pady=3)
    en5.grid(column=3, row=1, padx=3, pady=3)
    en6.grid(column=3, row=3, padx=3, pady=3)

    # Entry Grid F2
    B2.grid(column=0, row=1, padx=3, pady=3)
    Lb2.grid(column=0, row=3, padx=3, pady=3)
    enf1.grid(column=1, row=1, padx=3, pady=3)
    enf2.grid(column=1, row=3, padx=3, pady=3)
    enf3.grid(column=2, row=1, padx=3, pady=3)
    enf4.grid(column=2, row=3, padx=3, pady=3)
    enf5.grid(column=3, row=1, padx=3, pady=3)
    enf6.grid(column=3, row=3, padx=3, pady=3)

    # Tambahan Entry Grid
    kosong1.grid(column=0, row=2)
    derajat1.grid(column=1, row=0, sticky=' ')
    menit1.grid(column=2, row=0, sticky=' ')
    detik1.grid(column=3, row=0, sticky=' ')

    # Tambahan Entry Grid
    kosong2.grid(column=0, row=2)
    derajat2.grid(column=1, row=0, sticky=' ')
    menit2.grid(column=2, row=0, sticky=' ')
    detik2.grid(column=3, row=0, sticky=' ')

    # Combobox_Berdiri alat 1
    number4 = tk.StringVar()
    number_chosen4 = ttk.Combobox(input_frame3, width=12, textvariable=number4)
    selected_value_1 = selected_value1.get()
    values = [selected_value_1 + "_1",selected_value_1 + "_2"]
    number_chosen4['values'] = values
    number_chosen4.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen4.current(0)

    #Combobox berdiri alat 2
    number_4 = tk.StringVar()
    number_chosen_4 = ttk.Combobox(input_frame4, width=12, textvariable=number_4)
    selected_value_2 = selected_value2.get()
    values_ = [selected_value_2 + "_1",selected_value_2 + "_2"]
    number_chosen_4['values'] = values_
    number_chosen_4.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen_4.current(0)

def new_window4_T4():
    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)

    def convert_to_decimal_degree(degree1, degree2, minute1, minute2, second1, second2):
        DD_t = degree1 + (minute1 / 60) + (second1 / 3600)
        DD_i = degree2 + (minute2 / 60) + (second2 / 3600)

        if DD_i > DD_t:
            delta = DD_i - DD_t
            if delta > 180:
                delta = 360 - delta
        else:
            delta = DD_t - DD_i
            if delta > 180:
                delta = 360 - delta

        print(f"Nilai Sudut: {delta}")
        return delta

    # Definisi fungsi save_data di sini
    def save_data():
        # Mengambil nilai dari entry dan mengonversinya ke Decimal Degree
        sudut_biasa = convert_to_decimal_degree(float(en1.get()), float(enf1.get()), float(en3.get()), float(enf3.get()), float(en5.get()), float(enf5.get()))  # PB
        sudut_luar_biasa = convert_to_decimal_degree(float(en2.get()), float(enf2.get()), float(en4.get()), float(enf4.get()), float(en6.get()), float(enf6.get()))  # PLB

        # Menentukan nilai Titik Pantau dan Titik Ikat dari combobox
        selected_value = number_chosen4.get() or number_chosen44.get()
        value_pantau = selected_value3.get()
        titik_ikat_value = number_chosen4_ikat.get() or number_chosen4_ikat2.get()

        # Menyimpan data ke dalam tabel Sudut
        connection = sqlite3.connect(newdatabase_db)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Sudut_T4 (STA_1, sudut_biasa, Titik_Pantau, STA_2, sudut_luar_biasa, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                           (selected_value, sudut_biasa, value_pantau, selected_value, sudut_luar_biasa, titik_ikat_value))
            connection.commit()
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            print("Data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        connection.close()

    # Label Frame
    label_frame4 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(30, 40), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK PANTAU", style='Custom.TLabelframe')
    input_frame2 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK BACKSIGHT", style='Custom.TLabelframe')
    input_frame3 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 1", padding=(3, 35), style='Custom.TLabelframe')
    input_frame33 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 2", padding=(3, 35), style='Custom.TLabelframe')

    # Label
        # Frame dan Label Informasi
    label_frame5 = ttk.Labelframe(label_frame4, text=' INFORMASI ', padding=(30, 30), style='Custom.TLabelframe')
    label_frame5.grid(column=1, row=1,rowspan=4, padx=8, pady=9)
    # Langkah-langkah input program
    
    steps = """
    NOTE: CARA INPUT DATA HASIL BACAAN SUDUT DAN JARAK
     

    1. Pilih combobox Berdiri Alat mulai dari Berdiri Alat 1 (Berdiri Alat 2 Tidak Dipilih).

    2. Pilih kode pada berdiri alat dan sesuaikan kode untuk backsightnya 
       (urutannya sesuai berdiri alat 1 dan 2)
    
    3. Lalu input bacaan sudut Titik Pantau dan Titik Backsight.
    
    4. Klik "Simpan" untuk menyimpan data.
    
    5. Ulangi langkah nomor 1, 2, 3 dan 4 untuk kode berdiri alat 2 hingga semua selesai.
    
    6. Pindah ke Berdiri Alat 2 dan ulangi langkah yang sama.
    
    7. Setelah seluruh data bacaan sudut pada satu titik pantau telah diisi. klik "lanjut"
    
    8. Isi data jarak pada tampilan berikutnya, lalu sesuaikan seri 1 dan 2 
    """
    
    # Tambahkan langkah-langkah ke dalam label baru
    label_steps = Label(label_frame5, text=steps, font=("Arial", 12, "bold"), background=background_color,foreground="white", justify="left")
    label_steps.grid(row=1, column=0, padx=10, pady=10)

    # Label Frame 3
    kosong1 = Label(input_frame1, text=' ', background=background_color)
    derajat1 = Label(input_frame1, text='DERAJAT', font=("Arial", 12))
    menit1 = Label(input_frame1, text='MENIT', font=("Arial", 12))
    detik1 = Label(input_frame1, text='DETIK', font=("Arial", 12))
    B1 = Label(input_frame1, text="Biasa", background=background_color, font=("Arial", 12), foreground="white")
    Lb1 = Label(input_frame1, text="Luar Biasa", background=background_color, font=("Arial", 12), foreground="white")

    # Label Frame Input 2
    kosong2 = Label(input_frame2, text=' ', background=background_color)
    derajat2 = Label(input_frame2, text='DERAJAT', font=("Arial", 12))
    menit2 = Label(input_frame2, text='MENIT', font=("Arial", 12))
    detik2 = Label(input_frame2, text='DETIK', font=("Arial", 12))
    B2 = Label(input_frame2, text="Biasa", background=background_color, font=("Arial", 12), foreground="white")
    Lb2 = Label(input_frame2, text="Luar Biasa", background=background_color, font=("Arial", 12), foreground="white")

    # Tombol
    save = Button(label_frame4, text="Simpan", command=save_data, font=("Arial", 14),bg="#FFC900")

    def continue_to_new_window4_T4():
        new_window5_T4()
        label_frame4.destroy()

    spasi = Label(label_frame4, text=" ", background=background_color)
    cntn = Button(label_frame4, text="Lanjut", command=lambda: continue_to_new_window4_T4(), font=("Arial", 14),bg="#FFC900")

    # Adding a Text box Entry Widget

    # Degree, Minute, Second F1
    # Data input untuk PB
    e1 = tk.IntVar()
    en1 = Entry(input_frame1, textvariable=e1)
    e3 = tk.IntVar()
    en3 = Entry(input_frame1, textvariable=e3)
    e5 = tk.IntVar()
    en5 = Entry(input_frame1, textvariable=e5)

    # Data input untuk PLB
    e2 = tk.IntVar()
    en2 = Entry(input_frame1, textvariable=e2)
    e4 = tk.IntVar()
    en4 = Entry(input_frame1, textvariable=e4)
    e6 = tk.IntVar()
    en6 = Entry(input_frame1, textvariable=e6)

    # Degree, Minute, Second F2
    # Data input untuk IB
    ef1 = tk.IntVar()
    enf1 = Entry(input_frame2, textvariable=ef1)
    ef3 = tk.IntVar()
    enf3 = Entry(input_frame2, textvariable=ef3)
    ef5 = tk.IntVar()
    enf5 = Entry(input_frame2, textvariable=ef5)

    # Data input untuk ILB
    ef2 = tk.IntVar()
    enf2 = Entry(input_frame2, textvariable=ef2)
    ef4 = tk.IntVar()
    enf4 = Entry(input_frame2, textvariable=ef4)
    ef6 = tk.IntVar()
    enf6 = Entry(input_frame2, textvariable=ef6)

    # Grid
    label_frame4.grid(column=0, row=1, rowspan=4, padx=8, pady=8)
    input_frame1.grid(column=4, row=1)
    input_frame2.grid(column=4, row=3)
    input_frame3.grid(column=3, row=1, padx=8, pady=9)
    input_frame33.grid(column=3, row=3, padx=8, pady=9)

    save.grid(column=1, row=5, padx=3, pady=3, sticky="w")
    spasi.grid(column=5, row=1, padx=3)
    cntn.grid(column=4, row=5, padx=3, pady=3, sticky='e')

    # Entry Grid F1
    B1.grid(column=0, row=1, padx=3, pady=3)
    Lb1.grid(column=0, row=3, padx=3, pady=3)
    en1.grid(column=1, row=1, padx=3, pady=3)
    en2.grid(column=1, row=3, padx=3, pady=3)
    en3.grid(column=2, row=1, padx=3, pady=3)
    en4.grid(column=2, row=3, padx=3, pady=3)
    en5.grid(column=3, row=1, padx=3, pady=3)
    en6.grid(column=3, row=3, padx=3, pady=3)

    # Entry Grid F2
    B2.grid(column=0, row=2, padx=3, pady=3)
    Lb2.grid(column=0, row=4, padx=3, pady=3)
    enf1.grid(column=1, row=2, padx=3, pady=3)
    enf2.grid(column=1, row=4, padx=3, pady=3)
    enf3.grid(column=2, row=2, padx=3, pady=3)
    enf4.grid(column=2, row=4, padx=3, pady=3)
    enf5.grid(column=3, row=2, padx=3, pady=3)
    enf6.grid(column=3, row=4, padx=3, pady=3)

    # Tambahan Entry Grid
    kosong1.grid(column=0, row=2)
    derajat1.grid(column=1, row=0, sticky=' ')
    menit1.grid(column=2, row=0, sticky=' ')
    detik1.grid(column=3, row=0, sticky=' ')

    # Tambahan Entry Grid
    kosong2.grid(column=0, row=3)
    derajat2.grid(column=1, row=1, sticky=' ')
    menit2.grid(column=2, row=1, sticky=' ')
    detik2.grid(column=3, row=1, sticky=' ')

    # Combobox4 berdiri alat 1
    number4 = tk.StringVar()
    number_chosen4 = ttk.Combobox(input_frame3, width=8, textvariable=number4, font=("Arial", 12))
    selected_value_1 = selected_value1.get()
    selected_value_2 = selected_value2.get()
    values = [selected_value_1 + "_1", selected_value_1 + "_2"]
    number_chosen4['values'] = values
    number_chosen4.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen4.current(0)
    #berdiri alat 2
    number44 = tk.StringVar()
    number_chosen44 = ttk.Combobox(input_frame33, width=8, textvariable=number44, font=("Arial", 12))
    selected_value_2 = selected_value2.get()
    values = [selected_value_2 + "_1", selected_value_2 + "_2"]
    number_chosen44['values'] = values
    number_chosen44.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen44.current(0)

    # Combobox4 Ikat1
    number4_ikat = tk.StringVar()
    number_chosen4_ikat = ttk.Combobox(input_frame2, width=8, textvariable=number4_ikat, font=("Arial", 12))
    selected_value_1i = selected_valuei1.get()
    values = [selected_value_1i + "_1", selected_value_1i + "_2"]
    number_chosen4_ikat['values'] = values
    number_chosen4_ikat.grid(column=0, row=0, padx=3, pady=3)
    number_chosen4_ikat.current(0)

    # Combobox4 Ikat1
    number4_ikat2 = tk.StringVar()
    number_chosen4_ikat2 = ttk.Combobox(input_frame2, width=8, textvariable=number4_ikat2, font=("Arial", 12))
    selected_value_2i = selected_valuei2.get()
    values = [selected_value_2i + "_1", selected_value_2i + "_2"]
    number_chosen4_ikat2['values'] = values
    number_chosen4_ikat2.grid(column=0, row=1, padx=3, pady=3)
    number_chosen4_ikat2.current(0)

def new_window5():
    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)

    # Label Frame
    label_frame5 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(60, 65), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame5, padding=(6, 6), text="JARAK KE TITIK PANTAU", style='Custom.TLabelframe')
    frame1_seri_1 = ttk.Labelframe(input_frame1, padding=(2, 2), text="Seri 1", style='Custom.TLabelframe')
    frame1_seri_2 = ttk.Labelframe(input_frame1, padding=(2, 2), text="Seri 2", style='Custom.TLabelframe')

    input_frame2 = ttk.Labelframe(label_frame5, padding=(6, 6), text="JARAK KE TITIK IKAT", style='Custom.TLabelframe')
    frame2_seri_1 = ttk.Labelframe(input_frame2, padding=(2, 2), text="Seri 1", style='Custom.TLabelframe')
    frame2_seri_2 = ttk.Labelframe(input_frame2, padding=(2, 2), text="Seri 2", style='Custom.TLabelframe')

    input_frame3 = ttk.Labelframe(label_frame5, text="BERDIRI ALAT", padding=(6, 80), style='Custom.TLabelframe')

    def continue_to_new_choice():
        new_window_choice()
        label_frame5.destroy()

    # Pemisah antara lanjut dan input
    spasi = Label(label_frame5, text=" ", background=background_color)
    cntn = Button(label_frame5, text="Kembali", font=("Arial", 14), command=lambda: continue_to_new_choice(),bg="#FFC900")

    def save_data():
        # Mengambil nilai dari entry dan konversi ke dalam format yang sesuai
        jarak_pantau_1 = [en1.get(), en2.get()]
        jarak_pantau_2 = [en3.get(), en4.get()]
        jarak_ikat_1 = [enf1.get(), enf2.get()]
        jarak_ikat_2 = [enf3.get(), enf4.get()]

        selected_value = number_chosen5.get()
        value_pantau = selected_value3.get()
        other_value = selected_value1.get() if selected_value == selected_value2.get() else selected_value2.get()

        # Koneksikan ke database yang sudah dibuat sebelumnya
        connection = sqlite3.connect(newdatabase_db)
        cursor = connection.cursor()

        try:
            for jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2 in zip(jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2):
                if jarak_pantau_1 and jarak_pantau_2 and jarak_ikat_1 and jarak_ikat_2:
                    cursor.execute(
                        "INSERT INTO Jarak_T2 (STA_1, Jarak_P, Titik_Pantau, STA_2, Jarak_I, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                        (selected_value + '_1', jarak_pantau_1, value_pantau, selected_value + '_1', jarak_ikat_1, other_value))
                    cursor.execute(
                        "INSERT INTO Jarak_T2 (STA_1, Jarak_P, Titik_Pantau, STA_2, Jarak_I, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                        (selected_value + '_2', jarak_pantau_2, value_pantau, selected_value + '_2', jarak_ikat_2, other_value))
            connection.commit()
            messagebox.showinfo("Berhasil", "Informasi Berhasil Disimpan")
            print("data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    # Tombol
    save = Button(label_frame5, text="Simpan", font=("Arial", 14), command=save_data,bg="#FFC900")

    # Adding a Text box Entry Widget
    # Jarak dari berdiri alat ke titik pantau
    e1 = tk.DoubleVar()
    en1 = Entry(frame1_seri_1, textvariable=e1, font=("Arial", 12))
    e2 = tk.DoubleVar()
    en2 = Entry(frame1_seri_1, textvariable=e2, font=("Arial", 12))
    e3 = tk.DoubleVar()
    en3 = Entry(frame1_seri_2, textvariable=e3, font=("Arial", 12))
    e4 = tk.DoubleVar()
    en4 = Entry(frame1_seri_2, textvariable=e4, font=("Arial", 12))

    # Jarak dari berdiri alat ke titik ikat
    ef1 = tk.DoubleVar()
    enf1 = Entry(frame2_seri_1, textvariable=ef1, font=("Arial", 12))
    ef2 = tk.DoubleVar()
    enf2 = Entry(frame2_seri_1, textvariable=ef2, font=("Arial", 12))
    ef3 = tk.DoubleVar()
    enf3 = Entry(frame2_seri_2, textvariable=ef3, font=("Arial", 12))
    ef4 = tk.DoubleVar()
    enf4 = Entry(frame2_seri_2, textvariable=ef4, font=("Arial", 12))

    # Grid
    label_frame5.grid(column=0, row=1, padx=10, pady=10)
    input_frame1.grid(column=4, row=1, padx=10, pady=10)
    frame1_seri_1.grid(column=0, row=1)
    frame1_seri_2.grid(column=0, row=2)

    input_frame2.grid(column=4, row=2, padx=10, pady=10)
    frame2_seri_1.grid(column=0, row=1)
    frame2_seri_2.grid(column=0, row=2)
    input_frame3.grid(column=3, row=1, padx=10, pady=10)

    save.grid(column=2, row=5, padx=6, pady=6)
    spasi.grid(column=5, row=1, padx=6)
    cntn.grid(column=6, row=5, padx=6, pady=6)

    # Entry Grid F1
    en1.grid(column=0, row=1, padx=6, pady=6)
    en2.grid(column=0, row=2, padx=6, pady=6)
    en3.grid(column=0, row=3, padx=6, pady=6)
    en4.grid(column=0, row=4, padx=6, pady=6)

    # Entry Grid F2
    enf1.grid(column=0, row=1, padx=6, pady=6)
    enf2.grid(column=0, row=2, padx=6, pady=6)
    enf3.grid(column=0, row=3, padx=6, pady=6)
    enf4.grid(column=0, row=4, padx=6, pady=6)

    # Combobox5
    number5 = tk.StringVar()
    number_chosen5 = ttk.Combobox(input_frame3, width=12, textvariable=number5, font=("Arial", 16))
    number_chosen5['values'] = (selected_value1.get(), selected_value2.get())
    number_chosen5.grid(column=0, row=0, padx=6, pady=6, rowspan=3)
    number_chosen5.current(0)

def new_window5_T4():
    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)

    # Label Frame
    label_frame5 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(30, 60), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame5, padding=(3, 3), text="JARAK KE TITIK PANTAU", style='Custom.TLabelframe')
    frame1_seri_1 = ttk.Labelframe(input_frame1, padding=(1,1), text="Seri 1", style= 'Custom.TLabelframe')
    frame1_seri_2 = ttk.Labelframe(input_frame1, padding=(1,1), text="Seri 2", style= 'Custom.TLabelframe')

    input_frame2 = ttk.Labelframe(label_frame5, padding=(3, 3), text="JARAK KE TITIK IKAT", style='Custom.TLabelframe')
    frame2_seri_1 = ttk.Labelframe(input_frame2, padding=(1,1), text="Seri 1", style= 'Custom.TLabelframe')
    frame2_seri_2 = ttk.Labelframe(input_frame2, padding=(1,1), text="Seri 2", style= 'Custom.TLabelframe')

    input_frame3 = ttk.Labelframe(label_frame5, text="BERDIRI ALAT", padding=(3, 63), style='Custom.TLabelframe')

    def continue_to_new_choice():
        new_window_choice()
        label_frame5.destroy()

    # pemisah antara lanjut dan input
    spasi = Label(label_frame5, text=" ", background=background_color)
    cntn = Button(label_frame5, text="Kembali", command=lambda: continue_to_new_choice(), font=("Arial", 14),bg="#FFC900")

    def save_data():
        # Mengambil nilai dari entry dan konversi ke dalam format yang sesuai
        jarak_pantau_1 = [en1.get(),en2.get()]
        jarak_pantau_2 = [en3.get(),en4.get()]
        jarak_ikat_1 = [enf1.get(),enf2.get()]
        jarak_ikat_2 = [enf3.get(),enf4.get()]


        selected_value = number_chosen5.get()
        value_pantau = selected_value3.get()
        titik_ikat_value = number_chosen5_ikat.get()

        # Koneksikan ke database yang sudah dibuat sebelumnya
        connection = sqlite3.connect(newdatabase_db)
        cursor = connection.cursor()

        try:
            # Simpan data ke dalam tabel Jarak
            for jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2 in zip(jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2):
                if jarak_pantau_1 and jarak_pantau_2 and jarak_ikat_1 and jarak_ikat_2:  # memastikan tidak ada nilai yang kosong
                    cursor.execute("INSERT INTO Jarak_T4 (STA_1, Jarak_P, Titik_Pantau, STA_2, Jarak_I, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                                   (selected_value + '_1', jarak_pantau_1, value_pantau, selected_value + '_1', jarak_ikat_1, titik_ikat_value))
                    cursor.execute("INSERT INTO Jarak_T4 (STA_1, Jarak_P, Titik_Pantau, STA_2, Jarak_I, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                                   (selected_value + '_2', jarak_pantau_2, value_pantau, selected_value + '_2', jarak_ikat_2, titik_ikat_value))
            connection.commit()
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            print("Data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    # Tombol
    save = Button(label_frame5, text="Simpan", command=save_data, font=("Arial", 14),bg="#FFC900")

    # Adding a Text box Entry Widget
    # Jarak dari berdiri alat ke titik pantau
    e1 = tk.DoubleVar()
    en1 = Entry(frame1_seri_1, textvariable=e1, font=("Arial", 14))
    e2 = tk.DoubleVar()
    en2 = Entry(frame1_seri_1, textvariable=e2, font=("Arial", 14))
    e3 = tk.DoubleVar()
    en3 = Entry(frame1_seri_2, textvariable=e3, font=("Arial", 14))
    e4 = tk.DoubleVar()
    en4 = Entry(frame1_seri_2, textvariable=e4, font=("Arial", 14))
    
    # Jarak dari berdiri alat ke titik ikat
    ef1 = tk.DoubleVar()
    enf1 = Entry(frame2_seri_1, textvariable=ef1, font=("Arial", 14))
    ef2 = tk.DoubleVar()
    enf2 = Entry(frame2_seri_1, textvariable=ef2, font=("Arial", 14))
    ef3 = tk.DoubleVar()
    enf3 = Entry(frame2_seri_2, textvariable=ef3, font=("Arial", 14))
    ef4 = tk.DoubleVar()
    enf4 = Entry(frame2_seri_2, textvariable=ef4, font=("Arial", 14))
    
    # Grid
    label_frame5.grid(column=0, row=1, padx=8, pady=8)
    input_frame1.grid(column=4, row=1)
    frame1_seri_1.grid(column=0, row=1)
    frame1_seri_2.grid(column=0, row=2)

    input_frame2.grid(column=4, row=3,pady=9)
    frame2_seri_1.grid(column=0, row=1)
    frame2_seri_2.grid(column=0, row=2)
    input_frame3.grid(column=3, row=1, padx=8, pady=9)

    save.grid(column=2, row=5, padx=3, pady=3)
    spasi.grid(column=5, row=1, padx=3)
    cntn.grid(column=6, row=5, padx=3, pady=3)

    # Entry Grid F1
    en1.grid(column=0, row=1, padx=3, pady=3)
    en2.grid(column=0, row=2, padx=3, pady=3)
    en3.grid(column=0, row=3, padx=3, pady=3)
    en4.grid(column=0, row=4, padx=3, pady=3)

    # Entry Grid F2
    enf1.grid(column=0, row=2, padx=3, pady=3)
    enf2.grid(column=0, row=3, padx=3, pady=3)
    enf3.grid(column=0, row=4, padx=3, pady=3)
    enf4.grid(column=0, row=5, padx=3, pady=3)

    # Combobox5
    number5 = tk.StringVar()
    number_chosen5 = ttk.Combobox(input_frame3, width=12, textvariable=number5, font=("Arial", 14))
    number_chosen5['values'] = (selected_value1.get(), selected_value2.get())
    number_chosen5.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen5.current(0)

    # Combobox5 Ikat
    number5_ikat = tk.StringVar()
    number_chosen5_ikat = ttk.Combobox(input_frame2, width=12, textvariable=number5_ikat, font=("Arial", 14))
    number_chosen5_ikat['values'] = (selected_valuei1.get(), selected_valuei2.get())
    number_chosen5_ikat.grid(column=0, row=0, padx=3, pady=3)
    number_chosen5_ikat.current(0)

#INI ADALAH SEPARATOR UNTUK LANJUTAN INPUT
#membuat global value1 dan value2 untuk new_window3 dan new_window4
#selected_1 = tk.StringVar()
#selected_2 = tk.StringVar()
#selected_3 = tk.StringVar()

def new_window_3new():

    #Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background = background_color)

    #Label Frame
    label_frame3 = ttk.Labelframe(win, text=' PENDEFINISIAN TITIK ', padding=(30,60), style= 'Custom.TLabelframe')

    # Label Frame Dokumen
    label_frame4 = ttk.Labelframe(label_frame3, text=' Dokumen ', padding=(80,5), style='Custom.TLabelframe')
    label_frame4.grid(column=2, row=0, padx=8, pady=8, columnspan=5)
    
    #doc
    cara = """
    1. Input koordinat berdiri alat dan backsight, sesuai koordinat pada data ukur
    2. Isikan sesuai dengan formulir ukur (semua nilai diisi)
    3. Jika koordinat tidak memiliki simpangan baku, maka kosongkan nilai tersebut.
    """

    # Label
    l2 = Label(label_frame4, text=cara,background=background_color, font=("calibri",14), foreground="white", justify="left")
    l4 = Label(label_frame3, text="TITIK PANTAU", background=background_color, font=("calibri",22), foreground="white")

    l2_1 = Label(label_frame3, text="Berdiri Alat", background=background_color, font=("calibri",16), foreground="white")
    l2_2 = Label(label_frame3, text="Koordinat X", background=background_color, font=("calibri",16), foreground="white")
    l2_3 = Label(label_frame3, text="Koordinat Y", background=background_color, font=("calibri",16), foreground="white")
    l2_4 = Label(label_frame3, text="Simpangan Baku X", background=background_color, font=("calibri",16), foreground="white")
    l2_5 = Label(label_frame3, text="Simpangan Baku Y", background=background_color, font=("calibri",16), foreground="white")

    l3_1 = Label(label_frame3, text="Backsight", background=background_color, font=("calibri",16), foreground="white")
    l3_2 = Label(label_frame3, text="Koordinat X", background=background_color, font=("calibri",16), foreground="white")
    l3_3 = Label(label_frame3, text="Koordinat Y", background=background_color, font=("calibri",16), foreground="white")
    l3_4 = Label(label_frame3, text="Simpangan Baku X", background=background_color, font=("calibri",16), foreground="white")
    l3_5 = Label(label_frame3, text="Simpangan Baku Y", background=background_color, font=("calibri",16), foreground="white")

    def continue_to_new_window3():
        new_window_4new()
        label_frame3.destroy()

    #Fungsi untuk menyimpan data ke database
    def save_data():
        global selected_file_path
        try:
            # Mengambil nilai dari entry dan combobox
            sta1_x = float(e1.get())
            sta1_y = float(e2.get())
            sta2_x = float(e3.get())
            sta2_y = float(e4.get())
            stdev_1_x = float(sd1.get())
            stdev_1_y = float(sd2.get())
            stdev_2_x = float(sd3.get())
            stdev_2_y = float(sd4.get())
            titik_pantau = selected_value3.get()
            selected_value_combobox1 = number_chosen1.get()
            selected_value_combobox2 = number_chosen2.get()

            # Menyimpan ke database
            if selected_file_path is None:
                print("Database belum dipilih atau tidak ada.")
                return
            
            #menyimpan ke database
            conn = sqlite3.connect(selected_file_path)
            cursor = conn.cursor()

            #untuk menambah nilai data_id
            connect_id =  sqlite3.connect(selected_file_path)
            curs = connect_id.cursor()
            curs.execute('SELECT COUNT(*) FROM Pendefinisian_Titik_T2')
            count = curs.fetchone()[0] + 1
            data_id = f"data{count}"
            connect_id.close() # menutup koneksi

            try:
                # Memeriksa apakah Titik_Pantau sudah ada
                cursor.execute("SELECT 1 FROM Pendefinisian_Titik_T2 WHERE Titik_Pantau = ?", (titik_pantau,))
                exists = cursor.fetchone()
                
                if exists:
                    print("Titik_Pantau sudah ada. Masukkan nilai yang berbeda.")
                else:
                    cursor.execute("""INSERT INTO Pendefinisian_Titik_T2
                                      (data_id, Titik_Pantau, STA1, sta1_x, sta1_y, STA2, sta2_x, sta2_y)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                   (data_id, titik_pantau, selected_value_combobox1, sta1_x, sta1_y, selected_value_combobox2, sta2_x, sta2_y))
                    cursor.execute(""" INSERT INTO Simpangan_Baku_T2 
                                 (STA1, stdev_x_sta1, stdev_y_sta1, STA2, stdev_x_sta2, stdev_y_sta2)
                                VALUES (?, ?, ?, ?, ?, ?)""",
                                (selected_value_combobox1, stdev_1_x, stdev_1_y, selected_value_combobox2, stdev_2_x, stdev_2_y))
                    conn.commit()
                    print("Data berhasil disimpan.")
            except sqlite3.Error as e:
                print(f"An Error occured: {e}")
            finally:
                messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
                conn.close()
        except ValueError:
            print("Nilai koordinat harus berupa angka.")

    # Tombol
    save = Button(label_frame3, text="Simpan", font=("calibri",16),bg="#FFC900", command=save_data, width=10) 
    cntn = Button(label_frame3, text="Lanjut", font=("calibri",16),bg="#FFC900", command=lambda:continue_to_new_window3(), width=10)

    #Adding a Text box Entry Widget
    e1 = DoubleVar()
    en1 = Entry(label_frame3, textvariable = e1)
    e2 = DoubleVar()
    en2 = Entry(label_frame3, textvariable = e2)
    e3 = DoubleVar()
    en3 = Entry(label_frame3, textvariable = e3)
    e4 = DoubleVar()
    en4 = Entry(label_frame3, textvariable = e4)

    stdev1 = DoubleVar()
    sd1 = Entry(label_frame3, textvariable=stdev1)
    stdev2 = DoubleVar()
    sd2 = Entry(label_frame3, textvariable=stdev2)
    stdev3 = DoubleVar()
    sd3 = Entry(label_frame3, textvariable=stdev3)
    stdev4 = DoubleVar()
    sd4 = Entry(label_frame3, textvariable=stdev4)

    # Grid
    label_frame3.grid(column=0, row=1, padx=8, pady=8)

    l2.grid(column=2, row=0, padx=3, pady=3, columnspan=5, sticky="w")
    l4.grid(column=4, row=5, padx=3, pady=3, sticky=" ")

    l2_1.grid(column=2, row=1, padx=3, pady=3, sticky=" ")
    l2_2.grid(column=3, row=1, padx=3, pady=3, sticky=" ")
    l2_3.grid(column=4, row=1, padx=3, pady=3, sticky=" ")
    l2_4.grid(column=5, row=1, padx=3, pady=3, sticky=" ")
    l2_5.grid(column=6, row=1, padx=3, pady=3, sticky=" ")

    l3_1.grid(column=2, row=3, padx=3, pady=3, sticky=" ")
    l3_2.grid(column=3, row=3, padx=3, pady=3, sticky=" ")
    l3_3.grid(column=4, row=3, padx=3, pady=3, sticky=" ")
    l3_4.grid(column=5, row=3, padx=3, pady=3, sticky=" ")
    l3_5.grid(column=6, row=3, padx=3, pady=3, sticky=" ")

    save.grid(column=0, row=7, padx=3, pady=3)
    cntn.grid(column=7, row=7, padx=3, pady=3)

    en1.grid(column=3, row=2, padx=3, pady=3)
    en2.grid(column=4, row=2, padx=3, pady=3)
    en3.grid(column=3, row=4, padx=3, pady=3)
    en4.grid(column=4, row=4, padx=3, pady=3)

    sd1.grid(column=5, row=2, padx=3, pady=3)
    sd2.grid(column=6, row=2, padx=3, pady=3)
    sd3.grid(column=5, row=4, padx=3, pady=3)
    sd4.grid(column=6, row=4, padx=3, pady=3)

    # Combobox1
    number1 = tk.StringVar()
    number_chosen1 = ttk.Combobox(label_frame3, width=12, textvariable=number1, font=("calibri",12))
    number_chosen1['values'] = ('W1', 'P8', 'PRB3', 'B5', 'S2', 'S1', 'S8', 'P10', 'Z2', 'PRB2', 'B3')
    number_chosen1.grid(column=2, row=2, padx=3, pady=3)
    number_chosen1.current(0)

    # Combobox2
    number2 = tk.StringVar()
    number_chosen2 = ttk.Combobox(label_frame3, width=12, textvariable=number2, font=("calibri",12))
    number_chosen2['values'] = ('W1', 'P8', 'PRB3', 'B5', 'S2', 'S1', 'S8', 'P10', 'Z2', 'PRB2', 'B3')
    number_chosen2.grid(column=2, row=4, padx=3, pady=3)
    number_chosen2.current(0)
    
    # Update selected values for comboboxes 1 and 2
    def update_selected_values():
        selected_value1.set(number_chosen1.get())
        selected_value2.set(number_chosen2.get())

    number_chosen1.bind("<<ComboboxSelected>>", lambda event: update_selected_values())
    number_chosen2.bind("<<ComboboxSelected>>", lambda event: update_selected_values())
    #Combobox3
    number3 = tk.StringVar()
    number_chosen3 = ttk.Combobox(label_frame3, width = 12, textvariable=number3, font=("calibri",12))
    number_chosen3['values'] = ('Nu','Gb','Gs','Nb','Au','Ab','Gt','Nt','At','Wt','Ws','St','Bu','Bt','Ss','Wb','Sb','Su','Bb')
    number_chosen3.grid(column=4,row=6,padx=3,pady=3, sticky=" ")
    number_chosen3.current(0)
    number_chosen3.bind("<<ComboboxSelected>>", lambda event: selected_value3.set(number_chosen3.get()))

    # Menggunakan variabel global untuk menyimpan referensi ke jendela baru
    global new_window
    new_window = label_frame3  

def new_window_3new_T4():
    global selected_file_path
    #Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background = background_color)

    #Label Frame
    label_frame3 = ttk.Labelframe(win, text=' PENDEFINISIAN TITIK ', padding=(30,40), style= 'Custom.TLabelframe')
    #label frame doc
    label_frame_doc = ttk.Labelframe(label_frame3, text=' Informasi ', padding=(60,10), style= 'Custom.TLabelframe')
    label_frame_doc.grid(column=3, row=0, columnspan=2, pady=10, padx=10)

    #doc
    cara = """
    1. Input koordinat berdiri alat dan backsight, sesuai koordinat pada data ukur
    2. Jika titik berdiri alat yang digunakan hanya 3, maka isikan sesuai dengan formulir ukur (semua nilai diisi)
    3. Jika koordinat tidak memiliki simpangan baku, maka kosongkan nilai tersebut.
    """
    info = Label(label_frame_doc, text=cara, background=background_color, font=("calibri",14), foreground="white", justify="left")
    info.grid(column=0,row=0,padx=5,pady=5, sticky="ew")

    #label frame & grid (untuk memisah pengisian koordinat)
    label_frame4 = ttk.Labelframe(label_frame3, text=' PENDEFINISIAN TITIK ', padding=(30,60), style= 'Custom.TLabelframe')
    label_frame4.grid(column=3, row=1, pady=10, padx=10)

    label_frame5 = ttk.Labelframe(label_frame3, text=' PENDEFINISIAN TITIK ', padding=(30,60), style= 'Custom.TLabelframe')
    label_frame5.grid(column=4, row=1, pady=10, padx=10)

    #Label
    l0 = Label(label_frame4,text="Backsight 1", background=background_color, font=("calibri",14, "bold") , foreground="white")
    l1 = Label(label_frame5,text="Backsight 2", background=background_color, font=("calibri",14, "bold"), foreground="white")

    l0_1 = Label(label_frame4, text="Prisma", background=background_color, font=("calibri",10), foreground="white")
    l0_2 = Label(label_frame4, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l0_3 = Label(label_frame4, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l0_4 = Label(label_frame4, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l0_5 = Label(label_frame4, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")

    l1_1 = Label(label_frame5, text="Prisma", background=background_color, font=("calibri",10), foreground="white")
    l1_2 = Label(label_frame5, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l1_3 = Label(label_frame5, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l1_4 = Label(label_frame5, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l1_5 = Label(label_frame5, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")
    #
    l2 = Label(label_frame4,text="STA 1", background=background_color, font=("calibri",14, "bold"), foreground="white")
    l3 = Label(label_frame5,text="STA 2", background=background_color, font=("calibri",14, "bold"), foreground="white")

    l2_1 = Label(label_frame4, text="Berdiri Alat", background=background_color, font=("calibri",10), foreground="white")
    l2_2 = Label(label_frame4, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l2_3 = Label(label_frame4, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l2_4 = Label(label_frame4, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l2_5 = Label(label_frame4, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")

    l3_1 = Label(label_frame5, text="Berdiri Alat", background=background_color, font=("calibri",10), foreground="white")
    l3_2 = Label(label_frame5, text="Koordinat X", background=background_color, font=("calibri",10), foreground="white")
    l3_3 = Label(label_frame5, text="Koordinat Y", background=background_color, font=("calibri",10), foreground="white")
    l3_4 = Label(label_frame5, text="Simpangan Baku X", background=background_color, font=("calibri",10), foreground="white")
    l3_5 = Label(label_frame5, text="Simpangan Baku Y", background=background_color, font=("calibri",10), foreground="white")

    l4 = Label(label_frame3, text="TITIK PANTAU", background=background_color,font=("calibri",14, "bold"), foreground="white")
    
    def continue_to_new_window_4new_T4():
        new_window_4new_T4()
        label_frame3.destroy()

    #Fungsi untuk menyimpan data ke database
    def save_data():
        global selected_file_path
        #mengambil nilai dari entry dan combobox
        sta_1_x = float(e1.get())
        sta_1_y = float(e2.get())
        sta_2_x = float(e3.get())
        sta_2_y = float(e4.get())
        bs_1_x = float(e1i.get())
        bs_1_y = float(e2i.get())
        bs_2_x = float(e3i.get())
        bs_2_y = float(e4i.get())
        stdev_1_x = float(sd1.get())
        stdev_1_y = float(sd2.get())
        stdev_2_x = float(sd3.get())
        stdev_2_y = float(sd4.get())
        stdev_i1_x = float(sd1i.get())
        stdev_i1_y = float(sd2i.get())
        stdev_i2_x = float(sd3i.get())
        stdev_i2_y = float(sd4i.get())
        titik_pantau = selected_value3.get()
        selected_value_combobox1 = number_chosen1.get()
        selected_value_combobox2 = number_chosen2.get()
        selected_value_comboboxi1 = number_choseni1.get()
        selected_value_comboboxi2 = number_choseni2.get()

        #menyimpan ke database
        connection = sqlite3.connect(selected_file_path)
        cursor = connection.cursor()

        #untuk menambah nilai data_id
        connect_id =  sqlite3.connect(selected_file_path)
        curs = connect_id.cursor()
        curs.execute('SELECT COUNT(*) FROM Pendefinisian_Titik_T4')
        count = curs.fetchone()[0] + 1
        data_id = f"data{count}"
        
        try:
             # Memeriksa apakah Titik_Pantau sudah ada
            cursor.execute("SELECT 1 FROM Pendefinisian_Titik_T4 WHERE Titik_Pantau = ?", (titik_pantau,))
            exists = cursor.fetchone()
            
            if exists:
                print("Titik_Pantau sudah ada. Masukkan nilai yang berbeda.")
            else:
                # Menyimpan data ke `Pendefinisian_Titik_T4`
                cursor.execute("""INSERT INTO Pendefinisian_Titik_T4
                                (data_id, Titik_Pantau, STA_1, sta_1_x, sta_1_y, STA_2, sta_2_x, sta_2_y, BS_1, bs_1_x, bs_1_y, BS_2, bs_2_x, bs_2_y)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (data_id, titik_pantau, selected_value_combobox1, sta_1_x, sta_1_y, selected_value_combobox2, sta_2_x, sta_2_y, 
                                selected_value_comboboxi1, bs_1_x, bs_1_y, selected_value_comboboxi2, bs_2_x, bs_2_y))
                
                # Menyimpan data ke `Simpangan_Baku_T4`
                cursor.execute("""INSERT INTO Simpangan_Baku_T4
                                (STA_1, stdev_1_x, stdev_1_y, STA_2, stdev_2_x, stdev_2_y, BS_1, stdev_i1_x, stdev_i1_y, BS_2, stdev_i2_x, stdev_i2_y)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (selected_value_combobox1, stdev_1_x, stdev_1_y, selected_value_combobox2, stdev_2_x, stdev_2_y, 
                                selected_value_comboboxi1, stdev_i1_x, stdev_i1_y, selected_value_comboboxi2, stdev_i2_x, stdev_i2_y))

                connection.commit()
                print("Data berhasil disimpan.")
            
        except sqlite3.Error as e:
            print(f"An Error occured: {e}")
        finally:
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            connection.close()

    #Tombol
    save = Button(label_frame3, text="Simpan", command= save_data, font=("arial", 14),bg="#FFC900") 
    cntn = Button(label_frame3, text="Lanjut", command=lambda:continue_to_new_window_4new_T4(), font=("arial", 14),bg="#FFC900")

    #Adding a Text box Entry Widget
    e1i = DoubleVar()
    en1i = Entry(label_frame4, textvariable = e1i)
    e2i = DoubleVar()
    en2i = Entry(label_frame4, textvariable = e2i)
    e3i = DoubleVar()
    en3i = Entry(label_frame5, textvariable = e3i)
    e4i = DoubleVar()
    en4i = Entry(label_frame5, textvariable = e4i)

    stdev_e1i = DoubleVar()
    sd1i = Entry(label_frame4, textvariable = stdev_e1i)
    stdev_e2i = DoubleVar()
    sd2i = Entry(label_frame4, textvariable = stdev_e2i)
    stdev_e3i = DoubleVar()
    sd3i = Entry(label_frame5, textvariable = stdev_e3i)
    stdev_e4i = DoubleVar()
    sd4i = Entry(label_frame5, textvariable = stdev_e4i)

    e1 = DoubleVar()
    en1 = Entry(label_frame4, textvariable = e1)
    e2 = DoubleVar()
    en2 = Entry(label_frame4, textvariable = e2)
    e3 = DoubleVar()
    en3 = Entry(label_frame5, textvariable = e3)
    e4 = DoubleVar()
    en4 = Entry(label_frame5, textvariable = e4)

    stdev_e1 = DoubleVar()
    sd1 = Entry(label_frame4, textvariable = stdev_e1)
    stdev_e2 = DoubleVar()
    sd2 = Entry(label_frame4, textvariable = stdev_e2)
    stdev_e3 = DoubleVar()
    sd3 = Entry(label_frame5, textvariable = stdev_e3)
    stdev_e4 = DoubleVar()
    sd4 = Entry(label_frame5, textvariable = stdev_e4)
    #Grid
    label_frame3.grid(column=0, row=1, padx=8, pady=8)

    l0.grid(column=3, row=3,padx=3,pady=3, columnspan=3, sticky=" ")
    l0_1.grid(column=2, row=4,padx=3,pady=3, sticky=" ")
    l0_2.grid(column=3, row=4,padx=3,pady=3, sticky=" ")
    l0_3.grid(column=4, row=4,padx=3,pady=3, sticky=" ")
    l0_4.grid(column=5, row=4,padx=3,pady=3, sticky=" ")
    l0_5.grid(column=6, row=4,padx=3,pady=3, sticky=" ")

    l1.grid(column=3, row=9,padx=3,pady=3, columnspan=3, sticky=" ")
    l1_1.grid(column=2, row=10,padx=3,pady=3, sticky=" ")
    l1_2.grid(column=3, row=10,padx=3,pady=3, sticky=" ")
    l1_3.grid(column=4, row=10,padx=3,pady=3, sticky=" ")
    l1_4.grid(column=5, row=10,padx=3,pady=3, sticky=" ")
    l1_5.grid(column=6, row=10,padx=3,pady=3, sticky=" ")

    l2.grid(column=3, row=0,padx=3,pady=3, columnspan=3, sticky=" ")
    l2_1.grid(column=2, row=1,padx=3,pady=3, sticky=" ")
    l2_2.grid(column=3, row=1,padx=3,pady=3, sticky=" ")
    l2_3.grid(column=4, row=1,padx=3,pady=3, sticky=" ")
    l2_4.grid(column=5, row=1,padx=3,pady=3, sticky=" ")
    l2_5.grid(column=6, row=1,padx=3,pady=3, sticky=" ")

    l3.grid(column=3, row=6,padx=3,pady=3, columnspan=3, sticky=" ")
    l3_1.grid(column=2, row=7,padx=3,pady=3, sticky=" ")
    l3_2.grid(column=3, row=7,padx=3,pady=3, sticky=" ")
    l3_3.grid(column=4, row=7,padx=3,pady=3, sticky=" ")
    l3_4.grid(column=5, row=7,padx=3,pady=3, sticky=" ")
    l3_5.grid(column=6, row=7,padx=3,pady=3, sticky=" ")

    l4.grid(column=3, row=12,padx=3,pady=3, columnspan=3, sticky=" ")

    save.grid(column=3,row=12, padx=3, pady=3, sticky='w')
    cntn.grid(column=4,row=12, padx=3, pady=3, sticky='e')

    en1i.grid(column = 3, row = 5, padx=3, pady=3)
    en2i.grid(column = 4, row = 5, padx=3, pady=3)
    sd1i.grid(column = 5, row = 5, padx=3, pady=3)
    sd2i.grid(column = 6, row = 5, padx=3, pady=3)

    en3i.grid(column = 3, row = 11, padx=3, pady=3)
    en4i.grid(column = 4, row = 11, padx=3, pady=3)
    sd3i.grid(column = 5, row = 11, padx=3, pady=3)
    sd4i.grid(column = 6, row = 11, padx=3, pady=3)

    en1.grid(column = 3, row = 2, padx=3, pady=3)
    en2.grid(column = 4, row = 2, padx=3, pady=3)
    sd1.grid(column = 5, row = 2, padx=3, pady=3)
    sd2.grid(column = 6, row = 2, padx=3, pady=3)

    en3.grid(column = 3, row = 8, padx=3, pady=3)
    en4.grid(column = 4, row = 8, padx=3, pady=3)
    sd3.grid(column = 5, row = 8, padx=3, pady=3)
    sd4.grid(column = 6, row = 8, padx=3, pady=3)

    #Combobox1
    number1 = tk.StringVar()
    number_chosen1 = ttk.Combobox(label_frame4, width = 12, textvariable=number1, font=("calibri",12))
    number_chosen1['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_chosen1.grid(column=2,row=2,padx=3,pady=3)
    number_chosen1.current(0)

    #Combobox2
    number2 = tk.StringVar()
    number_chosen2 = ttk.Combobox(label_frame5, width = 12, textvariable=number2, font=("calibri",12))
    number_chosen2['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_chosen2.grid(column=2,row=8,padx=3,pady=3)
    number_chosen2.current(0)

    #Combobox ikat 1
    number_i1 = tk.StringVar()
    number_choseni1 = ttk.Combobox(label_frame4, width = 12, textvariable=number_i1, font=("calibri",12))
    number_choseni1['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_choseni1.grid(column=2,row=5,padx=3,pady=3)
    number_choseni1.current(0)

    #Combobox ikat 2
    number_i2 = tk.StringVar()
    number_choseni2 = ttk.Combobox(label_frame5, width = 12, textvariable=number_i2, font=("calibri",12))
    number_choseni2['values'] = ('W1','P8','PRB3','B5','S2','S1','S8','P10','Z2','PRB2','B3')
    number_choseni2.grid(column=2,row=11,padx=3,pady=3)
    number_choseni2.current(0)
    

    def update_selected_values():
        selected_value1.set(number_chosen1.get())
        selected_value2.set(number_chosen2.get())

    number_chosen1.bind("<<ComboboxSelected>>", lambda event: update_selected_values())
    number_chosen2.bind("<<ComboboxSelected>>", lambda event: update_selected_values())

    def update_selected_values_ikat():
        selected_valuei1.set(number_choseni1.get())
        selected_valuei2.set(number_choseni2.get())

    number_choseni1.bind("<<ComboboxSelected>>", lambda event: update_selected_values_ikat())
    number_choseni2.bind("<<ComboboxSelected>>", lambda event: update_selected_values_ikat())

    #Combobox3
    number3 = tk.StringVar()
    number_chosen3 = ttk.Combobox(label_frame3, width = 12, textvariable=number3, font=("calibri",12))
    number_chosen3['values'] = ('Nu','Gb','Gs','Nb','Au','Ab','Gt','Nt','At','Wt','Ws','St','Bu','Bt','Ss','Wb','Sb','Su','Bb')
    number_chosen3.grid(column=3,row=13,padx=3, columnspan=3, sticky=" ")
    number_chosen3.current(0)
    number_chosen3.bind("<<ComboboxSelected>>", lambda event: selected_value3.set(number_chosen3.get()))

    # Menggunakan variabel global untuk menyimpan referensi ke jendela baru
    global new_window
    new_window = label_frame3 

def new_window_4new():
    #Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background = background_color)
    
    def convert_to_decimal_degree(degree1, degree2, minute1, minute2, second1, second2):
        DD_t = degree1 + (minute1 / 60) + (second1 / 3600)
        DD_i = degree2 + (minute2 / 60) + (second2 / 3600)

        if DD_i > DD_t:
            delta = DD_i - DD_t
            if delta > 180:
                delta = 360 - delta
        else:
            delta = DD_t - DD_i
            if delta > 180:
                delta = 360 - delta

        print(f"Nilai Sudut: {delta}")
        return delta


    # Definisi fungsi save_data di sini
    def save_data():
        global selected_file_path
        # Mengambil nilai dari entry dan mengonversinya ke Decimal Degree
        sudut_biasa = convert_to_decimal_degree(float(en1.get()), float(enf1.get()), float(en3.get()), float(enf3.get()), float(en5.get()), float(enf5.get())) 
        sudut_luar_biasa = convert_to_decimal_degree(float(en2.get()), float(enf2.get()), float(en4.get()), float(enf4.get()), float(en6.get()), float(enf6.get())) 

        # Menentukan nilai STA dan Titik_Pantau berdasarkan pilihan combobox
        # Menentukan nilai Titik_Pantau
        selected_value = number_chosen4.get()
        value_pantau = selected_value3.get()
        
        
        # Menentukan nilai other_value berdasarkan selected_value
        selected_value_1_ = selected_value1.get()
        selected_value_2_ = selected_value2.get()

        if selected_value == selected_value_1_ + "_1":
            other_value = selected_value_2_ + "_1"
        elif selected_value == selected_value_2_ + "_1":
            other_value = selected_value_1_ + "_1"
        elif selected_value == selected_value_1_ + "_2":
            other_value = selected_value_2_ + "_2"
        elif selected_value == selected_value_2_ + "_2":
            other_value = selected_value_1_ + "_2"
        else:
            other_value = ""

        #menyimpan ke database
        conn = sqlite3.connect(selected_file_path)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO Sudut_T2 (STA_1, sudut_biasa, Titik_Pantau, STA_2, sudut_luar_biasa, Titik_Ikat ) VALUES (?, ?, ?, ?, ?, ?)",
                        (selected_value, sudut_biasa, value_pantau, selected_value, sudut_luar_biasa, other_value))
            conn.commit()
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            print("Data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        conn.close()

    # Label Frame
    label_frame4 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(30, 60), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK PANTAU", style='Custom.TLabelframe')
    input_frame2 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK BACKSIGHT", style='Custom.TLabelframe')
    input_frame3 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 1", padding=(3, 35), style='Custom.TLabelframe')
    input_frame4 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 2", padding=(3, 35), style='Custom.TLabelframe')

    # Label
    # Frame dan Label Informasi
    label_frame5 = ttk.Labelframe(label_frame4, text=' INFORMASI ', padding=(30, 30), style='Custom.TLabelframe')
    label_frame5.grid(column=1, row=1,rowspan=4, padx=8, pady=9)
    # Langkah-langkah input program
    
    steps = """
    NOTE: CARA INPUT DATA HASIL BACAAN SUDUT DAN JARAK
     

    1. Pilih combobox Berdiri Alat mulai dari Berdiri Alat 1 (Berdiri Alat 2 Tidak Dipilih).

    2. Pilih "kode Pantau_1", lalu input bacaan sudut ke Titik Pantau dan Titik Backsight.
    
    3. Klik "Simpan" untuk menyimpan data.
    
    4. Ulangi langkah nomor 1,2 dan 3 untuk "kode Pantau_2" hingga semua selesai.
    
    5. Pindah ke Berdiri Alat 2 dan ulangi langkah yang sama.
    
    6. Setelah seluruh data bacaan sudut pada satu titik pantau telah diisi. klik "lanjut"
    
    7. Isi data jarak pada tampilan berikutnya, lalu sesuaikan seri 1 dan 2 
    """

    # Tambahkan langkah-langkah ke dalam label baru
    label_steps = Label(label_frame5, text=steps, font=("Arial", 12,"bold"), justify="left", foreground="white", background=background_color)
    label_steps.grid(row=1, column=0, padx=10, pady=3, rowspan=5)

    # Label Frame 3
    kosong1 = Label(input_frame1, text=' ', background=background_color)
    derajat1 = Label(input_frame1, text='DERAJAT', font=("Arial", 14))
    menit1 = Label(input_frame1, text='MENIT', font=("Arial", 14))
    detik1 = Label(input_frame1, text='DETIK', font=("Arial", 14))
    B1 = Label(input_frame1, text="Biasa", background=background_color, font=("Arial", 14), foreground="white")
    Lb1 = Label(input_frame1, text="Luar Biasa", background=background_color, font=("Arial", 14), foreground="white")

    # Label Frame Input 2
    kosong2 = Label(input_frame2, text=' ', background=background_color)
    derajat2 = Label(input_frame2, text='DERAJAT', font=("Arial", 14))
    menit2 = Label(input_frame2, text='MENIT', font=("Arial", 14))
    detik2 = Label(input_frame2, text='DETIK', font=("Arial", 14))
    B2 = Label(input_frame2, text="Biasa", background=background_color, font=("Arial", 14), foreground="white")
    Lb2 = Label(input_frame2, text="Luar Biasa", background=background_color, font=("Arial", 14), foreground="white")

    # Tombol
    # Pindahkan pemanggilan save_data ke bawah definisi fungsi save_data
    save = Button(label_frame4, text="Simpan", command=save_data, font=("Arial", 14),bg="#FFC900")

    def continue_to_new_window4():
        new_window_5new()
        label_frame4.destroy()

    spasi = Label(label_frame4, text=" ", background=background_color)
    cntn = Button(label_frame4, text="Lanjut", command=lambda: continue_to_new_window4(), font=("Arial", 14),bg="#FFC900")

    # Adding a Text box Entry Widget

    # Degree, Minute, Second F1
    # Data input untuk PB
    e1 = tk.IntVar()
    en1 = Entry(input_frame1, textvariable=e1)
    e3 = tk.IntVar()
    en3 = Entry(input_frame1, textvariable=e3)
    e5 = tk.IntVar()
    en5 = Entry(input_frame1, textvariable=e5)

    # Data input untuk PLB
    e2 = tk.IntVar()
    en2 = Entry(input_frame1, textvariable=e2)
    e4 = tk.IntVar()
    en4 = Entry(input_frame1, textvariable=e4)
    e6 = tk.IntVar()
    en6 = Entry(input_frame1, textvariable=e6)

    # Degree, Minute, Second F2
    # Data input untuk IB
    ef1 = tk.IntVar()
    enf1 = Entry(input_frame2, textvariable=ef1)
    ef3 = tk.IntVar()
    enf3 = Entry(input_frame2, textvariable=ef3)
    ef5 = tk.IntVar()
    enf5 = Entry(input_frame2, textvariable=ef5)

    # Data input untuk ILB
    ef2 = tk.IntVar()
    enf2 = Entry(input_frame2, textvariable=ef2)
    ef4 = tk.IntVar()
    enf4 = Entry(input_frame2, textvariable=ef4)
    ef6 = tk.IntVar()
    enf6 = Entry(input_frame2, textvariable=ef6)

    # Grid
    label_frame4.grid(column=0, row=1, padx=8, pady=8)
    input_frame1.grid(column=4, row=1)
    input_frame2.grid(column=4, row=2)
    input_frame3.grid(column=3, row=1, padx=8, pady=9)
    input_frame4.grid(column=3, row=2, padx=8, pady=9)

    save.grid(column=1, row=5, padx=3, pady=3,sticky="w")
    spasi.grid(column=5, row=1, padx=3)
    cntn.grid(column=4, row=5, padx=3, pady=10, sticky="e")

    # Entry Grid F1
    B1.grid(column=0, row=1, padx=3, pady=3)
    Lb1.grid(column=0, row=3, padx=3, pady=3)
    en1.grid(column=1, row=1, padx=3, pady=3)
    en2.grid(column=1, row=3, padx=3, pady=3)
    en3.grid(column=2, row=1, padx=3, pady=3)
    en4.grid(column=2, row=3, padx=3, pady=3)
    en5.grid(column=3, row=1, padx=3, pady=3)
    en6.grid(column=3, row=3, padx=3, pady=3)

    # Entry Grid F2
    B2.grid(column=0, row=1, padx=3, pady=3)
    Lb2.grid(column=0, row=3, padx=3, pady=3)
    enf1.grid(column=1, row=1, padx=3, pady=3)
    enf2.grid(column=1, row=3, padx=3, pady=3)
    enf3.grid(column=2, row=1, padx=3, pady=3)
    enf4.grid(column=2, row=3, padx=3, pady=3)
    enf5.grid(column=3, row=1, padx=3, pady=3)
    enf6.grid(column=3, row=3, padx=3, pady=3)

    # Tambahan Entry Grid
    kosong1.grid(column=0, row=2)
    derajat1.grid(column=1, row=0, sticky=' ')
    menit1.grid(column=2, row=0, sticky=' ')
    detik1.grid(column=3, row=0, sticky=' ')

    # Tambahan Entry Grid
    kosong2.grid(column=0, row=2)
    derajat2.grid(column=1, row=0, sticky=' ')
    menit2.grid(column=2, row=0, sticky=' ')
    detik2.grid(column=3, row=0, sticky=' ')

    # Combobox_Berdiri alat 1
    number4 = tk.StringVar()
    number_chosen4 = ttk.Combobox(input_frame3, width=12, textvariable=number4)
    selected_value_1 = selected_value1.get()
    values = [selected_value_1 + "_1",selected_value_1 + "_2"]
    number_chosen4['values'] = values
    number_chosen4.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen4.current(0)

    #Combobox berdiri alat 2
    number_4 = tk.StringVar()
    number_chosen_4 = ttk.Combobox(input_frame4, width=12, textvariable=number_4)
    selected_value_2 = selected_value2.get()
    values_ = [selected_value_2 + "_1",selected_value_2 + "_2"]
    number_chosen_4['values'] = values_
    number_chosen_4.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen_4.current(0)

def new_window_4new_T4():
    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)
    
    def convert_to_decimal_degree(degree1, degree2, minute1, minute2, second1, second2):
        DD_t = degree1 + (minute1 / 60) + (second1 / 3600)
        DD_i = degree2 + (minute2 / 60) + (second2 / 3600)

        if DD_i > DD_t:
            delta = DD_i - DD_t
            if delta > 180:
                delta = 360 - delta
        else:
            delta = DD_t - DD_i
            if delta > 180:
                delta = 360 - delta

        print(f"Nilai Sudut: {delta}")
        return delta

    # Definisi fungsi save_data di sini
    def save_data():
        selected_file_path
        # Mengambil nilai dari entry dan mengonversinya ke Decimal Degree
        sudut_biasa = convert_to_decimal_degree(float(en1.get()), float(enf1.get()), float(en3.get()), float(enf3.get()), float(en5.get()), float(enf5.get()))  # PB
        sudut_luar_biasa = convert_to_decimal_degree(float(en2.get()), float(enf2.get()), float(en4.get()), float(enf4.get()), float(en6.get()), float(enf6.get()))  # PLB

        # Menentukan nilai Titik Pantau dan Titik Ikat dari combobox
        selected_value = number_chosen4.get() or number_chosen44.get()
        value_pantau = selected_value3.get()
        titik_ikat_value = number_chosen4_ikat.get() or number_chosen4_ikat2.get()

        # Menyimpan data ke dalam tabel Sudut
        connection = sqlite3.connect(selected_file_path)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Sudut_T4 (STA_1, sudut_biasa, Titik_Pantau, STA_2, sudut_luar_biasa, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                           (selected_value, sudut_biasa, value_pantau, selected_value, sudut_luar_biasa, titik_ikat_value))
            connection.commit()
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            print("Data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        connection.close()

    # Label Frame
    label_frame4 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(30, 40), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK PANTAU", style='Custom.TLabelframe')
    input_frame2 = ttk.Labelframe(label_frame4, padding=(3, 3), text="BACAAN SUDUT ALAT KE TITIK IKAT", style='Custom.TLabelframe')
    input_frame3 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 1", padding=(3, 35), style='Custom.TLabelframe')
    input_frame33 = ttk.Labelframe(label_frame4, text="BERDIRI ALAT 2", padding=(3, 35), style='Custom.TLabelframe')

    # Label
        # Frame dan Label Informasi
    label_frame5 = ttk.Labelframe(label_frame4, text=' INFORMASI ', padding=(30, 30), style='Custom.TLabelframe')
    label_frame5.grid(column=1, row=1,rowspan=4, padx=8, pady=9)
    # Langkah-langkah input program
    
    steps = """
    NOTE: CARA INPUT DATA HASIL BACAAN SUDUT DAN JARAK
     

    1. Pilih combobox Berdiri Alat mulai dari Berdiri Alat 1 (Berdiri Alat 2 Tidak Dipilih).

    2. Pilih kode pada berdiri alat dan sesuaikan kode untuk backsightnya 
       (urutannya sesuai berdiri alat 1 dan 2)
    
    3. Lalu input bacaan sudut Titik Pantau dan Titik Backsight.
    
    4. Klik "Simpan" untuk menyimpan data.
    
    5. Ulangi langkah nomor 1, 2, 3 dan 4 untuk kode berdiri alat 2 hingga semua selesai.
    
    6. Pindah ke Berdiri Alat 2 dan ulangi langkah yang sama.
    
    7. Setelah seluruh data bacaan sudut pada satu titik pantau telah diisi. klik "lanjut"
    
    8. Isi data jarak pada tampilan berikutnya, lalu sesuaikan seri 1 dan 2 
    """
    
    # Tambahkan langkah-langkah ke dalam label baru
    label_steps = Label(label_frame5, text=steps, font=("Arial", 12, "bold"), background=background_color,foreground="white", justify="left")
    label_steps.grid(row=1, column=0, padx=10, pady=10)

    # Label Frame 3
    kosong1 = Label(input_frame1, text=' ', background=background_color)
    derajat1 = Label(input_frame1, text='DERAJAT', font=("Arial", 14))
    menit1 = Label(input_frame1, text='MENIT', font=("Arial", 14))
    detik1 = Label(input_frame1, text='DETIK', font=("Arial", 14))
    B1 = Label(input_frame1, text="Biasa", background=background_color, font=("Arial", 14), foreground="white")
    Lb1 = Label(input_frame1, text="Luar Biasa", background=background_color, font=("Arial", 14), foreground="white")

    # Label Frame Input 2
    kosong2 = Label(input_frame2, text=' ', background=background_color)
    derajat2 = Label(input_frame2, text='DERAJAT', font=("Arial", 14))
    menit2 = Label(input_frame2, text='MENIT', font=("Arial", 14))
    detik2 = Label(input_frame2, text='DETIK', font=("Arial", 14))
    B2 = Label(input_frame2, text="Biasa", background=background_color, font=("Arial", 14), foreground="white")
    Lb2 = Label(input_frame2, text="Luar Biasa", background=background_color, font=("Arial", 14), foreground="white")

    # Tombol
    save = Button(label_frame4, text="Simpan", command=save_data, font=("Arial", 14),bg="#FFC900")

    def continue_to_new_window_4new_T4():
        new_window_5new_T4()
        label_frame4.destroy()

    spasi = Label(label_frame4, text=" ", background=background_color)
    cntn = Button(label_frame4, text="Lanjut", command=lambda: continue_to_new_window_4new_T4(), font=("Arial", 14),bg="#FFC900")

    # Adding a Text box Entry Widget

    # Degree, Minute, Second F1
    # Data input untuk PB
    e1 = tk.IntVar()
    en1 = Entry(input_frame1, textvariable=e1)
    e3 = tk.IntVar()
    en3 = Entry(input_frame1, textvariable=e3)
    e5 = tk.IntVar()
    en5 = Entry(input_frame1, textvariable=e5)

    # Data input untuk PLB
    e2 = tk.IntVar()
    en2 = Entry(input_frame1, textvariable=e2)
    e4 = tk.IntVar()
    en4 = Entry(input_frame1, textvariable=e4)
    e6 = tk.IntVar()
    en6 = Entry(input_frame1, textvariable=e6)

    # Degree, Minute, Second F2
    # Data input untuk IB
    ef1 = tk.IntVar()
    enf1 = Entry(input_frame2, textvariable=ef1)
    ef3 = tk.IntVar()
    enf3 = Entry(input_frame2, textvariable=ef3)
    ef5 = tk.IntVar()
    enf5 = Entry(input_frame2, textvariable=ef5)

    # Data input untuk ILB
    ef2 = tk.IntVar()
    enf2 = Entry(input_frame2, textvariable=ef2)
    ef4 = tk.IntVar()
    enf4 = Entry(input_frame2, textvariable=ef4)
    ef6 = tk.IntVar()
    enf6 = Entry(input_frame2, textvariable=ef6)

    # Grid
    label_frame4.grid(column=0, row=1, rowspan=4, padx=8, pady=8)
    input_frame1.grid(column=4, row=1)
    input_frame2.grid(column=4, row=3)
    input_frame3.grid(column=3, row=1, padx=8, pady=9)
    input_frame33.grid(column=3, row=3, padx=8, pady=9)

    save.grid(column=1, row=5, padx=3, pady=3, sticky="w")
    spasi.grid(column=5, row=1, padx=3)
    cntn.grid(column=4, row=5, padx=3, pady=3, sticky='e')

    # Entry Grid F1
    B1.grid(column=0, row=1, padx=3, pady=3)
    Lb1.grid(column=0, row=3, padx=3, pady=3)
    en1.grid(column=1, row=1, padx=3, pady=3)
    en2.grid(column=1, row=3, padx=3, pady=3)
    en3.grid(column=2, row=1, padx=3, pady=3)
    en4.grid(column=2, row=3, padx=3, pady=3)
    en5.grid(column=3, row=1, padx=3, pady=3)
    en6.grid(column=3, row=3, padx=3, pady=3)

    # Entry Grid F2
    B2.grid(column=0, row=2, padx=3, pady=3)
    Lb2.grid(column=0, row=4, padx=3, pady=3)
    enf1.grid(column=1, row=2, padx=3, pady=3)
    enf2.grid(column=1, row=4, padx=3, pady=3)
    enf3.grid(column=2, row=2, padx=3, pady=3)
    enf4.grid(column=2, row=4, padx=3, pady=3)
    enf5.grid(column=3, row=2, padx=3, pady=3)
    enf6.grid(column=3, row=4, padx=3, pady=3)

    # Tambahan Entry Grid
    kosong1.grid(column=0, row=2)
    derajat1.grid(column=1, row=0, sticky=' ')
    menit1.grid(column=2, row=0, sticky=' ')
    detik1.grid(column=3, row=0, sticky=' ')

    # Tambahan Entry Grid
    kosong2.grid(column=0, row=3)
    derajat2.grid(column=1, row=1, sticky=' ')
    menit2.grid(column=2, row=1, sticky=' ')
    detik2.grid(column=3, row=1, sticky=' ')

    # Combobox4 berdiri alat 1
    number4 = tk.StringVar()
    number_chosen4 = ttk.Combobox(input_frame3, width=12, textvariable=number4, font=("Arial", 12))
    selected_value_1 = selected_value1.get()
    selected_value_2 = selected_value2.get()
    values = [selected_value_1 + "_1", selected_value_1 + "_2"]
    number_chosen4['values'] = values
    number_chosen4.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen4.current(0)
    #berdiri alat 2
    number44 = tk.StringVar()
    number_chosen44 = ttk.Combobox(input_frame33, width=12, textvariable=number44, font=("Arial", 12))
    selected_value_2 = selected_value2.get()
    values = [selected_value_2 + "_1", selected_value_2 + "_2"]
    number_chosen44['values'] = values
    number_chosen44.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen44.current(0)

    # Combobox4 Ikat1
    number4_ikat = tk.StringVar()
    number_chosen4_ikat = ttk.Combobox(input_frame2, width=12, textvariable=number4_ikat, font=("Arial", 12))
    selected_value_1i = selected_valuei1.get()
    values = [selected_value_1i + "_1", selected_value_1i + "_2"]
    number_chosen4_ikat['values'] = values
    number_chosen4_ikat.grid(column=0, row=0, padx=3, pady=3)
    number_chosen4_ikat.current(0)

    # Combobox4 Ikat1
    number4_ikat2 = tk.StringVar()
    number_chosen4_ikat2 = ttk.Combobox(input_frame2, width=12, textvariable=number4_ikat2, font=("Arial", 12))
    selected_value_2i = selected_valuei2.get()
    values = [selected_value_2i + "_1", selected_value_2i + "_2"]
    number_chosen4_ikat2['values'] = values
    number_chosen4_ikat2.grid(column=0, row=1, padx=3, pady=3)
    number_chosen4_ikat2.current(0)

def new_window_5new():
    #Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background = background_color)

    # Label Frame
    label_frame5 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(60, 65), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame5, padding=(6, 6), text="JARAK KE TITIK PANTAU", style='Custom.TLabelframe')
    frame1_seri_1 = ttk.Labelframe(input_frame1, padding=(2, 2), text="Seri 1", style='Custom.TLabelframe')
    frame1_seri_2 = ttk.Labelframe(input_frame1, padding=(2, 2), text="Seri 2", style='Custom.TLabelframe')

    input_frame2 = ttk.Labelframe(label_frame5, padding=(6, 6), text="JARAK KE TITIK IKAT", style='Custom.TLabelframe')
    frame2_seri_1 = ttk.Labelframe(input_frame2, padding=(2, 2), text="Seri 1", style='Custom.TLabelframe')
    frame2_seri_2 = ttk.Labelframe(input_frame2, padding=(2, 2), text="Seri 2", style='Custom.TLabelframe')

    input_frame3 = ttk.Labelframe(label_frame5, text="BERDIRI ALAT", padding=(6, 80), style='Custom.TLabelframe')

    def continue_to_new_choice():
            window_choice()
            label_frame5.destroy()

    #pemisah antara lanjut dan input
    spasi = Label(label_frame5, text=" ", background=background_color)
    cntn = Button(label_frame5, text="Kembali", font=("Arial", 14),command=lambda:continue_to_new_choice(),bg="#FFC900")

    def save_data():
        global selected_file_path
        #Mengambil nilai dari entry dan konversi ke dalam format yang sesuai
        jarak_pantau_1 = [en1.get(),en2.get()]
        jarak_pantau_2 = [en3.get(),en4.get()]
        jarak_ikat_1 = [enf1.get(),enf2.get()]
        jarak_ikat_2 = [enf3.get(),enf4.get()]


        selected_value = number_chosen5.get()
        value_pantau = selected_value3.get()
        other_value = selected_value1.get() if selected_value == selected_value2.get() else selected_value2.get()

        # Koneksikan ke database yang sudah dibuat sebelumnya
        conn = sqlite3.connect(selected_file_path)
        cursor = conn.cursor()

        try:    
            # Simpan data ke dalam tabel Jarak
            for jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2  in zip (jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2):
                if jarak_pantau_1 and jarak_pantau_2 and jarak_ikat_1 and jarak_ikat_2: #memastikan tidak ada nilai yang kosong
                    cursor.execute("INSERT INTO Jarak_T2 (STA_1, Jarak_P,Titik_Pantau, STA_2, Jarak_I, Titik_Ikat ) VALUES (?, ?, ?, ?, ?, ?)", 
                                (selected_value + '_1', jarak_pantau_1, value_pantau, selected_value + '_1', jarak_ikat_1, other_value))
                    cursor.execute("INSERT INTO Jarak_T2  (STA_1, Jarak_P,Titik_Pantau, STA_2, Jarak_I, Titik_Ikat ) VALUES (?, ?, ?, ?, ?, ?)", 
                                (selected_value + '_2', jarak_pantau_2, value_pantau, selected_value + '_2', jarak_ikat_2, other_value))
            conn.commit()
            print("data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            conn.close()

    # Tombol
    save = Button(label_frame5, text="Simpan", font=("Arial", 14), command=save_data,bg="#FFC900")


    #Adding a Text box Entry Widget
    #Jarak dari berdiri alat ke titik pantau
    e1 = tk.DoubleVar()
    en1 = Entry(frame1_seri_1, textvariable=e1, font=("Arial", 12))
    e2 = tk.DoubleVar()
    en2 = Entry(frame1_seri_1, textvariable=e2, font=("Arial", 12))
    e3 = tk.DoubleVar()
    en3 = Entry(frame1_seri_2, textvariable=e3, font=("Arial", 12))
    e4 = tk.DoubleVar()
    en4 = Entry(frame1_seri_2, textvariable=e4, font=("Arial", 12))

    # Jarak dari berdiri alat ke titik ikat
    ef1 = tk.DoubleVar()
    enf1 = Entry(frame2_seri_1, textvariable=ef1, font=("Arial", 12))
    ef2 = tk.DoubleVar()
    enf2 = Entry(frame2_seri_1, textvariable=ef2, font=("Arial", 12))
    ef3 = tk.DoubleVar()
    enf3 = Entry(frame2_seri_2, textvariable=ef3, font=("Arial", 12))
    ef4 = tk.DoubleVar()
    enf4 = Entry(frame2_seri_2, textvariable=ef4, font=("Arial", 12))

    # Grid
    label_frame5.grid(column=0, row=1, padx=10, pady=10)
    input_frame1.grid(column=4, row=1, padx=10, pady=10)
    frame1_seri_1.grid(column=0, row=1)
    frame1_seri_2.grid(column=0, row=2)

    input_frame2.grid(column=4, row=2, padx=10, pady=10)
    frame2_seri_1.grid(column=0, row=1)
    frame2_seri_2.grid(column=0, row=2)
    input_frame3.grid(column=3, row=1, padx=10, pady=10)

    save.grid(column=2, row=5, padx=6, pady=6)
    spasi.grid(column=5, row=1, padx=6)
    cntn.grid(column=6, row=5, padx=6, pady=6)

    # Entry Grid F1
    en1.grid(column=0, row=1, padx=6, pady=6)
    en2.grid(column=0, row=2, padx=6, pady=6)
    en3.grid(column=0, row=3, padx=6, pady=6)
    en4.grid(column=0, row=4, padx=6, pady=6)

    # Entry Grid F2
    enf1.grid(column=0, row=1, padx=6, pady=6)
    enf2.grid(column=0, row=2, padx=6, pady=6)
    enf3.grid(column=0, row=3, padx=6, pady=6)
    enf4.grid(column=0, row=4, padx=6, pady=6)

    # Combobox5
    number5 = tk.StringVar()
    number_chosen5 = ttk.Combobox(input_frame3, width=12, textvariable=number5, font=("Arial", 16))
    number_chosen5['values'] = (selected_value1.get(), selected_value2.get())
    number_chosen5.grid(column=0, row=0, padx=6, pady=6, rowspan=3)
    number_chosen5.current(0)

def new_window_5new_T4():
    # Menambahkan warna latar belakang baru ke dalam style
    style.configure('Custom.TLabelframe', background=background_color)

    # Label Frame
    label_frame5 = ttk.Labelframe(win, text=' INPUT DATA ', padding=(30, 60), style='Custom.TLabelframe')
    input_frame1 = ttk.Labelframe(label_frame5, padding=(3, 3), text="JARAK KE TITIK PANTAU", style='Custom.TLabelframe')
    frame1_seri_1 = ttk.Labelframe(input_frame1, padding=(1,1), text="Seri 1", style= 'Custom.TLabelframe')
    frame1_seri_2 = ttk.Labelframe(input_frame1, padding=(1,1), text="Seri 2", style= 'Custom.TLabelframe')

    input_frame2 = ttk.Labelframe(label_frame5, padding=(3, 3), text="JARAK KE TITIK IKAT", style='Custom.TLabelframe')
    frame2_seri_1 = ttk.Labelframe(input_frame2, padding=(1,1), text="Seri 1", style= 'Custom.TLabelframe')
    frame2_seri_2 = ttk.Labelframe(input_frame2, padding=(1,1), text="Seri 2", style= 'Custom.TLabelframe')

    input_frame3 = ttk.Labelframe(label_frame5, text="BERDIRI ALAT", padding=(3, 63), style='Custom.TLabelframe')

    def continue_to_new_choice():
        window_choice()
        label_frame5.destroy()

    # pemisah antara lanjut dan input
    spasi = Label(label_frame5, text=" ", background=background_color)
    cntn = Button(label_frame5, text="Kembali", command=lambda: continue_to_new_choice(), font=("Arial", 14),bg="#FFC900")

    def save_data():
        # Mengambil nilai dari entry dan konversi ke dalam format yang sesuai
        jarak_pantau_1 = [en1.get(),en2.get()]
        jarak_pantau_2 = [en3.get(),en4.get()]
        jarak_ikat_1 = [enf1.get(),enf2.get()]
        jarak_ikat_2 = [enf3.get(),enf4.get()]

        selected_value = number_chosen5.get()
        value_pantau = selected_value3.get()
        titik_ikat_value = number_chosen5_ikat.get()

        # Koneksikan ke database yang sudah dibuat sebelumnya
        connection = sqlite3.connect(selected_file_path)
        cursor = connection.cursor()

        try:
            # Simpan data ke dalam tabel Jarak
            for jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2 in zip(jarak_pantau_1, jarak_pantau_2, jarak_ikat_1, jarak_ikat_2):
                if jarak_pantau_1 and jarak_pantau_2 and jarak_ikat_1 and jarak_ikat_2:  # memastikan tidak ada nilai yang kosong
                    cursor.execute("INSERT INTO Jarak_T4 (STA_1, Jarak_P, Titik_Pantau, STA_2, Jarak_I, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                                   (selected_value + '_1', jarak_pantau_1, value_pantau, selected_value + '_1', jarak_ikat_1, titik_ikat_value))
                    cursor.execute("INSERT INTO Jarak_T4 (STA_1, Jarak_P, Titik_Pantau, STA_2, Jarak_I, Titik_Ikat) VALUES (?, ?, ?, ?, ?, ?)",
                                   (selected_value + '_2', jarak_pantau_2, value_pantau, selected_value + '_2', jarak_ikat_2, titik_ikat_value))
            connection.commit()
            print("Data berhasil disimpan")
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            messagebox.showinfo("Berhasil","Informasi Berhasil Disimpan")
            connection.close()

    # Tombol
    save = Button(label_frame5, text="Simpan", command=save_data, font=("Arial", 14),bg="#FFC900")

    # Adding a Text box Entry Widget
    # Jarak dari berdiri alat ke titik pantau
    e1 = tk.DoubleVar()
    en1 = Entry(frame1_seri_1, textvariable=e1, font=("Arial", 14))
    e2 = tk.DoubleVar()
    en2 = Entry(frame1_seri_1, textvariable=e2, font=("Arial", 14))
    e3 = tk.DoubleVar()
    en3 = Entry(frame1_seri_2, textvariable=e3, font=("Arial", 14))
    e4 = tk.DoubleVar()
    en4 = Entry(frame1_seri_2, textvariable=e4, font=("Arial", 14))
    
    # Jarak dari berdiri alat ke titik ikat
    ef1 = tk.DoubleVar()
    enf1 = Entry(frame2_seri_1, textvariable=ef1, font=("Arial", 14))
    ef2 = tk.DoubleVar()
    enf2 = Entry(frame2_seri_1, textvariable=ef2, font=("Arial", 14))
    ef3 = tk.DoubleVar()
    enf3 = Entry(frame2_seri_2, textvariable=ef3, font=("Arial", 14))
    ef4 = tk.DoubleVar()
    enf4 = Entry(frame2_seri_2, textvariable=ef4, font=("Arial", 14))
    
    # Grid
    label_frame5.grid(column=0, row=1, padx=8, pady=8)
    input_frame1.grid(column=4, row=1)
    frame1_seri_1.grid(column=0, row=1)
    frame1_seri_2.grid(column=0, row=2)

    input_frame2.grid(column=4, row=3,pady=9)
    frame2_seri_1.grid(column=0, row=1)
    frame2_seri_2.grid(column=0, row=2)
    input_frame3.grid(column=3, row=1, padx=8, pady=9)

    save.grid(column=2, row=5, padx=3, pady=3)
    spasi.grid(column=5, row=1, padx=3)
    cntn.grid(column=6, row=5, padx=3, pady=3)

    # Entry Grid F1
    en1.grid(column=0, row=1, padx=3, pady=3)
    en2.grid(column=0, row=2, padx=3, pady=3)
    en3.grid(column=0, row=3, padx=3, pady=3)
    en4.grid(column=0, row=4, padx=3, pady=3)

    # Entry Grid F2
    enf1.grid(column=0, row=2, padx=3, pady=3)
    enf2.grid(column=0, row=3, padx=3, pady=3)
    enf3.grid(column=0, row=4, padx=3, pady=3)
    enf4.grid(column=0, row=5, padx=3, pady=3)

    # Combobox5
    number5 = tk.StringVar()
    number_chosen5 = ttk.Combobox(input_frame3, width=12, textvariable=number5, font=("Arial", 14))
    number_chosen5['values'] = (selected_value1.get(), selected_value2.get())
    number_chosen5.grid(column=3, row=1, padx=3, pady=3, rowspan=3)
    number_chosen5.current(0)

    # Combobox5 Ikat
    number5_ikat = tk.StringVar()
    number_chosen5_ikat = ttk.Combobox(input_frame2, width=12, textvariable=number5_ikat, font=("Arial", 14))
    number_chosen5_ikat['values'] = (selected_valuei1.get(), selected_valuei2.get())
    number_chosen5_ikat.grid(column=0, row=0, padx=3, pady=3)
    number_chosen5_ikat.current(0)

#PROSES PENGECEKAN DATA
def new_processing_window():
    # Membuat style khusus untuk tombol
    style = ttk.Style()
    style.configure('Custom.TButton', font=('Arial', 16))

    # Membuat label frame
    label_frame = ttk.Labelframe(win, text=' PEMROSESAN DATA ', padding=(30, 60), style='Custom.TLabelframe')
    label_frame.grid(column=0, row=1, padx=8, pady=8)

    # Fungsi untuk menghancurkan label_frame dan memanggil fungsi berikutnya
    def destroy_and_call(func, *args, **kwargs):
        label_frame.destroy()  # Menghancurkan label_frame
        func(*args, **kwargs)  # Memanggil fungsi atau menginisialisasi kelas dengan argumen

    # Lebar tombol seragam
    button_width = 30
    Label(label_frame,text="NOTE: Cek seluruh data mulai dari 1,2,3 dan 4",font=("Arial",12),foreground="white", background=background_color).grid(column=1, row=0)
    # GUI Elements for Database Selection and Results Processing

    Button(
        label_frame,justify="left", text="1. Cek Koordinat", font=("Arial", 14), width=button_width,
        bg="#FFC900",anchor="center", fg="black", command=lambda: destroy_and_call(DatabaseEditorKoordinat, win)
    ).grid(column=1, row=1, padx=8, pady=8)

    Button(
    label_frame,justify="left", text="2. Proses Sudut Data", font=("Arial", 14), width=button_width,
    bg="#FFC900",anchor="center", fg="black", command=lambda: destroy_and_call(new_processing_window_sudut)
    ).grid(column=1, row=2, padx=8, pady=8)

    Button(
        label_frame,justify="left", text="3. Proses Jarak Data", font=("Arial", 14), width=button_width,
        bg="#FFC900",anchor="center", fg="black", command=lambda: destroy_and_call(new_processing_window_jarak)
    ).grid(column=1, row=3, padx=8, pady=8)

    Button(
        label_frame,justify="left", text="4. Proses Simpangan Baku", font=("Arial", 14), width=button_width,
        bg="#FFC900",anchor="center", fg="black", command=lambda: destroy_and_call(new_processing_window_stdev)
    ).grid(column=1, row=4, padx=8, pady=8)

    # Back button
    def kembali_to_awal():
        label_frame.destroy()
        new_window1()

    Button(
        label_frame, text="Kembali", width=button_width, font=("Arial", 14),
        command=kembali_to_awal, bg="#FFC900", fg="black"
    ).grid(column=1, row=5, padx=8, pady=8)

def new_processing_window_sudut():

    label_frame = ttk.Labelframe(win, text=' PEMROSESAN DATA ', padding=(30, 60), style='Custom.TLabelframe')
    label_frame.grid(column=0, row=1, padx=8, pady=8)
    
    # Database selection function
    def select_database():
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            global_selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Database selected: {file_path}")

    # Restored original Sudut processing without extra details
    def calculate_and_display_paired_averages_with_tolerance(table_names, tolerance):
        """
        Menghitung dan menampilkan rata-rata pasangan sudut dari tabel dalam database dengan memeriksa toleransi deviasi.
        """
        db_path = global_selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return

        result_text_sudut.delete('1.0', tk.END)
        
        for table_name in table_names:
            result_text_sudut.insert(tk.END, f"--- Data Sudut dari Tabel: {table_name} ---\n\n")
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f"SELECT id, sudut_biasa, sudut_luar_biasa FROM {table_name} ORDER BY id ASC")
                angle_data = cursor.fetchall()
                conn.close()

                df = pd.DataFrame(angle_data, columns=["id", "sudut_biasa", "sudut_luar_biasa"])

                if df.empty:
                    result_text_sudut.insert(tk.END, f"Table '{table_name}' is empty.\n")
                    continue

                for i in range(0, len(df) - 1, 2):
                    if i + 1 >= len(df):
                        break
                    
                    avg_value = (df.loc[i, "sudut_biasa"] + df.loc[i, "sudut_luar_biasa"] + 
                                df.loc[i + 1, "sudut_biasa"] + df.loc[i + 1, "sudut_luar_biasa"]) / 4

                    deviations = [
                        abs(df.loc[i, "sudut_biasa"] - avg_value), 
                        abs(df.loc[i, "sudut_luar_biasa"] - avg_value),
                        abs(df.loc[i + 1, "sudut_biasa"] - avg_value), 
                        abs(df.loc[i + 1, "sudut_luar_biasa"] - avg_value)
                    ]

                    all_within_tolerance = all(dev <= tolerance for dev in deviations)
                    pair_label = f"Pair {df.loc[i, 'id']}-{df.loc[i + 1, 'id']}:"

                    if all_within_tolerance:
                        result_text_sudut.insert(tk.END, f"{pair_label}\n")
                        result_text_sudut.insert(tk.END, f"  Average Angle  : {avg_value:.4f} (Within Tolerance)\n\n")
                    else:
                        result_text_sudut.insert(tk.END, f"{pair_label}\n")
                        result_text_sudut.insert(tk.END, f"  Average Angle  : {avg_value:.4f} (Exceeds Tolerance)\n")

                        for idx, dev in enumerate(deviations):
                            if dev > tolerance:
                                sudut_type = "sudut_biasa" if idx % 2 == 0 else "sudut_luar_biasa"
                                row_index = i if idx < 2 else i + 1
                                result_text_sudut.insert(
                                    tk.END, 
                                    f"    {sudut_type.capitalize()} (ID {df.loc[row_index, 'id']}): {df.loc[row_index, sudut_type]:.4f}  |  Deviation: {dev:.4f}\n"
                                )

                        result_text_sudut.insert(tk.END, "\n")

            except sqlite3.Error as e:
                result_text_sudut.insert(tk.END, f"Error with table '{table_name}': {e}\n")
    lebar = 20
    # GUI Elements for Database Selection and Results Processing
    Button(
        label_frame, width=lebar, text="Select Database", command=select_database, font=("Arial", 14), bg="#FFC900"
    ).grid(column=0, row=5, padx=8, pady=8, sticky="w")

    Button(
        label_frame, width=lebar, text="Process Sudut Data", font=("Arial", 14), bg="#FFC900",
        command=lambda: calculate_and_display_paired_averages_with_tolerance(
            ["Sudut_T2", "Sudut_T4"], (0 + 0 / 60 + 5 / 3600)
        )
    ).grid(column=1, row=5, padx=8, pady=8, sticky="w")

    # Text widget for displaying results
    result_text_sudut = tk.Text(label_frame, wrap=tk.WORD, width=100, height=20)
    result_text_sudut.grid(column=0, columnspan=4, row=2, padx=10, pady=10, sticky="nsew")

    # Back button
    def kembali_to_awal():
        label_frame.destroy()
        new_processing_window()

    # Edit button
    def editedit():
        label_frame.destroy()
        DatabaseEditorSudut(win, global_selected_db_path.get())

    # Label note
    Label(
        label_frame, text="NOTE: Pilih database lalu proses sudut. Jika masih ada yang di luar toleransi, klik 'Edit Data'.",
        font=("Arial", 14), background=background_color, foreground="white", anchor="w", justify="left"
    ).grid(column=0, columnspan=4, row=0, padx=10, pady=10, sticky="w")

    # Back and Edit buttons
    Button(
        label_frame, width=lebar, text="Kembali", command=kembali_to_awal, font=("Arial", 14), bg="#FFC900"
    ).grid(column=3, row=5, padx=8, pady=8, sticky="w")

    Button(
        label_frame, width=lebar, text="Edit Data", command=editedit, font=("Arial", 14), bg="#FFC900"
    ).grid(column=2, row=5, padx=8, pady=8, sticky="w")

def new_processing_window_jarak():

    label_frame = ttk.Labelframe(win, text=' PEMROSESAN DATA ', padding=(30, 60), style='Custom.TLabelframe')
    label_frame.grid(column=0, row=1, padx=8, pady=8)
    
    # Database selection function
    def select_database():
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            global_selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Database selected: {file_path}")

    # Function to load and process Jarak data with averages and tolerance checks
    def process_jarak_data():
        """
        Fungsi untuk memproses data Jarak dari database SQLite.
        Menampilkan hasil dalam format yang mirip dengan program Sudut.
        """
        
        db_path = global_selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return

        def process_table(table_name, title):
            try:
                # Tambahkan header sebelum memproses tabel
                result_text_jarak.insert(tk.END, f"\n============ {title} ==============\n")

                # Load Jarak data dari tabel
                conn = sqlite3.connect(db_path)
                jarak_df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                conn.close()

                step_size = 4  # Ukuran langkah pengelompokan data (4 baris per kelompok)
                group_count = 1  # Penomoran kelompok

                # Memproses data dalam kelompok 4 baris
                for start_id in range(1, jarak_df['id'].max() + 1, step_size):
                    filtered_df = jarak_df[jarak_df['id'].between(start_id, start_id + step_size - 1)]

                    if filtered_df.empty or len(filtered_df) < 4:
                        continue

                    # Hitung rata-rata Jarak_P dan Jarak_I
                    avg_jarak_p = filtered_df['Jarak_P'].astype(float).mean()
                    avg_jarak_i = filtered_df['Jarak_I'].astype(float).mean()

                    # Toleransi
                    tolerance_p = avg_jarak_p / 10000
                    tolerance_i = avg_jarak_i / 10000

                    # Periksa apakah semua nilai dalam kelompok berada dalam toleransi
                    all_within_tolerance = all(
                        abs(filtered_df.iloc[i]['Jarak_P'] - avg_jarak_p) <= tolerance_p and
                        abs(filtered_df.iloc[i]['Jarak_I'] - avg_jarak_i) <= tolerance_i
                        for i in range(len(filtered_df))
                    )

                    # Format output
                    tolerance_status = "Within Tolerance" if all_within_tolerance else "Exceeds Tolerance"
                    sta_1 = (filtered_df['STA_1'].iloc[0].replace('_1', '') 
                            if not filtered_df['STA_1'].empty else "STA_1")
                    titik_ikat = (filtered_df['Titik_Ikat'].iloc[0] 
                                if not filtered_df['Titik_Ikat'].empty else "TITIK_IKAT")

                    result_text_jarak.insert(tk.END, f"Range {group_count}: ({sta_1}-{titik_ikat})\n")
                    result_text_jarak.insert(tk.END, f"  Average Distance : {avg_jarak_p:.4f} (Jarak_P), {avg_jarak_i:.4f} (Jarak_I) [{tolerance_status}]\n")

                    # Jika ada nilai di luar toleransi, tampilkan deviasi
                    if not all_within_tolerance:
                        for idx in range(len(filtered_df)):
                            jarak_p = filtered_df.iloc[idx]['Jarak_P']
                            jarak_i = filtered_df.iloc[idx]['Jarak_I']

                            if abs(jarak_p - avg_jarak_p) > tolerance_p:
                                result_text_jarak.insert(tk.END, (f"    Jarak_P (ID {filtered_df.iloc[idx]['id']}): {jarak_p:.4f} | Deviation: {abs(jarak_p - avg_jarak_p):.4f}\n"))
                            if abs(jarak_i - avg_jarak_i) > tolerance_i:
                                result_text_jarak.insert(tk.END, (f"    Jarak_I (ID {filtered_df.iloc[idx]['id']}): {jarak_i:.4f} | Deviation: {abs(jarak_i - avg_jarak_i):.4f}\n"))

                    result_text_jarak.insert(tk.END, "\n")
                    group_count += 1

            except sqlite3.Error as e:
                result_text_jarak.insert(tk.END, f"An error occurred with table {table_name}: {e}\n")

        # Proses kedua tabel Jarak_T4 dan Jarak_T2
        process_table("Jarak_T4","Jarak T4")
        process_table("Jarak_T2","Jarak T2")

    lebar = 20
    # GUI Elements for Database Selection and Results Processing
    Button(
        label_frame, text="Select Database", command=select_database, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=0, row=5, padx=8, pady=8, sticky="w")

    Button(
        label_frame, text="Process Jarak Data", command=process_jarak_data, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=1, row=5, padx=8, pady=8, sticky="w")

    # Text widget for displaying results
    result_text_jarak = tk.Text(label_frame, wrap=tk.WORD, width=100, height=20)
    result_text_jarak.grid(column=0, columnspan=4, row=2, padx=10, pady=10, sticky="nsew")

    # Back button
    def kembali_to_awal():
        label_frame.destroy()
        new_processing_window()

    # Edit button
    def editedit():
        label_frame.destroy()
        DatabaseEditorJarak(win, global_selected_db_path.get())

    # Label note
    Label(
        label_frame, text="NOTE: Pilih database lalu proses jarak. Jika ada data yang perlu diperbaiki, klik 'Edit Data'.",
        font=("Arial", 14), background="#15395b", foreground="white", anchor="w", justify="left"
    ).grid(column=0, columnspan=4, row=0, padx=10, pady=10, sticky="w")

    # Back and Edit buttons
    Button(
        label_frame, text="Kembali", command=kembali_to_awal, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=3, row=5, padx=8, pady=8, sticky="w")

    Button(
        label_frame, text="Edit Data", command=editedit, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=2, row=5, padx=8, pady=8, sticky="w")

def new_processing_window_stdev():

    label_frame = ttk.Labelframe(win, text=' PEMROSESAN DATA ', padding=(30, 60), style='Custom.TLabelframe')
    label_frame.grid(column=0, row=1, padx=8, pady=8)
    
    # Database selection function
    def select_database():
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            global_selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Database selected: {file_path}")

    #STDEV
    # Function to process stdev from various tables
    def stdev():
        db_path = global_selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return
        try:
            # Connect to the database
            conn = sqlite3.connect(db_path)

            # Define queries with proper JOINs
            queries = {
                "t2_sta1": """
                    SELECT DISTINCT 
                        pt.STA1 AS STA, 
                        pt.sta1_x AS coord_x, 
                        pt.sta1_y AS coord_y, 
                        sb.stdev_x_sta1 AS stdev_x, 
                        sb.stdev_y_sta1 AS stdev_y
                    FROM Pendefinisian_Titik_T2 pt
                    JOIN Simpangan_Baku_T2 sb ON pt.STA1 = sb.STA1
                """,
                "t2_sta2": """
                    SELECT DISTINCT 
                        pt.STA2 AS STA, 
                        pt.sta2_x AS coord_x, 
                        pt.sta2_y AS coord_y, 
                        sb.stdev_x_sta2 AS stdev_x, 
                        sb.stdev_y_sta2 AS stdev_y
                    FROM Pendefinisian_Titik_T2 pt
                    JOIN Simpangan_Baku_T2 sb ON pt.STA2 = sb.STA2
                """,
                "t4_sta1": """
                    SELECT DISTINCT 
                        pt.STA_1 AS STA, 
                        pt.sta_1_x AS coord_x, 
                        pt.sta_1_y AS coord_y, 
                        sb.stdev_1_x AS stdev_x, 
                        sb.stdev_1_y AS stdev_y
                    FROM Pendefinisian_Titik_T4 pt
                    JOIN Simpangan_Baku_T4 sb ON pt.STA_1 = sb.STA_1
                """,
                "t4_sta2": """
                    SELECT DISTINCT 
                        pt.STA_2 AS STA, 
                        pt.sta_2_x AS coord_x, 
                        pt.sta_2_y AS coord_y, 
                        sb.stdev_2_x AS stdev_x, 
                        sb.stdev_2_y AS stdev_y
                    FROM Pendefinisian_Titik_T4 pt
                    JOIN Simpangan_Baku_T4 sb ON pt.STA_2 = sb.STA_2
                """,
                "bs1": """
                    SELECT DISTINCT 
                        pt.BS_1 AS STA, 
                        pt.bs_1_x AS coord_x, 
                        pt.bs_1_y AS coord_y, 
                        sb.stdev_i1_x AS stdev_x, 
                        sb.stdev_i1_y AS stdev_y
                    FROM Pendefinisian_Titik_T4 pt
                    JOIN Simpangan_Baku_T4 sb ON pt.BS_1 = sb.BS_1
                """,
                "bs2": """
                    SELECT DISTINCT 
                        pt.BS_2 AS STA, 
                        pt.bs_2_x AS coord_x, 
                        pt.bs_2_y AS coord_y, 
                        sb.stdev_i2_x AS stdev_x, 
                        sb.stdev_i2_y AS stdev_y
                    FROM Pendefinisian_Titik_T4 pt
                    JOIN Simpangan_Baku_T4 sb ON pt.BS_2 = sb.BS_2
                """
            }

            # Execute each query and store results in a list of DataFrames
            dataframes = [pd.read_sql_query(query, conn) for query in queries.values()]

            # Combine all DataFrames and ensure unique STA entries with corresponding stdev values
            df_final_combined = pd.concat(dataframes).drop_duplicates(subset='STA').reset_index(drop=True)

            # Save the final combined DataFrame to a new table 'Simpangan_Baku_Combined'
            df_final_combined.to_sql('Simpangan_Baku', conn, if_exists='replace', index=False)

            # Close the database connection
            conn.close()

            # Display the final DataFrame in the Text widget
            result_text_stdev.delete("1.0", tk.END)  # Clear previous content
            result_text_stdev.insert("1.0", df_final_combined.to_string(index=False))  # Insert as string

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred while processing stdev: {e}")

    lebar = 20
    # GUI Elements for Database Selection and Results Processing
    Button(
        label_frame, text="Select Database", command=select_database, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=0, row=5, padx=8, pady=8, sticky="w")

    Button(
        label_frame, text="Process Stdev Data", command=stdev, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=1, row=5, padx=8, pady=8, sticky="w")

    # Text widget for displaying results
    result_text_stdev = tk.Text(label_frame, wrap=tk.WORD, width=100, height=20)
    result_text_stdev.grid(column=0, columnspan=4, row=2, padx=10, pady=10, sticky="nsew")

    # Back button
    def kembali_to_awal():
        label_frame.destroy()
        new_processing_window()

    # Edit button
    def editedit():
        label_frame.destroy()
        DatabaseEditorSimpanganBaku(win, global_selected_db_path.get())

    # Label note
    Label(
        label_frame, text="NOTE: Pilih database lalu proses simpangan baku. Jika ada data yang perlu diperbaiki, klik 'Edit Data'.",
        font=("Arial", 12), background="#15395b", foreground="white", anchor="w", justify="left"
    ).grid(column=0, columnspan=4, row=0, padx=10, pady=10, sticky="w")

    # Back and Edit buttons
    Button(
        label_frame, text="Kembali", command=kembali_to_awal, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=3, row=5, padx=8, pady=8, sticky="w")

    Button(
        label_frame, text="Edit Data", command=editedit, font=("Arial", 14), bg="#FFC900", width=lebar
    ).grid(column=2, row=5, padx=8, pady=8, sticky="w")

# Class pengeditan database
# Class Koordinat T2 dan T4
class DatabaseEditorKoordinat:
    def __init__(self, win):
        self.win = win
        # Warna background dan tombol
        background_color = "#15395b"
        button_color = "#FFC900"

        # Path database default
        self.selected_db_path = None

        # Definisi alias untuk tabel koordinat
        self.table_aliases = {
            "Tabel Koordinat T2": "Pendefinisian_Titik_T2",
            "Tabel Koordinat T4": "Pendefinisian_Titik_T4"
        }

        # Frame utama
        self.label_frame = tk.Frame(win, bg=background_color)
        self.label_frame.grid(row=1, column=0, sticky="nsew")

        # Konfigurasi grid untuk frame utama
        win.grid_rowconfigure(0, weight=0)
        win.grid_rowconfigure(1, weight=1)
        win.grid_columnconfigure(0, weight=1)

        # Canvas untuk scroll
        canvas = tk.Canvas(self.label_frame, bg=background_color, highlightthickness=0, width=1200, height=550)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars untuk canvas
        v_scrollbar = ttk.Scrollbar(self.label_frame, orient="vertical", command=canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(self.label_frame, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Frame scrollable
        self.scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Gaya untuk frame dan elemen
        style = ttk.Style()
        style.configure("Custom.TFrame", background=background_color)
        style.configure("Custom.TLabel", background=background_color, foreground="white", font=("Arial", 10, "bold"))
        style.configure("Custom.TButton", background=button_color, foreground="black", font=("Arial", 10))

        # Frame kiri untuk tombol
        left_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame kanan untuk entries dan TreeView
        right_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label frame untuk informasi
        info_frame = ttk.Labelframe(left_frame, text="INFORMASI", padding=(10, 5),style="Custom.TFrame")
        info_frame.grid(row=0,rowspan=11, column=0, padx=10, pady=10, sticky="new")
        ttk.Label(
            info_frame,
            text=(
                "NOTE:\n"
                "1. Klik 'Select Database'\n\n"
                "2. Klik 'Muat Tabel T2' untuk memuat data 2 Titik Acuan koordinat\n\n"
                "3. Klik 'Muat Tabel T4' untuk memuat data 4 Titik Acuan koordinat\n\n"
                "4. Pilih baris langsung pada data yang tertampil,lalu anda bisa\n" 
                "     memilih beberapa pilihan berikut:\n\n"
                "5. Klik 'Tambah Data', jika Anda ingin menambah data baru dalam\n"
                "     satu baris\n\n"
                "6. Klik 'Update Data', Jika Anda ingin mengganti data yang tidak\n"
                "     sesuai\n\n"
                "7. Simpan perubahan, dilakukan setelah update data\n\n"
                "8. Hapus Data, dilakukan untuk menghapus data (satu baris)"
            ),font=("Calibri", 14),
            anchor="w",
            justify="left",
            style="Custom.TLabel"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")


        # Entries untuk T2
        self.entries = {}
        columns = {
            "id": "Nomor ID",
            "Titik_Pantau": "Titik Pantau",
            "STA1": "STA 1",
            "sta1_x": "Koordinat X STA 1",
            "sta1_y": "Koordinat Y STA 1",
            "STA2": "STA 2",
            "sta2_x": "Koordinat X STA 2",
            "sta2_y": "Koordinat Y STA 2"
        }

        start_row_t2 = 1  # Baris awal untuk T2
        for i, (column, display_name) in enumerate(columns.items()):
            ttk.Label(
                right_frame, text=display_name, style="Custom.TLabel", font=("Calibri", 12)
            ).grid(row=start_row_t2 + i, column=0, pady=5, sticky="w")
            entry = ttk.Entry(right_frame)
            entry.grid(row=start_row_t2 + i, column=1, pady=5, padx=10, sticky="w")
            self.entries[column] = entry

        # Entries untuk T4
        self.entries_t4 = {}
        columns_t4 = {
            "id": "Nomor ID",
            "Titik_Pantau": "Titik Pantau",
            "STA_1": "STA 1",
            "sta_1_x": "Koordinat X STA 1",
            "sta_1_y": "Koordinat Y STA 1",
            "STA_2": "STA 2",
            "sta_2_x": "Koordinat X STA 2",
            "sta_2_y": "Koordinat Y STA 2",
            "BS_1": "Backsight 1",
            "bs_1_x": "Koordinat X BS 1",
            "bs_1_y": "Koordinat Y BS 1",
            "BS_2": "Backsight 2",
            "bs_2_x": "Koordinat X BS 2",
            "bs_2_y": "Koordinat Y BS 2"
        }

        start_row_t4 = start_row_t2 + len(columns) + 2  # Mulai setelah entri T2 dengan jarak
        for i, (column, display_name) in enumerate(columns_t4.items()):
            ttk.Label(
                right_frame, text=display_name, style="Custom.TLabel", font=("Calibri", 12)
            ).grid(row=start_row_t4 + i, column=0, pady=5, sticky="w")
            entry = ttk.Entry(right_frame)
            entry.grid(row=start_row_t4 + i, column=1, pady=5, padx=10, sticky="w")
            self.entries_t4[column] = entry

        # Tombol "Select Database"
        Button(
            left_frame, text="Select Database", command=self.select_database,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=1, column=1, pady=10)

        # Tombol operasi
        Label(left_frame, text="", background="#15395b").grid(row=0, column=1, pady=10)

        Button(
            left_frame, text="Tambah Data", command=self.add_data,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=4, column=1, pady=10)

        Button(
            left_frame, text="Update Data", command=self.update_data,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=5, column=1, pady=10)

        Button(
            left_frame, text="Simpan Perubahan", command=self.save_updated_data,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=6, column=1, pady=10)

        Button(
            left_frame, text="Hapus Data", command=self.delete_data,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=7, column=1, pady=10)

        Button(
            left_frame, text="Kembali", command=self.kembali_to_awal,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=8, column=1, pady=10)

        Button(
            left_frame, text="Muat Data T4", command=self.load_data_2,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=3, column=1, pady=10)

        Button(
            left_frame, text="Muat Data T2", command=self.load_data,
            width=20, bg="#FFC900", font=("Calibri", 12)
        ).grid(row=2, column=1, pady=10)
        
        # Pilih Tabel
        self.table_combobox = ttk.Combobox(
            left_frame,
            width=18,
            font=("Calibri", 12),
            values=list(self.table_aliases.keys()),
            state="readonly"
        )
        self.table_combobox.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.table_combobox.current(0)  # Pilihan default
        self.table_combobox.bind("<<ComboboxSelected>>", self.handle_table_selection)

        # TreeView untuk T2 dan T4
        ttk.Label(
            right_frame, text="Data Koordinat T2", style="Custom.TLabel", font=("Calibri", 12)
        ).grid(row=0, column=2, padx=10, pady=(0, 5), sticky="ew")  # Label T2 tepat di atas TreeView T2
        self.tree1 = ttk.Treeview(right_frame, show='headings')
        self.tree1.grid(row=1, column=2, rowspan=8, sticky="nsew")

        ttk.Label(
            right_frame, text="Data Koordinat T4", style="Custom.TLabel", font=("Calibri", 14)
        ).grid(row=9, column=2, padx=10, pady=(0, 5), sticky="ew")  # Label T4 tepat di atas TreeView T4
        self.tree2 = ttk.Treeview(right_frame, show='headings',height=20)
        self.tree2.grid(row=10, column=2, rowspan=50, sticky="nsew")

        # Load data ke TreeView
        self.load_data()
        self.load_data_2()

    def select_database(self):
        """
        Fungsi untuk memilih database menggunakan file dialog.
        """
        # Buka dialog untuk memilih file dengan filter hanya file SQLite (*.db)
        file_path = filedialog.askopenfilename(
            title="Pilih Database",
            filetypes=[("SQLite Database files", "*.db")],
        )

        if file_path:  # Jika pengguna memilih file
            self.selected_db_path = file_path  # Simpan path file ke atribut kelas
            messagebox.showinfo("Informasi", f"Database berhasil dipilih: {file_path}")
        else:  # Jika pengguna membatalkan pemilihan file
            messagebox.showwarning("Warning", "Anda belum memilih file database.")

    def load_data(self):
        """
        Memuat data dari tabel 'Pendefinisian_Titik_T2' ke TreeView pertama.
        """
        # Nama tabel dan kolom
        table_1_koord = "Pendefinisian_Titik_T2"
        column_1_koord = ["id", "Titik_Pantau", "STA1", "sta1_x", "sta1_y", "STA2", "sta2_x", "sta2_y"]
        column_1_koord_display = ["Nomor ID", "Titik Pantau", "STA 1", "Koordinat x STA 1", "Koordinat y STA 1", "STA 2", "Koordinat x STA 2", "Koordinat y STA 2"]

        # Validasi path database
        if not self.selected_db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            # Koneksi ke database
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Konfigurasi kolom TreeView
            self.tree1["columns"] = column_1_koord_display
            for col in column_1_koord_display:
                self.tree1.heading(col, text=col)
                self.tree1.column(col, anchor="w", stretch=tk.YES)

            # Hapus data lama dari TreeView
            self.tree1.delete(*self.tree1.get_children())

            # Query data
            column_query = ", ".join(column_1_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_1_koord}")
            rows = cursor.fetchall()

            # Masukkan data ke TreeView
            for row in rows:
                self.tree1.insert('', 'end', values=row)

            # Tutup koneksi
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")

    def load_data_2(self):
        """
        Memuat data dari tabel 'Pendefinisian_Titik_T4' ke TreeView kedua.
        """
        # Nama tabel dan kolom
        table_2_koord = "Pendefinisian_Titik_T4"
        column_2_koord = ["id", "Titik_Pantau", "STA_1", "sta_1_x", "sta_1_y", "STA_2", "sta_2_x", "sta_2_y", "BS_1", "bs_1_x", "bs_1_y", "BS_2", "bs_2_x", "bs_2_y"]
        column_2_koord_display = ["Nomor ID", "Titik Pantau", "STA 1", "Koordinat x STA 1", "Koordinat y STA 1", "STA 2", "Koordinat x STA 2", "Koordinat y STA 2", "Backsight 1", "Koordinat x BS 1", "Koordinat y BS 1", "Backsight 2", "Koordinat x BS 2", "Koordinat y BS 2"]

        # Validasi path database
        if not self.selected_db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            # Koneksi ke database
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Konfigurasi kolom TreeView
            self.tree2["columns"] = column_2_koord_display
            for col in column_2_koord_display:
                self.tree2.heading(col, text=col)
                self.tree2.column(col, anchor="w", stretch=tk.YES)

            # Hapus data lama dari TreeView
            self.tree2.delete(*self.tree2.get_children())

            # Query data
            column_query = ", ".join(column_2_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_2_koord}")
            rows = cursor.fetchall()

            # Masukkan data ke TreeView
            for row in rows:
                self.tree2.insert('', 'end', values=row)

            # Tutup koneksi
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")

    def add_data(self):
        """
        Menambahkan data baru ke tabel yang dipilih melalui combobox.
        """
        # Validasi pemilihan tabel
        if not hasattr(self, "table_combobox") or not self.table_combobox.get():
            messagebox.showwarning("Warning", "Pilih tabel terlebih dahulu.")
            return

        # Mendapatkan nama tabel dari alias combobox
        table_choice = self.table_aliases.get(self.table_combobox.get())
        if table_choice not in ["Pendefinisian_Titik_T2", "Pendefinisian_Titik_T4"]:
            messagebox.showerror("Error", "Tabel yang dipilih tidak valid.")
            return

        # Tentukan kolom dan entries berdasarkan tabel yang dipilih
        if table_choice == "Pendefinisian_Titik_T2":
            columns = ["id", "Titik_Pantau", "STA1", "sta1_x", "sta1_y", "STA2", "sta2_x", "sta2_y"]
            entries = self.entries
        elif table_choice == "Pendefinisian_Titik_T4":
            columns = ["id", "Titik_Pantau", "STA_1", "sta_1_x", "sta_1_y", "STA_2", "sta_2_x", "sta_2_y", 
                    "BS_1", "bs_1_x", "bs_1_y", "BS_2", "bs_2_x", "bs_2_y"]
            entries = self.entries_t4

        # Ambil nilai dari kolom input (entries)
        values = []
        for col in columns:
            if col in entries:  # Gunakan entries sesuai tabel yang dipilih
                value = entries[col].get().strip()
                if not value:  # Validasi input
                    messagebox.showwarning("Warning", f"Kolom '{col}' tidak boleh kosong.")
                    return
                values.append(value)

        # Masukkan data ke database
        try:
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Query untuk menambahkan data
            placeholders = ", ".join(["?" for _ in columns])
            cursor.execute(f"INSERT INTO {table_choice} ({', '.join(columns)}) VALUES ({placeholders})", values)

            conn.commit()
            conn.close()

            # Perbarui TreeView yang sesuai dengan tabel
            if table_choice == "Pendefinisian_Titik_T2":
                self.load_data()
            elif table_choice == "Pendefinisian_Titik_T4":
                self.load_data_2()

            messagebox.showinfo("Success", f"Data berhasil ditambahkan ke tabel {self.table_combobox.get()}.")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Gagal menambahkan data: ID sudah ada.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {e}")

    def handle_table_selection(self, event):
        """
        Tangani pemilihan tabel dari combobox.
        """
        table_choice = self.table_combobox.get()
        if table_choice in self.table_aliases:
            self.update_entries(self.table_aliases[table_choice])
        else:
            messagebox.showerror("Error", "Pilihan tabel tidak valid.")

    def update_entries(self, table_choice):
        """
        Perbarui kolom entri berdasarkan tabel yang dipilih.
        """
        if table_choice == "Pendefinisian_Titik_T2":
            # Aktifkan entri T2 dan nonaktifkan entri T4
            for col, entry in self.entries.items():
                entry.configure(state="normal")
            for col, entry in self.entries_t4.items():
                entry.configure(state="disabled")
        elif table_choice == "Pendefinisian_Titik_T4":
            # Aktifkan entri T4 dan nonaktifkan entri T2
            for col, entry in self.entries.items():
                entry.configure(state="disabled")
            for col, entry in self.entries_t4.items():
                entry.configure(state="normal")
        else:
            messagebox.showerror("Error", "Pilihan tabel tidak valid.")

    def update_data(self):
        """
        Mengupdate data koordinat dari baris yang dipilih di TreeView.
        """
        # Tentukan TreeView dan tabel yang dipilih
        selected_item_t2 = self.tree1.selection()
        selected_item_t4 = self.tree2.selection()

        if not selected_item_t2 and not selected_item_t4:
            messagebox.showwarning("Warning", "Pilih baris yang akan diperbarui.")
            return

        # Identifikasi TreeView dan tabel yang sesuai
        if selected_item_t2:
            tree = self.tree1
            table_name = "Pendefinisian_Titik_T2"
            selected_item = selected_item_t2[0]
            entries = self.entries  # Kolom input untuk T2
        elif selected_item_t4:
            tree = self.tree2
            table_name = "Pendefinisian_Titik_T4"
            selected_item = selected_item_t4[0]
            entries = self.entries_t4  # Kolom input untuk T4

        # Validasi apakah item masih ada
        if not tree.exists(selected_item):
            messagebox.showerror("Error", "Data yang dipilih tidak valid atau sudah dihapus.")
            return

        # Ambil nilai baris yang dipilih
        selected_values = tree.item(selected_item, "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Isi Entry dengan data yang dipilih
        for key, entry in entries.items():
            column_index = list(entries.keys()).index(key)
            entry.delete(0, tk.END)
            entry.insert(0, selected_values[column_index])

        # Tampilkan pesan untuk memastikan pengguna mengklik tombol "Simpan Perubahan"
        messagebox.showinfo("Info", "Silakan lakukan perubahan di kolom input, lalu klik 'Simpan Perubahan'.")

        # Simpan data yang akan diperbarui sebagai atribut kelas untuk digunakan di tombol "Simpan Perubahan"
        self.current_update_table = table_name
        self.current_update_item = selected_values

    def save_updated_data(self):
        """
        Menyimpan data koordinat yang telah diperbarui ke database.
        """
        if not hasattr(self, "current_update_table") or not hasattr(self, "current_update_item"):
            messagebox.showwarning("Warning", "Tidak ada data yang dipilih untuk diperbarui.")
            return

        # Tentukan kolom input yang relevan berdasarkan tabel
        entries = self.entries if self.current_update_table == "Pendefinisian_Titik_T2" else self.entries_t4

        # Ambil data dari kolom input
        data = {key: entry.get() for key, entry in entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "Semua kolom harus diisi.")
            return

        try:
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Buat klausa SET untuk query UPDATE
            set_clause = ", ".join(f"{key} = ?" for key in data.keys())
            cursor.execute(
                f"UPDATE {self.current_update_table} SET {set_clause} WHERE id = ?",
                (*data.values(), self.current_update_item[0])
            )

            conn.commit()
            conn.close()

            # Perbarui tampilan TreeView yang sesuai
            if self.current_update_table == "Pendefinisian_Titik_T2":
                self.load_data()
            elif self.current_update_table == "Pendefinisian_Titik_T4":
                self.load_data_2()

            messagebox.showinfo("Success", "Data berhasil diperbarui.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def delete_data(self):
        """
        Menghapus data yang dipilih dari TreeView dan database.
        """
        # Tentukan TreeView aktif berdasarkan pemilihan item
        if self.tree1.selection():
            tree = self.tree1
            table_name = "Pendefinisian_Titik_T2"
        elif self.tree2.selection():
            tree = self.tree2
            table_name = "Pendefinisian_Titik_T4"
        else:
            messagebox.showwarning("Warning", "Pilih baris yang akan dihapus.")
            return

        # Ambil item yang dipilih dari TreeView
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Ambil data dari baris yang dipilih
        selected_values = tree.item(selected_item[0], "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Konfirmasi penghapusan
        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus data ID {selected_values[0]} dari {table_name}?"
        )
        if not confirm:
            return

        try:
            # Hapus data dari database
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (selected_values[0],))
            conn.commit()
            conn.close()

            # Hapus item dari TreeView secara langsung
            tree.delete(selected_item[0])

            # Perbarui tampilan TreeView yang sesuai
            if table_name == "Pendefinisian_Titik_T2":
                self.load_data()
            elif table_name == "Pendefinisian_Titik_T4":
                self.load_data_2()

            messagebox.showinfo("Success", f"Data ID {selected_values[0]} berhasil dihapus dari {table_name}.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def kembali_to_awal(self):
        self.label_frame.destroy()
        new_processing_window()

# Class Sudut T2 dan T4
class DatabaseEditorSudut:
    def __init__(self, win, db_path):
        # Warna background dan tombol
        background_color = "#15395b"
        button_color = "#FFC900"

        # Validasi input db_path
        if not db_path:
            messagebox.showerror("Error", "Database path not provided.")
            return

        # Simpan db_path sebagai atribut kelas
        self.selected_db_path = db_path

        # Definisi alias untuk tabel
        self.table_aliases = {
            "Tabel Sudut T2": "Sudut_T2",
            "Tabel Sudut T4": "Sudut_T4"
        }

        # Frame utama
        self.label_frame = tk.Frame(win, bg=background_color)
        self.label_frame.grid(row=0, column=0, sticky="nsew")

        # Konfigurasi grid untuk frame utama
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)

        # Canvas untuk scroll
        canvas = tk.Canvas(self.label_frame, bg=background_color, highlightthickness=0, width=1200, height=550)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars untuk canvas
        v_scrollbar = ttk.Scrollbar(self.label_frame, orient="vertical", command=canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(self.label_frame, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Frame scrollable
        self.scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Gaya untuk frame dan elemen
        style = ttk.Style()
        style.configure("Custom.TFrame", background=background_color)
        style.configure("Custom.TLabel", background=background_color, foreground="white", font=("Arial", 10, "bold"))
        style.configure("Custom.TButton", background=button_color, foreground="black", font=("Arial", 10))

        # Frame kiri untuk tombol dan input
        left_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame kanan untuk Treeview
        right_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label judul untuk Treeview pertama
        ttk.Label(right_frame, text="Data Tabel Sudut T2", style="Custom.TLabel").grid(row=0, column=0, pady=10)

        # Treeview untuk tabel pertama
        self.tree1 = ttk.Treeview(right_frame, show='headings')
        self.tree1.grid(row=1, column=0, sticky="nsew")

        scroll1 = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=scroll1.set)
        scroll1.grid(row=1, column=1, sticky="ns")

        # Label judul untuk Treeview kedua
        ttk.Label(right_frame, text="Data Tabel Sudut T4", style="Custom.TLabel").grid(row=2, column=0, pady=10)

        # Treeview untuk tabel kedua
        self.tree2 = ttk.Treeview(right_frame, show='headings')
        self.tree2.grid(row=3, column=0, sticky="nsew")

        scroll2 = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=scroll2.set)
        scroll2.grid(row=3, column=1, sticky="ns")

        # Pilih Tabel
        ttk.Label(left_frame, text="Pilih Tabel:", style="Custom.TLabel", font=("Calibri", 12)).grid(row=0, column=0, pady=5, sticky="w")
        self.table_combobox = ttk.Combobox(
            left_frame, values=list(self.table_aliases.keys()), state="readonly"
        )
        self.table_combobox.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.table_combobox.current(0)

        # Form untuk menambahkan/mengedit data
        ttk.Label(left_frame, text="Tambah Data:", style="Custom.TLabel", font=("Calibri", 12)).grid(row=1, column=0, columnspan=2, pady=5)

        self.entries = {}
        columns = {
            "id": "Nomor ID",
            "STA_1": "STA",
            "sudut_biasa": "Sudut Biasa",
            "sudut_luar_biasa": "Sudut Luar Biasa",
            "Titik_Ikat": "Backsight",
            "Titik_Pantau": "Titik Pantau"
        }

        for i, (column, display_name) in enumerate(columns.items()):
            ttk.Label(left_frame, text=display_name, style="Custom.TLabel",font=("Calibri", 14)).grid(row=i + 2, column=0, pady=5, sticky="w")
            entry = ttk.Entry(left_frame)
            entry.grid(row=i + 2, column=1, pady=5, padx=5, sticky="w")
            self.entries[column] = entry

        # Tombol untuk operasi
        button_width = 15  # Lebar tombol
        Button(left_frame, text="Tambah Data", command=self.add_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 3, column=0, pady=5)
        Button(left_frame, text="Update Data", command=self.update_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 4, column=0, pady=5)
        Button(left_frame, text="Hapus Data", command=self.delete_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 5, column=0, pady=5)
        Button(left_frame, text="Kembali", command=self.kembali_to_awal, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 6, column=0, pady=5)

        # Tombol "Simpan Perubahan" di samping tombol "Update Data"
        self.save_button = Button(left_frame, text="Simpan Update", command=self.save_updated_data, font=("Calibri", 12), width=12, padx=3)
        self.save_button.grid(row=10, column=1, pady=5)

        # Load data ke Treeview
        self.load_data()
        self.load_data_2()

    def load_data(self):
        # Tabel pertama
        table_1_koord = "Sudut_T2"
        column_1_koord = ["id", "STA_1", "sudut_biasa", "sudut_luar_biasa", "Titik_Ikat","Titik_Pantau"]
        column_1_koord_display = ["Nomor ID", "STA", "Sudut Biasa", "Sudut Luar Biasa", "Backsight", "Titik Pantau"]

        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            self.tree1["columns"] = column_1_koord_display
            for col in column_1_koord_display:
                self.tree1.heading(col, text=col)
                self.tree1.column(col, anchor="w", stretch=tk.YES)

            self.tree1.delete(*self.tree1.get_children())


            column_query = ", ".join(column_1_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_1_koord}")
            rows = cursor.fetchall()
            for row in rows:
                self.tree1.insert('', 'end', values=row)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def load_data_2(self):
        # Tabel kedua
        table_2_koord = "Sudut_T4"
        column_2_koord = ["id", "STA_1", "sudut_biasa", "sudut_luar_biasa", "Titik_Ikat","Titik_Pantau"]
        column_2_koord_display = ["Nomor ID", "STA", "Sudut Biasa", "Sudut Luar Biasa", "Backsight", "Titik Pantau"]

        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            self.tree2["columns"] = column_2_koord_display
            for col in column_2_koord_display:
                self.tree2.heading(col, text=col)
                self.tree2.column(col, anchor="w", stretch=tk.YES)

            self.tree2.delete(*self.tree2.get_children())

            column_query = ", ".join(column_2_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_2_koord}")
            rows = cursor.fetchall()
            for row in rows:
                self.tree2.insert('', 'end', values=row)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def add_data(self):
        # Periksa apakah tabel sudah dipilih
        if not hasattr(self, "table_combobox") or not self.table_combobox.get():
            messagebox.showwarning("Warning", "Pilih tabel terlebih dahulu.")
            return

        # Mendapatkan nama tabel dari alias
        table_name = self.table_aliases[self.table_combobox.get()]

        # Ambil data dari entry
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "Semua kolom harus diisi.")
            return

        try:
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Tambahkan data ke tabel yang dipilih
            columns = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data.values())
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", tuple(data.values()))

            conn.commit()
            conn.close()

            # Perbarui tampilan tabel yang sesuai
            if table_name == "Sudut_T2":
                self.load_data()
            elif table_name == "Sudut_T4":
                self.load_data_2()

            messagebox.showinfo("Success", "Data berhasil ditambahkan.")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"Gagal menambahkan data: ID sudah ada di {table_name}.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {e}")

    def update_data(self):
        # Tentukan TreeView dan tabel yang dipilih
        selected_item_t2 = self.tree1.selection()
        selected_item_t4 = self.tree2.selection()

        if not selected_item_t2 and not selected_item_t4:
            messagebox.showwarning("Warning", "Pilih baris yang akan diperbarui.")
            return

        # Identifikasi TreeView dan tabel yang sesuai
        if selected_item_t2:
            tree = self.tree1
            table_name = "Sudut_T2"
            selected_item = selected_item_t2[0]
        elif selected_item_t4:
            tree = self.tree2
            table_name = "Sudut_T4"
            selected_item = selected_item_t4[0]

        # Validasi apakah item masih ada
        if not tree.exists(selected_item):
            messagebox.showerror("Error", "Data yang dipilih tidak valid atau sudah dihapus.")
            return

        # Ambil nilai baris yang dipilih
        selected_values = tree.item(selected_item, "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Isi Entry dengan data yang dipilih
        for key, entry in self.entries.items():
            column_index = list(self.entries.keys()).index(key)
            entry.delete(0, tk.END)
            entry.insert(0, selected_values[column_index])

        # Tampilkan pesan untuk memastikan pengguna mengklik tombol "Simpan Perubahan"
        messagebox.showinfo("Info", "Silakan lakukan perubahan di kolom input, lalu klik 'Simpan Perubahan'.")

        # Simpan data yang akan diperbarui sebagai atribut kelas untuk digunakan di tombol "Simpan Perubahan"
        self.current_update_table = table_name
        self.current_update_item = selected_values

    def save_updated_data(self):
        if not hasattr(self, "current_update_table") or not hasattr(self, "current_update_item"):
            messagebox.showwarning("Warning", "Tidak ada data yang dipilih untuk diperbarui.")
            return

        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "Semua kolom harus diisi.")
            return

        try:
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            set_clause = ", ".join(f"{key} = ?" for key in data.keys())
            cursor.execute(
                f"UPDATE {self.current_update_table} SET {set_clause} WHERE id = ?",
                (*data.values(), self.current_update_item[0])
            )

            conn.commit()
            conn.close()

            # Perbarui tampilan TreeView yang sesuai
            if self.current_update_table == "Sudut_T2":
                self.load_data()
            elif self.current_update_table == "Sudut_T4":
                self.load_data_2()

            messagebox.showinfo("Success", "Data berhasil diperbarui.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def delete_data(self):
        # Tentukan TreeView aktif berdasarkan pemilihan item
        if self.tree1.selection():
            tree = self.tree1
            table_name = "Sudut_T2"
        elif self.tree2.selection():
            tree = self.tree2
            table_name = "Sudut_T4"
        else:
            messagebox.showwarning("Warning", "Pilih baris yang akan dihapus.")
            return

        # Ambil item yang dipilih dari TreeView
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Ambil data dari baris yang dipilih
        selected_values = tree.item(selected_item[0], "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Konfirmasi penghapusan
        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus data ID {selected_values[0]} dari {table_name}?"
        )
        if not confirm:
            return

        try:
            # Hapus data dari database
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (selected_values[0],))
            conn.commit()
            conn.close()

            # Hapus item dari TreeView secara langsung
            tree.delete(selected_item[0])

            messagebox.showinfo("Success", f"Data ID {selected_values[0]} berhasil dihapus dari {table_name}.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def kembali_to_awal(self):
        self.label_frame.destroy()
        new_processing_window()

# Class Jarak T2 dan T4
class DatabaseEditorJarak:
    def __init__(self, win, db_path):
        # Warna background dan tombol
        background_color = "#15395b"
        button_color = "#FFC900"

        # Validasi input db_path
        if not db_path:
            messagebox.showerror("Error", "Database path not provided.")
            return

        # Simpan db_path sebagai atribut kelas
        self.selected_db_path = db_path

        # Definisi alias untuk tabel
        self.table_aliases = {
            "Tabel Jarak T2": "Jarak_T2",
            "Tabel Jarak T4": "Jarak_T4"
        }

        # Frame utama
        self.label_frame = tk.Frame(win, bg=background_color)
        self.label_frame.grid(row=0, column=0, sticky="nsew")

        # Konfigurasi grid untuk frame utama
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)

        # Canvas untuk scroll
        canvas = tk.Canvas(self.label_frame, bg=background_color, highlightthickness=0, width=1200, height=550)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars untuk canvas
        v_scrollbar = ttk.Scrollbar(self.label_frame, orient="vertical", command=canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(self.label_frame, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Frame scrollable
        self.scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Gaya untuk frame dan elemen
        style = ttk.Style()
        style.configure("Custom.TFrame", background=background_color)
        style.configure("Custom.TLabel", background=background_color, foreground="white", font=("Arial", 10, "bold"))
        style.configure("Custom.TButton", background=button_color, foreground="black", font=("Arial", 10))

        # Frame kiri untuk tombol dan input
        left_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame kanan untuk Treeview
        right_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label judul untuk Treeview pertama
        ttk.Label(right_frame, text="Data Tabel Jarak T2", style="Custom.TLabel").grid(row=0, column=0, pady=10)

        # Treeview untuk tabel pertama
        self.tree1 = ttk.Treeview(right_frame, show='headings')
        self.tree1.grid(row=1, column=0, sticky="nsew")

        scroll1 = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=scroll1.set)
        scroll1.grid(row=1, column=1, sticky="ns")

        # Label judul untuk Treeview kedua
        ttk.Label(right_frame, text="Data Tabel Jarak T4", style="Custom.TLabel").grid(row=2, column=0, pady=10)

        # Treeview untuk tabel kedua
        self.tree2 = ttk.Treeview(right_frame, show='headings')
        self.tree2.grid(row=3, column=0, sticky="nsew")

        scroll2 = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=scroll2.set)
        scroll2.grid(row=3, column=1, sticky="ns")

        # Pilih Tabel
        ttk.Label(left_frame, text="Pilih Tabel:", style="Custom.TLabel", font=("Calibri", 12)).grid(row=0, column=0, pady=5, sticky="w")
        self.table_combobox = ttk.Combobox(
            left_frame, values=list(self.table_aliases.keys()), state="readonly"
        )
        self.table_combobox.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.table_combobox.current(0)

        # Form untuk menambahkan/mengedit data
        ttk.Label(left_frame, text="Tambah Data:", style="Custom.TLabel", font=("Calibri", 12)).grid(row=1, column=0, columnspan=2, pady=5)

        self.entries = {}
        columns = {
            "id": "Nomor ID",
            "STA_1": "STA",
            "Jarak_P": "Jarak STA-Pantau",
            "Titik_Pantau": "Titik Pantau",
            "STA_2": "STA",
            "Jarak_I": "Jarak STA-BS",
            "Titik_Ikat": "Backsight"
            
        }

        for i, (column, display_name) in enumerate(columns.items()):
            ttk.Label(left_frame, text=display_name, style="Custom.TLabel", font=("Calibri", 14)).grid(row=i + 2, column=0, pady=5, sticky="w")
            entry = ttk.Entry(left_frame)
            entry.grid(row=i + 2, column=1, pady=5, padx=5, sticky="w")
            self.entries[column] = entry

        # Tombol untuk operasi
        button_width = 15  # Lebar tombol
        Button(left_frame, text="Tambah Data", command=self.add_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 3, column=0, pady=5)
        Button(left_frame, text="Update Data", command=self.update_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 4, column=0, pady=5)
        Button(left_frame, text="Hapus Data", command=self.delete_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 5, column=0, pady=5)
        Button(left_frame, text="Kembali", command=self.kembali_to_awal, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 6, column=0, pady=5)

        # Tombol "Simpan Perubahan" di samping tombol "Update Data"
        self.save_button = Button(left_frame, text="Simpan Update", command=self.save_updated_data, font=("Calibri", 12), width=12, padx=3)
        self.save_button.grid(row=11, column=1, pady=5)

        # Load data ke Treeview
        self.load_data()
        self.load_data_2()

    def load_data(self):
        """
        Load data untuk tabel Jarak_T2.
        """
        table_1_koord = "Jarak_T2"
        column_1_koord = ["id", "STA_1", "Jarak_P", "Titik_Pantau", "STA_2", "Jarak_I", "Titik_Ikat"]
        column_1_koord_display = ["Nomor ID", "STA", "Jarak dari STA-Pantau", "Titik Pantau", "STA", "Jarak dari STA-Backsight", "Backsight"]

        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Set header TreeView
            self.tree1["columns"] = column_1_koord_display
            for col in column_1_koord_display:
                self.tree1.heading(col, text=col)
                self.tree1.column(col, anchor="w", stretch=tk.YES)

            # Hapus data sebelumnya
            self.tree1.delete(*self.tree1.get_children())

            # Query data dari database
            column_query = ", ".join(column_1_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_1_koord}")
            rows = cursor.fetchall()

            # Masukkan data ke TreeView
            for row in rows:
                self.tree1.insert('', 'end', values=row)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")

    def load_data_2(self):
        """
        Load data untuk tabel Jarak_T4.
        """
        table_2_koord = "Jarak_T4"
        column_2_koord = ["id", "STA_1", "Jarak_P", "Titik_Pantau", "STA_2", "Jarak_I", "Titik_Ikat"]
        column_2_koord_display = ["Nomor ID", "STA", "Jarak dari STA-Pantau", "Titik Pantau", "STA", "Jarak dari STA-Backsight", "Backsight"]

        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Set header TreeView
            self.tree2["columns"] = column_2_koord_display
            for col in column_2_koord_display:
                self.tree2.heading(col, text=col)
                self.tree2.column(col, anchor="w", stretch=tk.YES)

            # Hapus data sebelumnya
            self.tree2.delete(*self.tree2.get_children())

            # Query data dari database
            column_query = ", ".join(column_2_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_2_koord}")
            rows = cursor.fetchall()

            # Masukkan data ke TreeView
            for row in rows:
                self.tree2.insert('', 'end', values=row)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")

    def add_data(self):
        """
        Menambahkan data ke tabel Jarak_T2 atau Jarak_T4 berdasarkan pilihan.
        """
        # Periksa apakah database telah dipilih
        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        # Tampilkan dialog untuk memilih tabel
        table_choice = self.table_combobox.get()
        if table_choice not in self.table_aliases:
            messagebox.showerror("Error", "Pilih tabel yang valid.")
            return

        # Mendapatkan nama tabel dari alias
        table_name = self.table_aliases[table_choice]

        # Ambil data dari entry
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):  # Pastikan semua kolom diisi
            messagebox.showwarning("Warning", "Semua kolom harus diisi.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Tambahkan data ke tabel yang dipilih
            columns = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data.values())
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", tuple(data.values()))

            conn.commit()
            conn.close()

            # Perbarui tampilan tabel yang sesuai
            if table_name == "Jarak_T2":
                self.load_data()
            elif table_name == "Jarak_T4":
                self.load_data_2()

            messagebox.showinfo("Success", "Data berhasil ditambahkan.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"Gagal menambahkan data: ID sudah ada di {table_name}.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {e}")

    def update_data(self):
        """
        Memulai proses pembaruan data dengan menampilkan data yang dipilih ke kolom input.
        """
        # Tentukan TreeView dan tabel yang dipilih
        selected_item_t2 = self.tree1.selection()
        selected_item_t4 = self.tree2.selection()

        if not selected_item_t2 and not selected_item_t4:
            messagebox.showwarning("Warning", "Pilih baris yang akan diperbarui.")
            return

        # Identifikasi TreeView dan tabel yang sesuai
        if selected_item_t2:
            tree = self.tree1
            table_name = "Jarak_T2"
            selected_item = selected_item_t2[0]
        elif selected_item_t4:
            tree = self.tree2
            table_name = "Jarak_T4"
            selected_item = selected_item_t4[0]

        # Validasi apakah item masih ada
        if not tree.exists(selected_item):
            messagebox.showerror("Error", "Data yang dipilih tidak valid atau sudah dihapus.")
            return

        # Ambil nilai baris yang dipilih
        selected_values = tree.item(selected_item, "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Isi Entry dengan data yang dipilih
        for key, entry in self.entries.items():
            column_index = list(self.entries.keys()).index(key)
            entry.delete(0, tk.END)
            entry.insert(0, selected_values[column_index])

        # Tampilkan pesan untuk memastikan pengguna mengklik tombol "Simpan Perubahan"
        messagebox.showinfo("Info", "Silakan lakukan perubahan di kolom input, lalu klik 'Simpan Perubahan'.")

        # Simpan data yang akan diperbarui sebagai atribut kelas untuk digunakan di tombol "Simpan Perubahan"
        self.current_update_table = table_name
        self.current_update_item = selected_values

    def save_updated_data(self):
        """
        Menyimpan perubahan data yang telah diperbarui ke dalam database.
        """
        if not hasattr(self, "current_update_table") or not hasattr(self, "current_update_item"):
            messagebox.showwarning("Warning", "Tidak ada data yang dipilih untuk diperbarui.")
            return

        # Ambil data dari Entry
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):  # Validasi apakah semua kolom telah diisi
            messagebox.showwarning("Warning", "Semua kolom harus diisi.")
            return

        try:
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Perbarui data di tabel yang sesuai
            set_clause = ", ".join(f"{key} = ?" for key in data.keys())
            cursor.execute(
                f"UPDATE {self.current_update_table} SET {set_clause} WHERE id = ?",
                (*data.values(), self.current_update_item[0])
            )

            conn.commit()
            conn.close()

            # Perbarui tampilan TreeView yang sesuai
            if self.current_update_table == "Jarak_T2":
                self.load_data()
            elif self.current_update_table == "Jarak_T4":
                self.load_data_2()

            messagebox.showinfo("Success", "Data berhasil diperbarui.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def delete_data(self):
        """
        Menghapus data yang dipilih dari database dan TreeView.
        """
        # Tentukan TreeView aktif berdasarkan pemilihan item
        if self.tree1.selection():
            tree = self.tree1
            table_name = "Jarak_T2"
        elif self.tree2.selection():
            tree = self.tree2
            table_name = "Jarak_T4"
        else:
            messagebox.showwarning("Warning", "Pilih baris yang akan dihapus.")
            return

        # Ambil item yang dipilih dari TreeView
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Ambil data dari baris yang dipilih
        selected_values = tree.item(selected_item[0], "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Konfirmasi penghapusan
        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus data ID {selected_values[0]} dari {table_name}?"
        )
        if not confirm:
            return

        try:
            # Hapus data dari database
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (selected_values[0],))
            conn.commit()
            conn.close()

            # Hapus item dari TreeView secara langsung
            tree.delete(selected_item[0])

            messagebox.showinfo("Success", f"Data ID {selected_values[0]} berhasil dihapus dari {table_name}.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def kembali_to_awal(self):
        self.label_frame.destroy()
        new_processing_window()

# Class Simpangan Baku
class DatabaseEditorSimpanganBaku:
    def __init__(self, win, db_path):
        # Warna background dan tombol
        background_color = "#15395b"
        button_color = "#FFC900"

        # Validasi input db_path
        if not db_path:
            messagebox.showerror("Error", "Database path not provided.")
            return

        # Simpan db_path sebagai atribut kelas
        self.selected_db_path = db_path

        # Frame utama
        self.label_frame = tk.Frame(win, bg=background_color)
        self.label_frame.grid(row=0, column=0, sticky="nsew")

        # Konfigurasi grid untuk frame utama
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)

        # Canvas untuk scroll
        canvas = tk.Canvas(self.label_frame, bg=background_color, highlightthickness=0, width=1200, height=450)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars untuk canvas
        v_scrollbar = ttk.Scrollbar(self.label_frame, orient="vertical", command=canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = ttk.Scrollbar(self.label_frame, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Frame scrollable
        self.scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Gaya untuk frame dan elemen
        style = ttk.Style()
        style.configure("Custom.TFrame", background=background_color)
        style.configure("Custom.TLabel", background=background_color, foreground="white", font=("Arial", 10, "bold"))
        style.configure("Custom.TButton", background=button_color, foreground="black", font=("Arial", 10))

        # Frame kiri untuk tombol dan input
        left_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame kanan untuk TreeView
        right_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label judul untuk TreeView
        ttk.Label(right_frame, text="Data Tabel Simpangan Baku", style="Custom.TLabel").grid(row=0, column=0, pady=10)

        # TreeView untuk tabel
        self.tree1 = ttk.Treeview(right_frame, show='headings')
        self.tree1.grid(row=1, column=0, sticky="nsew")

        scroll1 = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=scroll1.set)
        scroll1.grid(row=1, column=1, sticky="ns")

        # Form untuk menambahkan/mengedit data
        ttk.Label(left_frame, text="Tambah/Edit Data:", style="Custom.TLabel", font=("Calibri", 12)).grid(row=0, column=0, columnspan=2, pady=5)

        self.entries = {}
        columns = {
            "STA": "STA",
            "coord_x": "Koordinat X STA",
            "coord_y": "Koordinat Y STA",
            "stdev_x": "STDEV X",
            "stdev_y": "STDEV Y",
        }

        for i, (column, display_name) in enumerate(columns.items()):
            ttk.Label(left_frame, text=display_name, style="Custom.TLabel", font=("Calibri", 14)).grid(row=i + 1, column=0, pady=5, sticky="w")
            entry = ttk.Entry(left_frame)
            entry.grid(row=i + 1, column=1, pady=5, padx=5, sticky="w")
            self.entries[column] = entry

        # Tombol untuk operasi
        button_width = 15
        Button(left_frame, text="Tambah Data", command=self.add_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 2, column=0, pady=5)
        Button(left_frame, text="Update Data", command=self.update_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 3, column=0, pady=5)
        Button(left_frame, text="Hapus Data", command=self.delete_data, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 4, column=0, pady=5)
        Button(left_frame, text="Kembali", command=self.kembali_to_awal, width=button_width, bg=button_color, font=("Calibri", 14)).grid(row=len(columns) + 5, column=0, pady=5)

        # Tombol "Simpan Update" untuk menyimpan perubahan
        self.save_button = Button(left_frame, text="Simpan Update", command=self.save_updated_data, font=("Calibri", 12), width=12, padx=3)
        self.save_button.grid(row=len(columns) + 3, column=1, pady=5)

        # Load data ke TreeView
        self.load_data()

    def load_data(self):
        # Tabel untuk simpangan baku
        table_koord = "Simpangan_Baku"
        column_koord = ["STA", "coord_x", "coord_y", "stdev_x", "stdev_y"]
        column_koord_display = ["STA", "Koordinat X STA", "Koordinat Y STA", "STDEV X", "STDEV Y"]

        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            self.tree1["columns"] = column_koord_display
            for col in column_koord_display:
                self.tree1.heading(col, text=col)
                self.tree1.column(col, anchor="w", stretch=tk.YES)

            self.tree1.delete(*self.tree1.get_children())

            column_query = ", ".join(column_koord)
            cursor.execute(f"SELECT {column_query} FROM {table_koord}")
            rows = cursor.fetchall()
            for row in rows:
                self.tree1.insert('', 'end', values=row)

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def add_data(self):
        """
        Menambahkan data baru ke tabel 'Simpangan_Baku' menggunakan kolom entry yang disediakan.
        """
        # Validasi path database
        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        # Kolom tabel Simpangan_Baku
        columns = ["STA", "coord_x", "coord_y", "stdev_x", "stdev_y"]
        values = []

        # Ambil data dari entry yang sesuai
        for col in columns:
            value = self.entries[col].get().strip()
            if not value:  # Validasi input
                messagebox.showwarning("Warning", f"Kolom '{col}' tidak boleh kosong.")
                return
            values.append(value)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Query untuk menambahkan data
            placeholders = ", ".join(["?" for _ in columns])
            cursor.execute(
                f"INSERT INTO Simpangan_Baku ({', '.join(columns)}) VALUES ({placeholders})",
                values,
            )

            conn.commit()
            conn.close()

            # Memuat ulang data ke TreeView
            self.load_data()

            messagebox.showinfo("Success", "Data berhasil ditambahkan ke tabel Simpangan_Baku.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Gagal menambahkan data: ID atau STA mungkin sudah ada.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {e}")

    def update_data(self):
        # Memastikan ada baris yang dipilih di TreeView
        selected_item = self.tree1.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Pilih baris yang akan diperbarui.")
            return

        # Ambil data dari baris yang dipilih
        selected_item = selected_item[0]
        selected_values = self.tree1.item(selected_item, "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Isi form entri dengan data dari baris yang dipilih
        for i, key in enumerate(self.entries.keys()):
            entry = self.entries[key]
            entry.delete(0, tk.END)
            entry.insert(0, selected_values[i])

        # Tampilkan pesan untuk memastikan pengguna mengklik tombol "Simpan Perubahan"
        messagebox.showinfo("Info", "Silakan ubah data di form entri, lalu klik tombol 'Simpan Update' untuk menyimpan perubahan.")

        # Simpan data baris yang sedang diedit sebagai atribut kelas untuk digunakan di save_updated_data
        self.current_update_item = selected_values

    def save_updated_data(self):
        if not hasattr(self, "current_update_item"):
            messagebox.showwarning("Warning", "Tidak ada data yang dipilih untuk diperbarui.")
            return

        # Ambil data dari form entri
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Warning", "Semua kolom harus diisi.")
            return

        try:
            conn = sqlite3.connect(self.selected_db_path)
            cursor = conn.cursor()

            # Update data di database
            set_clause = ", ".join(f"{key} = ?" for key in data.keys())
            sta_value = self.current_update_item[0]  # STA di kolom pertama
            cursor.execute(f"UPDATE Simpangan_Baku SET {set_clause} WHERE STA = ?", (*data.values(), sta_value))

            conn.commit()
            conn.close()

            # Hapus atribut setelah update
            del self.current_update_item

            # Perbarui tampilan TreeView
            self.load_data()

            messagebox.showinfo("Success", "Perubahan berhasil disimpan.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menyimpan perubahan: {e}")

    def delete_data(self):
        # Memastikan ada baris yang dipilih di TreeView
        selected_item = self.tree1.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Pilih baris yang akan dihapus.")
            return

        db_path = self.selected_db_path
        if not db_path:
            messagebox.showwarning("Warning", "Database belum dipilih.")
            return

        # Ambil data dari baris yang dipilih
        selected_item = selected_item[0]
        selected_values = self.tree1.item(selected_item, "values")
        if not selected_values:
            messagebox.showerror("Error", "Gagal mendapatkan data yang dipilih.")
            return

        # Konfirmasi penghapusan
        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus data STA {selected_values[0]} dari tabel Simpangan_Baku?"
        )
        if not confirm:
            return

        try:
            # Hapus data dari database berdasarkan kolom STA
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Simpangan_Baku WHERE STA = ?", (selected_values[0],))
            conn.commit()
            conn.close()

            # Hapus item dari TreeView secara langsung
            self.tree1.delete(selected_item)

            messagebox.showinfo("Success", f"Data STA {selected_values[0]} berhasil dihapus dari tabel Simpangan_Baku.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def kembali_to_awal(self):
        self.label_frame.destroy()
        new_processing_window()

class Pengolahan_matang:
    def __init__(self, win):
        # Main label frame
        self.label_frame = ttk.Labelframe(win, text=' PENGOLAHAN DATA ', padding=(30, 60), style='Custom.TLabelframe')
        self.label_frame.grid(row=0, column=0, padx=10, pady=10)

        # Variables for storing database paths
        self.selected_db_path = tk.StringVar()  # Source database path
        self.save_db_path = tk.StringVar()      # Destination database path

        # Create UI elements
        self.create_widgets(self.label_frame)

    def create_widgets(self, label_frame):
        # Lebar tombol seragam
        button_width = 15
        Label(label_frame, text=" NOTE: Klik Nomor 1,2,3,4,5, dan 6 secara berurutan.",background=background_color, foreground="white", font=("Calibri",18,"bold")).grid(column=0,row=0,columnspan=4,sticky="w")

        # Select source database button
        select_button = Button(label_frame,text="1. Pilih Database",command=self.select_database,bg="#FFC900",font=("Calibri", 14),width=button_width)
        select_button.grid(row=3, column=0, padx=3, pady=10)

        # Save destination database button (triggers migration after save)
        save_button = Button(label_frame,text="2. Save As",command=self.save_database_as,bg="#FFC900",font=("Calibri", 14),width=button_width)
        save_button.grid(row=4, column=0, padx=3, pady=10)

        # Process Sudut button
        sudut_button = Button(label_frame,text="3. Proses Sudut T2",command=self.proses_sudut,bg="#FFC900",font=("Calibri", 14),width=button_width)
        sudut_button.grid(row=3, column=1, padx=3, pady=10)

        # Process Sudut T4 button
        sudut_t4_button = Button(label_frame,text="4. Proses Sudut T4",command=self.proses_sudut_t4,bg="#FFC900",font=("Calibri", 14),width=button_width)
        sudut_t4_button.grid(row=4, column=1, padx=3, pady=10)

        # Process Jarak button
        jarak_button = Button(label_frame,text="5. Proses Jarak T2",command=self.proses_jarak,bg="#FFC900",font=("Calibri", 14),width=button_width)
        jarak_button.grid(row=3, column=2, padx=3, pady=10)

        # Process Jarak T4 button
        jarak_t4_button = Button(label_frame,text="6. Proses Jarak T4",command=self.proses_jarak_T4,bg="#FFC900",font=("Calibri", 14),width=button_width)
        jarak_t4_button.grid(row=4, column=2, padx=3, pady=10)

        # Back button
        back_button = Button(label_frame,text="Kembali",command=self.kembali_to_awal,bg="#FFC900",font=("Calibri", 14),width=button_width)
        back_button.grid(row=4, column=3, padx=3, pady=10)

        # Display area
        self.result_text = tk.Text(label_frame, wrap=tk.WORD, width=150, height=20)
        self.result_text.grid(row=2, column=0, columnspan=4, padx=8, pady=8)

    def select_database(self):
        # Select source database
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            self.selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Source database selected: {file_path}")

    def save_database_as(self):
        # Select destination database and trigger migration
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            self.save_db_path.set(file_path)
            messagebox.showinfo("Information", f"Destination database set to: {file_path}")
            self.migrate_tables()  # Trigger migration after Save As

    def migrate_tables(self):
        # Migrate tables from source to destination database
        try:
            source_db_path = self.selected_db_path.get()
            destination_db_path = self.save_db_path.get()

            if not source_db_path or not destination_db_path:
                messagebox.showwarning("Warning", "Please select both source and destination databases.")
                return

            # Connect to source database and retrieve tables
            conn_src = sqlite3.connect(source_db_path)
            pendefinisian_titik_df = pd.read_sql_query("SELECT * FROM Pendefinisian_Titik_T2", conn_src)
            pendefinisian_titik_t4_df = pd.read_sql_query("SELECT * FROM Pendefinisian_Titik_T4", conn_src)
            Simpangan_Baku_df = pd.read_sql_query("SELECT * FROM Simpangan_Baku", conn_src)
            conn_src.close()

            # Connect to destination database and save tables
            conn_dest = sqlite3.connect(destination_db_path)
            pendefinisian_titik_df.to_sql("Pendefinisian_Titik_T2", conn_dest, if_exists='replace', index=False)
            pendefinisian_titik_t4_df.to_sql("Pendefinisian_Titik_T4", conn_dest, if_exists='replace', index=False)
            Simpangan_Baku_df.to_sql("Simpangan_Baku", conn_dest, if_exists='replace', index=False)
            conn_dest.close()

            messagebox.showinfo("Success", "Tables 'Pendefinisian_Titik_2', 'Pendefinisian_Titik_T4' and 'Simpangan Baku' migrated successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during migration: {e}")

    def calculate_jarak_averages(self, df, step_size=4):
        # Calculate averages of Jarak_P and Jarak_I
        results = []
        for start_id in range(1, df['id'].max() + 1, step_size):
            filtered_df = df[df['id'].between(start_id, start_id + step_size - 1)]
            avg_jarak_p = filtered_df['Jarak_P'].astype(float).mean()
            avg_jarak_i = filtered_df['Jarak_I'].astype(float).mean()

            # Metadata extraction
            sta_1 = filtered_df['STA_1'].iloc[0].replace('_1', '') if not filtered_df['STA_1'].empty else None
            titik_pantau = filtered_df['Titik_Pantau'].iloc[0] if not filtered_df['Titik_Pantau'].empty else None
            sta_2 = filtered_df['STA_2'].iloc[0].replace('_1', '') if not filtered_df['STA_2'].empty else None
            titik_ikat = filtered_df['Titik_Ikat'].iloc[0] if not filtered_df['Titik_Ikat'].empty else None

            results.append({
                "ID_Range": f"{start_id}-{start_id + step_size - 1}",
                "STA_1": sta_1,
                "Jarak_P": avg_jarak_p,
                "Titik_Pantau": titik_pantau,
                "STA_2": sta_2,
                "Jarak_I": avg_jarak_i,
                "Titik_Ikat": titik_ikat
            })
        return pd.DataFrame(results)

    def proses_jarak(self):
        db_path = self.selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return

        # Load and process Jarak table
        conn = sqlite3.connect(db_path)
        try:
            jarak_df = pd.read_sql_query("SELECT * FROM Jarak_T2", conn)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return
        finally:
            conn.close()

        jarak_averages_df = self.calculate_jarak_averages(jarak_df)
        self.save_to_database(jarak_averages_df, "Jarak_Fine_T2")
        self.result_text.insert(tk.END, "Jarak T2 Averages :\n")
        self.result_text.insert(tk.END, jarak_averages_df.to_string(index=False) + "\n\n")

    def proses_jarak_T4(self):
        db_path = self.selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return

        # Load and process Jarak table
        conn = sqlite3.connect(db_path)
        try:
            jarak_t4_df = pd.read_sql_query("SELECT * FROM Jarak_T4", conn)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return
        finally:
            conn.close()

        jarak_t4_averages_df = self.calculate_jarak_averages(jarak_t4_df)
        self.save_to_database(jarak_t4_averages_df, "Jarak_Fine_T4")
        self.result_text.insert(tk.END, "Jarak T2 Averages :\n")
        self.result_text.insert(tk.END, jarak_t4_averages_df.to_string(index=False) + "\n\n")

    def calculate_sudut_averages(self, df):
        # Calculate combined average for each consecutive pair in Sudut tables
        results = []
        for i in range(0, len(df) - 1, 2):
            combined_avg = (df.loc[i, 'sudut_biasa'] + df.loc[i, 'sudut_luar_biasa'] +
                            df.loc[i + 1, 'sudut_biasa'] + df.loc[i + 1, 'sudut_luar_biasa']) / 4
            sta_1 = df.loc[i, 'STA_1'].replace('_1', '')
            titik_ikat = df.loc[i, 'Titik_Ikat'].replace('_1', '')
            results.append({
                "Pair_ID": f"{df.loc[i, 'id']}-{df.loc[i+1, 'id']}",
                "STA_1": sta_1,
                "Titik_Pantau": df.loc[i, 'Titik_Pantau'],
                "Titik_Ikat": titik_ikat,
                "Sudut": combined_avg
            })
        return pd.DataFrame(results)

    def proses_sudut(self):
        db_path = self.selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return

        conn = sqlite3.connect(db_path)
        try:
            sudut_df = pd.read_sql_query("SELECT * FROM Sudut_T2", conn)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return
        finally:
            conn.close()

        sudut_averages_df = self.calculate_sudut_averages(sudut_df)
        self.save_to_database(sudut_averages_df, "Sudut_Fine_T2")
        self.result_text.insert(tk.END, "Sudut T2 Averages:\n")
        self.result_text.insert(tk.END, sudut_averages_df.to_string(index=False) + "\n\n")

    def proses_sudut_t4(self):
        db_path = self.selected_db_path.get()
        if not db_path:
            messagebox.showwarning("Warning", "Please select a database first.")
            return

        # Load and process Sudut_T4 table
        conn = sqlite3.connect(db_path)
        try:
            sudut_t4_df = pd.read_sql_query("SELECT * FROM Sudut_T4", conn)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return
        finally:
            conn.close()

        # Calculate averages for Sudut T4
        sudut_t4_averages_df = self.calculate_sudut_averages(sudut_t4_df)
        self.save_to_database(sudut_t4_averages_df, "Sudut_Fine_T4")
        self.result_text.insert(tk.END, "Sudut T4 Averages:\n")
        self.result_text.insert(tk.END, sudut_t4_averages_df.to_string(index=False) + "\n\n")

    def save_to_database(self, df, table_name):
        save_path = self.save_db_path.get()
        if not save_path:
            messagebox.showwarning("Warning", "Please specify a save path first.")
            return

        # Save processed data to destination database
        conn = sqlite3.connect(save_path)
        try:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            messagebox.showinfo("Success", f"Data saved to {table_name} in {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
        finally:
            conn.close()

    # "Back" button functionality
    def kembali_to_awal(self):
        self.label_frame.destroy()  
        new_window1()

def proses_azimuth():
    #membuat style, label frame dan tampilan widgets
    #style
    label_frame_az = ttk.Labelframe(win, text=' PERHITUNGAN AZIMUTH ', padding = (30,20), style='Custom.TLabelframe')
    label_frame_az.grid(column=0, row=1, padx=3, pady=3)

    selected_db_path = tk.StringVar()
    save_db_path = tk.StringVar()

    # Database selection function
    def select_database():
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Database selected: {file_path}")

    def save_database_as():
        save_as_file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database files", "*.db")])
        if save_as_file_path:
            save_db_path.set(save_as_file_path)
            messagebox.showinfo("Information", f"Database will be saved as: {save_as_file_path}")
            
    def azimuth(selected_db_path, save_db_path):
        try:
            #Koneksi kepada database lama
            con = sqlite3.connect(selected_db_path)
            curt2 = con.cursor()
            curt4 = con.cursor()

            curt2.execute(''' SELECT id, STA1, sta1_x, sta1_y, STA2, sta2_x, sta2_y, Titik_Pantau FROM Pendefinisian_Titik_T2 ''')
            koord2 = curt2.fetchall()
            curt4.execute(''' SELECT id, STA_1, sta_1_x, sta_1_y, STA_2, sta_2_x, sta_2_y, BS_1, bs_1_x, bs_1_y, BS_2, bs_2_x, bs_2_y, Titik_Pantau FROM Pendefinisian_Titik_T4 ''')
            koord4 = curt4.fetchall()

            #Koneksi pada database baru
            con2 = sqlite3.connect(save_db_path)
            cur2 = con2.cursor()

            cur2.execute('''
                            CREATE TABLE IF NOT EXISTS "Azimuth_sta_t2" (
                        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                        "STA1" TEXT,
                        "STA2" TEXT,
                        "azimuth" REAL,
                        "Titik_Pantau" TEXT,
                        "rumus" TEXT
                            )
                        ''')
            
            cur2.execute('''
                            CREATE TABLE IF NOT EXISTS "Azimuth_sta_t4" (
                        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                        "STA" TEXT,
                        "BS" TEXT,
                        "azimuth" REAL,
                        "Titik_Pantau" TEXT,
                        "rumus" TEXT
                            )
                        ''')
            
            # Mendefinisikan koordinat inisiasi titik pantau
            points = {
                'Ab': (443941.290, 9143047.828),
                'Au': (443944.900, 9143051.222),
                'At': (443948.802, 9143048.611),
                'Nb': (443940.754, 9143083.157),
                'Nu': (443944.256, 9143089.403),
                'Nt': (443947.582, 9143085.212),
                'Gb': (443941.577, 9143119.181),
                'Gs': (443944.432, 9143118.082),
                'Gt': (443947.153, 9143122.398),
                'Bb': (443890.339, 9143048.451),
                'Bu': (443898.126, 9143053.665),
                'Bt': (443903.233, 9143049.025),
                'Wb': (443889.984, 9143122.648),
                'Ws': (443896.869, 9143114.522),
                'Wt': (443902.579, 9143119.386),
                'Sb': (443886.093, 9143083.251),
                'Su': (443895.459, 9143095.457),
                'St': (443906.824, 9143081.634),
                'Ss': (443897.770, 9143073.258)
            }
   
            #membuat fungsi perhitungan azimuth otomatis
            #Azimuth 2 dengan dua titik sta sekaligus backsight
            #Azimuth sta1-sta2
            def azimuth_target_t2_1():
                # Calculate azimuth for each row in koord2 and insert into Azimuth_sta_t2
                try:
                    processed_entries = 0
                    for row in koord2:
                        _, STA1, sta1_x, sta1_y, STA2, sta2_x, sta2_y, Titik_Pantau = row
                        # Menghitung azimuth inisiasi
                        if Titik_Pantau in points:
                            target_x, target_y = points[Titik_Pantau]
                            az = degrees(atan2(sta2_x - sta1_x, sta2_y - sta1_y)) % 360
                            azimuth_target = degrees(atan2(target_x - sta1_x, target_y - sta1_y)) % 360
                            print(f"t2_1 - Azimuth dari {STA1} ke {STA2}: {az}")
                            azimuth_perhitungan_t2_t1(STA1, STA2, az, azimuth_target, Titik_Pantau)
                except Exception as e:
                    print(f"An error occured in azimuth_target_t2_1: {e}")
                
            #Azimuth sta2-sta1
            def azimuth_target_t2_2():
                try:
                    # Calculate azimuth for each row in koord2 and insert into Azimuth_sta_t2
                    for row in koord2:
                        _, STA1, sta1_x, sta1_y, STA2, sta2_x, sta2_y, Titik_Pantau = row
                        # Menghitung azimuth inisiasi
                        if Titik_Pantau in points:
                            target_x, target_y = points[Titik_Pantau]
                            az_ = degrees(atan2(sta1_x - sta2_x, sta1_y - sta2_y)) % 360
                            azimuth_target_ = degrees(atan2(target_x - sta2_x, target_y - sta2_y)) % 360
                            print(f"t2_2 - Azimuth dari {STA2} ke {STA1}: {az_}")
                            azimuth_perhitungan_t2_t2(STA2, STA1, az_, azimuth_target_, Titik_Pantau)
                except Exception as e:
                    print(f"An error occured in azimuth_target_t2_2 :{e}")
                
            #Perhitungan Azimuth real dengan memakai sudut dan azimuth sta1-sta2
            def azimuth_perhitungan_t2_t1(STA1, STA2, az, azimuth_target, Titik_Pantau):
                try:
                    #Menyeleksi database yang akan digunakan
                    curt2.execute(''' SELECT Sudut FROM Sudut_Fine_T2 WHERE Titik_Pantau = ? ''', (Titik_Pantau,))
                    sudut_2 = curt2.fetchall()

                    for i in range(0,len(sudut_2), 2):
                        Sudut = sudut_2[i][0]
                        # Logika pengecekan sudut antara STA-BS dan STA-Target
                        if az > azimuth_target and 0 < az < 90 and 0 < azimuth_target < 90: #-------------------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az < azimuth_target and 0 < az < 90 and 0 < azimuth_target < 90: #----------------------------------------------------
                            azimuth_target_real = Sudut + az
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az > azimuth_target and 90 < az < 180 and 90 < azimuth_target <180: #-------------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az < azimuth_target and 90 < az < 180 and 90 < azimuth_target < 180: #-----------------------------------------------
                            azimuth_target_real = Sudut + az
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az < 90 and 90 < azimuth_target  < 180: #------------------------------------------------------------------------
                            azimuth_target_real =  Sudut + az
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azimuth_target < 90 and 90 < az  < 180: #------------------------------------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az < azimuth_target and 180 < az < 270 and 180 < azimuth_target < 270: #-------------------------------------------
                            azimuth_target_real = Sudut + az
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az > azimuth_target and 180 < az < 270 and 180 < azimuth_target < 270: #-------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az < azimuth_target and 270 < az < 360 and 270 < azimuth_target < 360: #------------------------------------------
                            azimuth_target_real = Sudut + az
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az > azimuth_target and 270 < az < 360 and 270 < azimuth_target < 360: #------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < az < 270 and 270 < azimuth_target < 360: #------------------------------------------------------------------
                            azimuth_target_real = Sudut + az
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < azimuth_target < 270 and 270 < az < 360: #------------------------------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < az < 180 and 180 < azimuth_target < 270: #-------------------------------------------------------------------
                            azimuth_target_real = az + Sudut
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < azimuth_target < 180 and 180 < az < 270: #-------------------------------------------------------------------
                            azimuth_target_real = az - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az < 90 and 270 < azimuth_target < 360: #-----------------------------------------------------------------------
                            azimuth_target_real = (360-Sudut) + az
                            print(f"Nilai dari e3 : {azimuth_target_real}\n")
                            print(az)
                            print(Sudut)
                            rumus_terpilih = 'e3'
                            save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)    
                        elif 0 < azimuth_target < 90 and 270 < az < 360: #----------------------------------------------------------------------
                                azimuth_target_real = az - (360-Sudut)
                                print(f"Nilai dari e4 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e4'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < az < 360 and 90 < azimuth_target < 180: #******************************************************************_______
                            if (az-azimuth_target) < 180:
                                azimuth_target_real = az - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az - (360-Sudut)
                                print(f"Nilai dari e4 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e4'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < azimuth_target < 360 and 90 < az < 180: #******************************************************************_______
                            if (azimuth_target - az) < 180:
                                azimuth_target_real = Sudut + az
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az < 90 and 180 < azimuth_target < 270: #*******************************************************************________
                            if (azimuth_target-az) < 180:
                                azimuth_target_real = Sudut + az
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azimuth_target < 90 and 180 < az < 270: #******************************************************************________
                            if (az-azimuth_target) < 180:
                                azimuth_target_real = az - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az - (360-Sudut)
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t2(STA1, STA2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                except Exception as e:
                    print(f"An error occured : {e}")

            #Perhitungan Azimuth real dengan memakai sudut dan azimuth sta2-sta1
            def azimuth_perhitungan_t2_t2(STA2, STA1, az_, azimuth_target_, Titik_Pantau):
                try:
                    #Menyeleksi database yang akan digunakan
                    curt2.execute(''' SELECT Sudut FROM Sudut_Fine_T2 WHERE Titik_Pantau = ? ''', (Titik_Pantau,))
                    sudut_2 = curt2.fetchall()
                
                    for i in range(1,len(sudut_2),2):
                        Sudut  = sudut_2[i][0]
                        # Logika pengecekan sudut antara STA-BS dan STA-Target
                        if az_ > azimuth_target_ and 0< az_ < 90 and 0 < azimuth_target_ < 90:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ < azimuth_target_ and 0 < az_ < 90 and 0 < azimuth_target_ < 90:
                            azimuth_target_real = Sudut + az_
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ > azimuth_target_ and 90 < az_ < 180 and 90 < azimuth_target_ <180:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ < azimuth_target_ and 90 < az_ < 180 and 90 < azimuth_target_ < 180:
                            azimuth_target_real = Sudut + az_
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az_ < 90 and 90 < azimuth_target_  < 180:
                            azimuth_target_real =  Sudut + az_
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azimuth_target_ < 90 and 90 < az_  < 180:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ < azimuth_target_ and 180 < az_ < 270 and 180 < azimuth_target_ < 270:
                            azimuth_target_real = Sudut + az_
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ > azimuth_target_ and 180 < az_ < 270 and 180 < azimuth_target_ < 270:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ < azimuth_target_ and 270 < az_ < 360 and 270 < azimuth_target_ < 360:
                            azimuth_target_real = Sudut + az_
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az_ > azimuth_target_ and 270 < az_ < 360 and 270 < azimuth_target_ < 360:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < az_ < 270 and 270 < azimuth_target_ < 360:
                            azimuth_target_real = Sudut + az_
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < azimuth_target_ < 270 and 270 < az_ < 360:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < az_ < 180 and 180 < azimuth_target_ < 270:
                            azimuth_target_real = az_ + Sudut
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e1'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < azimuth_target_ < 180 and 180 < az_ < 270:
                            azimuth_target_real = az_ - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e2'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az_ < 90 and 270 < azimuth_target_ < 360: 
                            azimuth_target_real = (360-Sudut) + az_
                            print(f"Nilai dari e3 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e3'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih) 
                        elif 0 < azimuth_target_ < 90 and 270 < az_ < 360: 
                            azimuth_target_real = az_ - (360-Sudut)
                            print(f"Nilai dari e4 : {azimuth_target_real}\n")
                            print(az_)
                            print(Sudut)
                            rumus_terpilih = 'e4'
                            save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < az_ < 360 and 90 < azimuth_target_ < 180: #*************************************************____________
                            if (az_-azimuth_target_) < 180:
                                azimuth_target_real = az_ - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az_ - (360-Sudut)
                                print(f"Nilai dari e4 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e4'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < azimuth_target_ < 360 and 90 < az_ < 180: #**************************************************____________
                            if (azimuth_target_ - az_) < 180:
                                azimuth_target_real = Sudut + az_
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az_
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az_ < 90 and 180 < azimuth_target_ < 270:#*********************************************************____________
                            if (azimuth_target_-az_) < 180:
                                azimuth_target_real = Sudut + az_
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az_
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azimuth_target_ < 90 and 180 < az_ < 270: #*************************************************************__________
                            if (az_-azimuth_target_) < 180:
                                azimuth_target_real = az_ - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az_ - (360-Sudut)
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az_)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t2(STA2, STA1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                except Exception as e:
                    print(f"An error occured : {e}")

            def save_data_t2(STA,STA_,azimuth_value, Titik_Pantau, rumus):
                try: 
                    cur2.execute('''INSERT INTO Azimuth_sta_t2 (STA1, STA2, azimuth, Titik_Pantau, rumus) VALUES(?, ?, ?, ?, ?)''',
                                 (STA, STA_, azimuth_value, Titik_Pantau, rumus))
                    con2.commit()
                except Exception as e:
                    print(f"An error occured in save data t2:{e}")
            
            #Azimuth 4 dengan tiga/4 titik dengan 2 sta berbeda dan 2 backsight berbeda
            #Azimuth sta1
            def azimuth_target_t4_1():
                try:
                    # Calculate azimuth for each row in koord4 and insert into Azimuth_sta_t4
                    for row in koord4:
                        _,STA_1, sta_1_x, sta_1_y, STA_2, sta_2_x, sta_2_y, BS_1, bs_1_x, bs_1_y, BS_2, bs_2_x, bs_2_y, Titik_Pantau = row
                        # Menghitung azimuth inisiasi
                        if Titik_Pantau in points:
                            target_x, target_y = points[Titik_Pantau]
                            azi1 = degrees(atan2(target_x - sta_1_x, target_y - sta_1_y)) % 360 #azimuth sta - target(inisiasi)
                            az1 = degrees(atan2(bs_1_x - sta_1_x, bs_1_y - sta_1_y)) % 360 #azimuth sta - ikat
                            print(f"t4_1 - Azimuth dari {STA_1} ke {BS_1}: {az1}")
                            azimuth_perhitungan_t4_1(STA_1, BS_1, az1, azi1, Titik_Pantau)
                except Exception as e:
                    print(f"An error occured in azimuth_target_t4 1: {e}")
            #Azimuth sta2
            def azimuth_target_t4_2():
                try:
                    # Calculate azimuth for each row in koord4 and insert into Azimuth_sta_t4
                    for row in koord4:
                        _,STA_1, sta_1_x, sta_1_y, STA_2, sta_2_x, sta_2_y, BS_1, bs_1_x, bs_1_y, BS_2, bs_2_x, bs_2_y, Titik_Pantau = row
                        # Menghitung azimuth inisiasi
                        if Titik_Pantau in points:
                            target_x, target_y = points[Titik_Pantau]
                            azi2 = degrees(atan2(target_x - sta_2_x, target_y - sta_2_y)) % 360 #azimuth sta - target(inisiasi)
                            az2 = degrees(atan2(bs_2_x - sta_2_x, bs_2_y - sta_2_y)) % 360 #azimuth sta - ikat
                            print("Menjalankan azimuth perhitungan")
                            azimuth_perhitungan_t4_2(STA_2, BS_2, az2, azi2, Titik_Pantau)
                except Exception as e:
                    print(f"An error occured in azimuth_target_t4 2: {e}")

            #Perhitungan Azimuth real dengan memakai sudut dan azimuth STA1-Ikat1
            def azimuth_perhitungan_t4_1(STA_1, BS_1, az1, azi1, Titik_Pantau):
                try:
                    #Menyeleksi database yang akan digunakan
                    curt4.execute(''' SELECT Sudut FROM Sudut_Fine_T4 WHERE Titik_Pantau = ? ''', (Titik_Pantau,))
                    sudut_4 = curt4.fetchall()
                    #save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                    for i in range(0,len(sudut_4),2):
                        Sudut = sudut_4[i][0]
                        # Logika pengecekan sudut antara STA-BS dan STA-Target
                        if az1 > azi1 and 0 < az1 < 90 and 0 < azi1 < 90:
                            azimuth_target_real = az1 - Sudut
                            print(f"Nilai dari Azimuth : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 < azi1 and 0 < az1 < 90 and 0 < azi1 < 90:
                            azimuth_target_real = Sudut + az1
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 > azi1 and 90 < az1 < 180 and 90 < azi1 < 180:
                            azimuth_target_real = az1 - Sudut
                            print(f"Nilai dari Azimuth : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 < azi1 and 90 < az1 < 180 and 90 < azi1 < 180:
                            azimuth_target_real = Sudut + az1
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azi1 < 90 and 90 < az1 < 180:
                            azimuth_target_real = az1 - Sudut
                            print(f"Nilai dari Azimuth : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az1 < 90 and 90 < azi1 < 180:
                            azimuth_target_real = Sudut + az1
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 < azi1 and 180 < az1 < 270 and 180 < azi1 < 270:
                            azimuth_target_real = Sudut + az1
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 > azi1 and 180 < az1 < 270 and 180 < azi1 < 270:
                            azimuth_target_real = az1 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 < azi1 and 270 < az1 < 360 and 270 < azi1 < 360:
                            azimuth_target_real = Sudut + az1
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az1 > azi1 and 270 < az1 < 360 and 270 < azi1 < 360:
                            azimuth_target_real = az1 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < az1 < 270 and 270 < azi1 < 360:
                            azimuth_target_real = Sudut + az1
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < azi1 < 270 and 270 < az1 < 360:
                            azimuth_target_real = az1 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < az1 < 180 and 180 < azi1 < 270:
                            azimuth_target_real =  az1 + (360-Sudut)
                            print(f"Nilai dari e3 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e3'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < azi1 < 180 and 180 < az1 < 270:
                            azimuth_target_real = az1 - (Sudut-360)
                            print(f"Nilai dari e4 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e4'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az1 < 90 and 270 < azi1 < 360:
                            azimuth_target_real = (360-Sudut) + az1
                            print(f"Nilai dari e3 : {azimuth_target_real}\n")
                            print(az1)
                            print(Sudut)
                            rumus_terpilih = 'e3'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih) 
                        elif 0 < azi1 < 90 and 270 < az1 < 360:
                            azimuth_target_real = az1 - (360-Sudut)
                            print(f"Nilai dari e4 : {azimuth_target_real}\n")
                            print(az1)
                            print(Sudut)
                            rumus_terpilih = 'e4'
                            save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < az1 < 360 and 90 < azi1 < 180:
                            if (az1-azi1) < 180:
                                azimuth_target_real = az1 - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az1 - (360-Sudut)
                                print(f"Nilai dari e4 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e4'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < azi1 < 360 and 90 < az1 < 180:
                            if (azi1 - az1) < 180:
                                azimuth_target_real = Sudut + az1
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az1
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az1 < 90 and 180 < azi1 < 270:
                            if (azi1-az1) < 180:
                                azimuth_target_real = Sudut + az1
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az1
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azi1 < 90 and 180 < az1 < 270:
                            if (az1-azi1) < 180:
                                azimuth_target_real = az1 - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az1 - (360-Sudut)
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az1)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t4(STA_1, BS_1, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                except Exception as e:
                    print(f"An error occured in azimuth_perhitungan t4 1: {e}")
            #Perhitungan Azimuth real dengan memakai sudut dan azimuth STA2-Ikat2
            def azimuth_perhitungan_t4_2(STA_2, BS_2, az2, azi2, Titik_Pantau):
                try:
                    #Menyeleksi database yang akan digunakan
                    curt4.execute(''' SELECT Sudut FROM Sudut_Fine_T4 WHERE Titik_Pantau = ? ''', (Titik_Pantau,))
                    sudut_4 = curt4.fetchall()

                    for i in range(1,len(sudut_4),2):
                        Sudut= sudut_4[i][0]
                        # Logika pengecekan sudut antara STA-BS dan STA-Target
                        if az2 > azi2 and 0 < az2 < 90 and 0 < azi2 < 90:
                            azimuth_target_real = (az2) - (360 - Sudut)
                            print(f"Nilai dari Azimuth : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 < azi2 and 0 < az2 < 90 and 0 < azi2 < 90:
                            azimuth_target_real = Sudut + az2
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 > azi2 and 90 < az2 < 180 and 90 < azi2 < 180:
                            azimuth_target_real = az2 - Sudut
                            print(f"Nilai dari Azimuth : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 < azi2 and 90 < az2 < 180 and 90 < azi2 < 180:
                            azimuth_target_real = Sudut + az2
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azi2 < 90 and 90 < az2 < 180:
                            azimuth_target_real = az2 - Sudut
                            print(f"Nilai dari Azimuth : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az2 < 90 and 90 < azi2 < 180:
                            azimuth_target_real = Sudut + az2
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 < azi2 and 180 < az2 < 270 and 180 < azi2 < 270:
                            azimuth_target_real = Sudut + az2
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 > azi2 and 180 < az2 < 270 and 180 < azi2 < 270:
                            azimuth_target_real = az2 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 < azi2 and 270 < az2 < 360 and 270 < azi2 < 360:
                            azimuth_target_real = Sudut + az2
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif az2 > azi2 and 270 < az2 < 360 and 270 < azi2 < 360:
                            azimuth_target_real = az2 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < az2 < 270 and 270 < azi2 < 360:
                            azimuth_target_real = Sudut + az2
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 180 < azi2 < 270 and 270 < az2 < 360:
                            azimuth_target_real = az2 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < az2 < 180 and 180 < azi2 < 270:
                            azimuth_target_real =  az2 + Sudut
                            print(f"Nilai dari e1 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e1'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 90 < azi2 < 180 and 180 < az2 < 270:
                            azimuth_target_real = az2 - Sudut
                            print(f"Nilai dari e2 : {azimuth_target_real}\n")
                            rumus_terpilih = 'e2'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az2 < 90 and 270 < azi2 < 360:
                            azimuth_target_real = (360-Sudut) + az2
                            print(f"Nilai dari e3 : {azimuth_target_real}\n")
                            print(az2)
                            print(Sudut)
                            rumus_terpilih = 'e3'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azi2 < 90 and 270 < az2 < 360:
                            azimuth_target_real = az2 - (360-Sudut)
                            print(f"Nilai dari e4 : {azimuth_target_real}\n")
                            print(az2)
                            print(Sudut)
                            rumus_terpilih = 'e4'
                            save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < az2 < 360 and 90 < azi2 < 180:
                            if (az2-azi2) < 180:
                                azimuth_target_real = az2 - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az2 - (360-Sudut)
                                print(f"Nilai dari e4 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e4'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 270 < azi2 < 360 and 90 < az2 < 180:
                            if (azi2 - az2) < 180:
                                azimuth_target_real = Sudut + az2
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az2
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < az2 < 90 and 180 < azi2 < 270:
                            if (azi2-az2) < 180:
                                azimuth_target_real = Sudut + az2
                                print(f"Nilai dari e1 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e1'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = (360-Sudut) + az2
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                        elif 0 < azi2 < 90 and 180 < az2 < 270:
                            if (az2-azi2) < 180:
                                azimuth_target_real = az2 - Sudut
                                print(f"Nilai dari e2 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e2'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                            else:
                                azimuth_target_real = az2 - (360-Sudut)
                                print(f"Nilai dari e3 : {azimuth_target_real}\n")
                                print(az2)
                                print(Sudut)
                                rumus_terpilih = 'e3'
                                save_data_t4(STA_2, BS_2, azimuth_target_real, Titik_Pantau, rumus_terpilih)
                except Exception as e:
                    print(f"An error occured : {e}")
            #save data azimuth t4
            def save_data_t4(STA,BS,azimuth_value, Titik_Pantau, rumus):
                try: 
                    cur2.execute('''INSERT INTO Azimuth_sta_t4 (STA, BS, azimuth, Titik_Pantau, rumus) VALUES(?, ?, ?, ?, ?)''',
                                 (STA, BS, azimuth_value, Titik_Pantau, rumus))
                    con2.commit()
                except Exception as e:
                    print(f"An error occured in save data t4:{e}")
            
            #Start Awal Proses Azimuth
            azimuth_target_t2_1()
            azimuth_target_t2_2()
            
            azimuth_target_t4_1()
            azimuth_target_t4_2()

            # Function to sort, drop, and replace a table
            def sortir_tabel(table_name):
                # Load and sort the data by 'Titik_Pantau'
                query = f"SELECT * FROM {table_name} ORDER BY Titik_Pantau ASC;"
                sorted_data = pd.read_sql_query(query, con2)  # Use con2 instead of cur2
                sorted_data['id'] = range(1, len(sorted_data) + 1)

                # Drop the existing table and create a new one with sorted data
                with con2:
                    con2.execute(f"DROP TABLE IF EXISTS {table_name};")  # Corrected typo
                    sorted_data.to_sql(table_name, con2, if_exists='replace', index=False)  # Use con2 instead of cur2

                # Confirm the changes (optional, for verification)
                updated_query = f"SELECT * FROM {table_name} ORDER BY id;"
                updated_data = pd.read_sql_query(updated_query, con2)
                print(f"Updated Data for {table_name}:")
                print(updated_data)  # Display first few rows for verification
                
                result_text.insert(tk.END, f"Updated Data for {table_name}:\n{updated_data.to_string()}\n\n")

            # Apply the function to both tables
            result_text.delete('1.0', tk.END)
            sortir_tabel('Azimuth_sta_t2')
            sortir_tabel('Azimuth_sta_t4')

            # Close the connection
            con2.close()

            def migrate_tables(selected_db_path, save_db_path):
                # Migrate tables from source to destination database
                try:
                    # Connect to source database and retrieve tables
                    conn_src = sqlite3.connect(selected_db_path)
                    pendefinisian_titik_df = pd.read_sql_query("SELECT * FROM Pendefinisian_Titik_T2", conn_src)
                    pendefinisian_titik_t4_df = pd.read_sql_query("SELECT * FROM Pendefinisian_Titik_T4", conn_src)
                    sudut_t2_df = pd.read_sql_query("SELECT * FROM Sudut_Fine_T2",conn_src)
                    sudut_t4_df = pd.read_sql_query("SELECT * FROM Sudut_Fine_T4",conn_src)
                    Jarak_Fine_t2_df = pd.read_sql_query("SELECT * FROM Jarak_Fine_T2", conn_src)
                    Jarak_Fine_t4_df = pd.read_sql_query("SELECT * FROM Jarak_Fine_T4", conn_src)
                    Simpangan_Baku_df = pd.read_sql_query("SELECT * FROM Simpangan_Baku", conn_src)
                    conn_src.close()

                    # Connect to destination database and save tables
                    conn_dest = sqlite3.connect(save_db_path)
                    pendefinisian_titik_df.to_sql("Pendefinisian_Titik_T2", conn_dest, if_exists='replace', index=False)
                    pendefinisian_titik_t4_df.to_sql("Pendefinisian_Titik_T4", conn_dest, if_exists='replace', index=False)
                    sudut_t2_df.to_sql("Sudut_Fine_T2", conn_dest,if_exists='replace', index=False)
                    sudut_t4_df.to_sql("Sudut_Fine_T4", conn_dest,if_exists='replace', index=False)
                    Jarak_Fine_t2_df.to_sql("Jarak_Fine_T2", conn_dest,if_exists='replace', index=False)
                    Jarak_Fine_t4_df.to_sql("Jarak_Fine_T4", conn_dest,if_exists='replace', index=False)
                    Simpangan_Baku_df.to_sql("Simpangan_Baku", conn_dest, if_exists='replace', index=False)
                    conn_dest.close()

                    messagebox.showinfo("Success")

                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during migration: {e}")
            #Menjalankan Migrasi
            migrate_tables(selected_db_path, save_db_path)

        except Exception as e:
            print(f"An error occured: {e}")


    def kembali_to_awal():
        label_frame_az.destroy()
        new_window1()
    #Doc
    info = """
    NOTE:
    1. Pilih Database yang telah di proses oleh menu "pengolahan data" (data yang anda save as)
    2. Klik "Save As" untuk menyimpan data hasil Azimuth
    3. Klik "Proses Azimuth" untuk memulai proses perhitungan azimuth.
    4. Klik "Kembali" untuk kembali ke menu awal.
    """
    Label(label_frame_az, text=info,justify="left",background=background_color,font=("Calibri", 14), foreground="white").grid(column=0, row=0,columnspan=3, padx=8, pady=8, sticky="w")
    #lebar button
    button_width = 15
    #GUI Elements
    Button(label_frame_az, text="Select Database", command=lambda:select_database(),bg="#FFC900",font=("Calibri", 14),width=button_width).grid(column=0, row=2, padx=8, pady=8)
    Button(label_frame_az, text=" Save as ", command=lambda:save_database_as(),bg="#FFC900",font=("Calibri", 14),width=button_width).grid(column=1, row=2, padx=8, pady=8)
    Button(label_frame_az, text="Proses Azimuth", command=lambda:azimuth(selected_db_path.get(), save_db_path.get()),bg="#FFC900",font=("Calibri", 14),width=button_width).grid(column=2, row=2, padx=8, pady=8)
    Button(label_frame_az, text="Kembali", command=kembali_to_awal,bg="#FFC900",font=("Calibri", 14),width=button_width).grid(column=3, row=2, padx=8, pady=8)

    result_text = tk.Text(label_frame_az, wrap=tk.WORD, width=150, height=20)
    result_text.grid(column=0,columnspan=4, row=1, padx=8, pady=8)

def koord_pendekatan():
    #membuat style, label frame dan tampilan widgets
    #style
    label_frame_az = ttk.Labelframe(win, text=' PERHITUNGAN KOORDINAT PENDEKATAN ', padding = (30,20), style='Custom.TLabelframe')
    label_frame_az.grid(column=0, row=1, padx=3, pady=3)

    selected_db_path = tk.StringVar()

    # Database selection function
    def select_database():
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Database selected: {file_path}")

    def koord(selected_db_path):
        try:
            #Koneksi kepada database lama
            con = sqlite3.connect(selected_db_path)
            curt2 = con.cursor()
            curt4 = con.cursor()
            dist2 = con.cursor()
            dist4 = con.cursor()
            az2 = con.cursor()
            az4 = con.cursor()
            save_data = con.cursor()

            #mengambil database T2
            curt2.execute(''' SELECT STA1, sta1_x, sta1_y, Titik_Pantau FROM Pendefinisian_Titik_T2 ''')
            koord2 = curt2.fetchall()
            dist2.execute(''' SELECT STA_1, Jarak_P, Titik_Pantau FROM Jarak_Fine_T2 ''')
            jarak2 = dist2.fetchall()
            az2.execute(''' SELECT STA1, azimuth, Titik_Pantau FROM Azimuth_sta_T2 ''')
            azimuth2 = az2.fetchall()

            #Mengambil database T4
            curt4.execute(''' SELECT STA_1, sta_1_x, sta_1_y, Titik_Pantau FROM Pendefinisian_Titik_T4 ''')
            koord4 = curt4.fetchall()
            dist4.execute(''' SELECT STA_1, Jarak_P, Titik_Pantau FROM Jarak_Fine_T4 ''')
            jarak4 = dist4.fetchall()
            az4.execute(''' SELECT STA, azimuth, Titik_Pantau FROM Azimuth_sta_T4 ''')
            azimuth4 = az4.fetchall()

            # Ambil urutan titik_pantau dari Sudut_Fine_T2 dan Sudut_Fine_T4
            save_data.execute("SELECT DISTINCT Titik_Pantau FROM Sudut_Fine_T2 ORDER BY rowid")
            titik_pantau_t2 = [row[0] for row in save_data.fetchall()]

            save_data.execute("SELECT DISTINCT Titik_Pantau FROM Sudut_Fine_T4 ORDER BY rowid")
            titik_pantau_t4 = [row[0] for row in save_data.fetchall()]

            # Gabungkan dan hilangkan duplikat
            titik_pantau_order = list(dict.fromkeys(titik_pantau_t2 + titik_pantau_t4))

            save_data.execute('''
                            CREATE TABLE IF NOT EXISTS "Koordinat_Pendekatan" (
                        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                        "Titik_Pantau" TEXT,
                        "X_Target" TEXT,
                        "Y_Target" REAL
                            )
                        ''')

            data_to_save = [] # Temporary list to store data before saving
            
            # Fungsi untuk menyimpan data koordinat pendekatan ke dalam list sementara
            def save_data_koord(Titik_Pantau, xt, yt):
                data_to_save.append((Titik_Pantau, xt, yt))

            #Fungsi untuk perhitungan koordinat pendekatan
            def perhitungan(jarak, azimuth, xi, yi, Titik_Pantau):
                xt = xi + jarak * np.sin(np.radians(azimuth))
                yt = yi + jarak * np.cos(np.radians(azimuth))
                save_data_koord(Titik_Pantau, xt, yt)

            #Fungsi untuk koordinat pendekatan T2
            def koordinat_pendekatan_t2():
                try:
                    for koord in koord2: #koord , jarak , azimuth in zip(koord2, jarak2, azimuth2):
                        STA1, sta1_x, sta1_y, Titik_Pantau = koord
                        jarak_list = [j for j in jarak2 if j[0] == STA1 and j[2] == Titik_Pantau]
                        azimuth_list = [a for a in azimuth2 if a[0] == STA1 and a[2] == Titik_Pantau]
                        if jarak_list and azimuth_list:
                            for jarak, azimuth in zip(jarak_list, azimuth_list):
                                try:
                                    _ , Jarak_P, _ = jarak 
                                    _ , azimuth, _ = azimuth
                                    perhitungan(Jarak_P, azimuth, sta1_x, sta1_y, Titik_Pantau)
                                except Exception as e:
                                    print(f"An error occured: {e}")
                except Exception as e:
                    print(f"An error occured: {e}")
                
            #Fungsi untuk koordinat pendekatan T2
            def koordinat_pendekatan_t4():
                try:
                    for koord in koord4: #koord,jarak,azimuth in zip(koord4, jarak4, azimuth4):
                        STA_1, sta_1_x, sta_1_y, Titik_Pantau = koord
                        jarak_list = [j for j in jarak4 if j[0] == STA_1 and j[2] == Titik_Pantau]
                        azimuth_list = [a for a in azimuth4 if a[0] == STA_1 and a[2] == Titik_Pantau] 
                        if jarak_list and azimuth_list:
                            for jarak, azimuth in zip(jarak_list, azimuth_list):
                                try:
                                    _ , Jarak_P, _ = jarak
                                    _ , azimuth, _ = azimuth
                                    perhitungan(Jarak_P, azimuth, sta_1_x, sta_1_y, Titik_Pantau)
                                except Exception as e:
                                    print(f"An error occured: {e}")
                except Exception as e:
                    print(f"An error occured: {e}")

            koordinat_pendekatan_t2()
            koordinat_pendekatan_t4()

            # Sort data_to_save berdasarkan urutan titik_pantau_order
            data_to_save.sort(key=lambda x: titik_pantau_order.index(x[0]) if x[0] in titik_pantau_order else len(titik_pantau_order))

            # Simpan data yang sudah terurut ke database
            for Titik_Pantau, xt, yt in data_to_save:
                try:
                    save_data.execute('''INSERT INTO Koordinat_Pendekatan (Titik_Pantau, X_Target, Y_Target) VALUES(?, ?, ?)''',
                                      (Titik_Pantau, xt, yt))
                    con.commit()
                    result_text.insert(tk.END, f"Data saved: Titik_Pantau={Titik_Pantau}, X_Target={xt}, Y_Target={yt}\n")
                except Exception as e:
                    print(f"An error occurred in saving sorted data: {e}")

        except Exception as e:
            print(f"An error occured in koord :{e}")
    
    def database_matang(selected_db_path):
        con = sqlite3.connect(selected_db_path)
        cur = con.cursor()

        # Membuat tabel gabungan untuk hasil akhir
        cur.execute(""" 
        CREATE TABLE IF NOT EXISTS Gabung_Data_T2_T4 (
            STA TEXT,
            BS TEXT,
            Jarak_P REAL, 
            Jarak_I REAL,
            Sudut REAL,
            Rumus TEXT,
            Titik_Pantau TEXT
        )
        """)

        try:
            # Query untuk mengambil data dari T2
            query_t2 = """ 
            SELECT DISTINCT
                t1.STA_1 AS STA,
                t2.Titik_Ikat AS BS,
                t1.Jarak_P, 
                t1.Jarak_I, 
                t2.Sudut,
                t3.rumus,
                t1.Titik_Pantau
            FROM Jarak_Fine_T2 t1
            INNER JOIN Sudut_Fine_T2 t2 
                ON t1.STA_1 = t2.STA_1 AND t1.Titik_Pantau = t2.Titik_Pantau
            INNER JOIN Azimuth_sta_t2 t3 
                ON t3.STA1 = t1.STA_1 AND t3.Titik_Pantau = t1.Titik_Pantau
            """

            # Eksekusi query dan masukkan hasil ke tabel gabungan
            cur.execute(query_t2)
            results_t2 = cur.fetchall()

            for row in results_t2:
                cur.execute(""" 
                INSERT OR IGNORE INTO Gabung_Data_T2_T4 (STA, BS, Jarak_P, Jarak_I, Sudut, Rumus, Titik_Pantau)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, row)

            # Query untuk mengambil data dari T4
            query_t4 = """ 
            SELECT DISTINCT
                t1.STA_1 AS STA,
                t2.Titik_Ikat AS BS,
                t1.Jarak_P, 
                t1.Jarak_I, 
                t2.Sudut,
                t3.rumus,
                t1.Titik_Pantau
            FROM Jarak_Fine_T4 t1
            INNER JOIN Sudut_Fine_T4 t2 
                ON t1.STA_1 = t2.STA_1 AND t1.Titik_Pantau = t2.Titik_Pantau
            INNER JOIN Azimuth_sta_t4 t3 
                ON t3.STA = t1.STA_1 AND t3.Titik_Pantau = t1.Titik_Pantau
            """

            # Eksekusi query dan masukkan hasil ke tabel gabungan
            cur.execute(query_t4)
            results_t4 = cur.fetchall()

            for row in results_t4:
                cur.execute(""" 
                INSERT OR IGNORE INTO Gabung_Data_T2_T4 (STA, BS, Jarak_P, Jarak_I, Sudut, Rumus, Titik_Pantau)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, row)

            # Commit perubahan
            con.commit()

            # Verifikasi hasil tabel gabungan
            cur.execute("SELECT * FROM Gabung_Data_T2_T4")
            merged_result = cur.fetchall()

            for row in merged_result:
                print(row)

            print("Data dari T2 dan T4 berhasil digabungkan ke tabel Gabung_Data_T2_T4.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Tutup koneksi
            con.close()

        # Back button
    def kembali_to_awal():
        label_frame_az.destroy()
        new_window1()
    # Doc
    info = """
    NOTE:
    1. Pilih Database yang telah di proses oleh menu "perhitungan azimuth" (data yang anda save as).
    2. Klik "Proses Koordinat Pendekatan" untuk memulai proses perhitungan koordinat.
    3. Klik "Proses Database HKT" untuk mulai memproses seluruh database yang diperlukan dalam perhitungan HKT.
    4. Klik "Kembali" untuk kembali ke menu awal.
    """
    Label(
        label_frame_az,
        text=info,
        justify="left",
        background=background_color,
        font=("Calibri", 14),
        foreground="white"
    ).grid(column=0, row=0, columnspan=3, padx=8, pady=8, sticky="w")

    # Lebar tombol seragam
    button_width = 25

    # GUI Elements
    Button(
        label_frame_az,
        text="Select Database",
        command=lambda: select_database(),
        bg="#FFC900",
        font=("Calibri", 14),
        width=button_width
    ).grid(column=0, row=2, padx=8, pady=8, sticky="w")

    Button(
        label_frame_az,
        text="Proses Koordinat Pendekatan",
        command=lambda: koord(selected_db_path.get()),
        bg="#FFC900",
        font=("Calibri", 14),
        width=button_width
    ).grid(column=1, row=2, padx=8, pady=8, sticky="w")

    Button(
        label_frame_az,
        text="Proses Database HKT",
        command=lambda: database_matang(selected_db_path.get()),
        bg="#FFC900",
        font=("Calibri", 14),
        width=button_width
    ).grid(column=2, row=2, padx=8, pady=8, sticky="w")

    Button(
        label_frame_az,
        text="Kembali",
        command=kembali_to_awal,
        bg="#FFC900",
        font=("Calibri", 14),
        width=button_width
    ).grid(column=3, row=2, padx=8, pady=8, sticky="w")

    # Area untuk menampilkan hasil
    result_text = tk.Text(label_frame_az, wrap=tk.WORD, width=150, height=20)
    result_text.grid(column=0, columnspan=4, row=1, padx=8, pady=8)

#proses perhitungan hkt
class hkt:
    def __init__(self, win):
        # Definisikan warna latar belakang
        background_color = "#15395b"

        # Atur gaya untuk LabelFrame
        style = ttk.Style()
        style.configure("Custom.TLabelframe", background=background_color, foreground="white", font=("Arial", 12, "bold"))
        style.configure("Custom.TLabelframe.Label", background=background_color, foreground="white")

        # Main Frame
        self.label_frame = ttk.Frame(win, style="Custom.TLabelframe")
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Konfigurasi grid utama
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)

        # Variables for database paths
        self.selected_db_path = tk.StringVar()  # Source database path

        # Buat elemen GUI
        self.create_widgets(self.label_frame)

    def create_widgets(self, label_frame):
        # Informasi dan hasil dalam satu frame
        info_result_frame = tk.Frame(
            label_frame,
            bg="#15395b"
        )
        info_result_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Konfigurasi grid pada frame utama
        label_frame.rowconfigure(1, weight=1)
        label_frame.columnconfigure(0, weight=1)

        # Informasi cara penggunaan
        info_text = tk.Text(
            info_result_frame,
            wrap=tk.WORD,
            width=100,
            height=6,
            font=("Arial", 12),
            bg="#15395b",
            fg="white",
            state=tk.DISABLED,
            bd=0,  # Tidak ada cekungan
            highlightthickness=0  # Hilangkan border
        )
        info_text.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="w")
        info_text.configure(state=tk.NORMAL)
        info_text.insert(tk.END, "1. Pilih database menggunakan tombol 'Pilih Database'.\n")
        info_text.insert(tk.END, "2. Gunakan tombol sesuai urutan untuk melakukan perhitungan langkah demi langkah.\n")
        info_text.insert(tk.END, "3. Hasil perhitungan akan ditampilkan pada area di bawah ini.\n")
        info_text.insert(tk.END, "4. Tombol Iterasi akan menjalankan perhitungan sampai konvergen.\n")
        info_text.configure(state=tk.DISABLED)

        # Area teks untuk hasil
        self.result_text_combined = tk.Text(
            info_result_frame,
            wrap=tk.WORD,
            width=100,
            height=15,
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#000000",
            bd=0,  # Tidak ada cekungan
            highlightthickness=0  # Hilangkan border
        )
        self.result_text_combined.grid(row=1, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")

        # Konfigurasi seragam untuk tombol
        button_width = 25  # Lebar tombol seragam
        padx, pady = 5, 5  # Padding seragam

        # Frame untuk tombol (definisikan sebagai atribut kelas)
        self.button_frame = tk.Frame(label_frame, bg="#15395b")
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Tombol Pilih Database
        ttk.Button(self.button_frame, text="Pilih Database", command=self.select_database, width=button_width).grid(row=0, column=0, columnspan=3, padx=padx, pady=pady, sticky="ew")

        #Fungsi sementara
        def placeholder():
            self.update_result_text("Fungsi belum diimplementasikan")
        # Tempatkan tombol langkah utama secara grid
        steps = [
            ("1. Generate Rumus", self.generate_rumus_and_validate),
            ("2. Generate Variables", self.fetch_all_variables_from_db),
            ("3. Inisiasi Koordinat", self.fetch_coordinate_values),
            ("4. Proses Matrix A", self.calculate_jacobian_matrix),
            ("5. Proses Matrix L1", self.matrix_L1),
            ("6. Proses Matrix L01", self.matrix_L01),
            ("7. Proses Matrix F1", self.matrix_F1),
            ("8. Proses Matrix L2",self.matrix_L2),
            ("9. Proses Matrix L02",self.matrix_L02),
            ("10. Proses Matrix F2",self.matrix_F2),
            ("11. Proses Matrix P", self.calculate_variances_and_matrices),
            ("12. Proses Matrix X", self.delta_x),
            ("13. Iterasi", self.least_squares),
            ("14. Uji Global", self.request_global_test_input),
            ("15. Data Snooping", self.data_snooping_test),
            ("Kembali", self.kembali_to_awal),
        ]

        for i, (text, command) in enumerate(steps):
            row, col = divmod(i, 5)  # Maksimal 3 tombol per baris
            ttk.Button(self.button_frame, text=text, command=command, width=button_width).grid(row=row + 1, column=col, padx=padx, pady=pady)

        # Input untuk Uji Global di bawah tombol
        self.add_global_test_input()

    def add_global_test_input(self):
        """
        Tambahkan input untuk Uji Global di bawah tombol utama.
        """
        input_frame = tk.Frame(self.button_frame, bg="#15395b")
        input_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        tk.Label(input_frame, text="Jumlah Observasi (n):", bg="#15395b", fg="white").grid(row=0, column=0, sticky="w", padx=5)
        n_entry = tk.Entry(input_frame, width=10)
        n_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Jumlah Parameter (p):", bg="#15395b", fg="white").grid(row=1, column=0, sticky="w", padx=5)
        p_entry = tk.Entry(input_frame, width=10)
        p_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Button(
            input_frame,
            text="Lakukan Uji Global",
            command=lambda: self.uji_global(n_entry.get(), p_entry.get())
        ).grid(row=0, column=2, rowspan=2, padx=5, pady=2, sticky="ew")

    def select_database(self):
        # Select source database
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            self.selected_db_path.set(file_path)
            messagebox.showinfo("Information", f"Source database selected: {file_path}")

    def save_database_as(self):
        # Select destination database and trigger migration
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database files", "*.db")])
        if file_path:
            self.save_db_path.set(file_path)
            messagebox.showinfo("Information", f"Destination database set to: {file_path}")
            self.migrate_tables()  # Trigger migration after Save As
 
    def update_result_text(self, message):
        """
        Update the result text area with the given message.
        """
        try:
            self.result_text_combined.configure(state=tk.NORMAL)
            self.result_text_combined.delete("1.0", tk.END)
            self.result_text_combined.insert(tk.END, message)
            self.result_text_combined.configure(state=tk.DISABLED)
        except Exception as e:
            print(f"Error updating result text: {e}")

    def generate_rumus_and_validate(self):
        """Generate the formulas for distance and angles in radians and degrees."""
        db_path = self.selected_db_path.get()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        try:
            c.execute('SELECT STA, BS, Titik_Pantau, Rumus FROM Gabung_Data_T2_T4')
            rows = c.fetchall()
            
            distances = []
            angles_degree = []
            angles_seconds = []

            for row in rows:
                sta, bs, titik_pantau, rumus = row

                # Buat variabel yang akan digunakan
                xt = sp.symbols(f"x{titik_pantau.lower()}")
                yt = sp.symbols(f"y{titik_pantau.lower()}")
                xsta = sp.symbols(f"x{sta.lower()}")
                ysta = sp.symbols(f"y{sta.lower()}")
                xbs = sp.symbols(f"x{bs.lower()}")
                ybs = sp.symbols(f"y{bs.lower()}")

                # Rumus Jarak
                rumus_jarak = sp.sqrt((xt - xsta)**2 + (yt - ysta)**2)
                distances.append(rumus_jarak)

                # Rumus Sudut
                if rumus == "e1":
                    angle_degree = (sp.atan2(xt - xsta, yt - ysta) - sp.atan2(xbs - xsta, ybs - ysta)) * 180 / sp.pi
                elif rumus == "e2":
                    angle_degree = (sp.atan2(xbs - xsta, ybs - ysta) - sp.atan2(xt - xsta, yt - ysta)) * 180 / sp.pi
                elif rumus == "e3":
                    angle_degree = (sp.atan2(xbs - xsta, ybs - ysta)* 180 / sp.pi) + (360 - sp.atan2(xt - xsta, yt - ysta) * 180 / sp.pi)
                elif rumus == "e4":
                    angle_degree = (sp.atan2(xt - xsta, yt - ysta)* 180 / sp.pi) + (360 - sp.atan2(xbs - xsta, ybs - ysta) * 180 / sp.pi)
                else:
                    angle_degree = 0

                angles_degree.append(angle_degree)
                
                #Rumus sudut dalam detik
                if rumus == "e1":
                    angle_seconds = (sp.atan2(xt - xsta, yt - ysta) - sp.atan2(xbs - xsta, ybs - ysta)) * (180*3600) / sp.pi
                elif rumus == "e2":
                    angle_seconds = (sp.atan2(xbs - xsta, ybs - ysta) - sp.atan2(xt - xsta, yt - ysta)) * (180*3600) / sp.pi
                elif rumus == "e3":
                    angle_seconds = (sp.atan2(xbs - xsta, ybs - ysta)* (180*3600) / sp.pi) + (360 - sp.atan2(xt - xsta, yt - ysta) * (180*3600) / sp.pi)
                elif rumus == "e4":
                    angle_seconds = (sp.atan2(xt - xsta, yt - ysta)* (180*3600) / sp.pi) + (360 - sp.atan2(xbs - xsta, ybs - ysta) * (180*3600) / sp.pi)
                else:
                    angle_seconds = 0

                angles_seconds.append(angle_seconds)

            rumus_derajat = distances + angles_degree
            rumus_detik = distances + angles_seconds

            #self.update_result_text(f"Rumus Jarak dan Sudut:\n{np.array(rumus_derajat)}")
            # Menambahkan urutan nomor menggunakan enumerate
            rumus_dengan_nomor = "\n".join([f"{i+1}. {rumus}" for i, rumus in enumerate(rumus_detik)])

            # Menampilkan hasil
            self.update_result_text(f"Rumus Jarak dan Sudut:\n{rumus_dengan_nomor}")
            return rumus_derajat, rumus_detik
        finally:
            conn.close()

    def fetch_all_variables_from_db(self):
        """Fetch all symbolic variables from the database based on Titik_Pantau and STA."""
        db_path = self.selected_db_path.get()
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT stdev_x, stdev_y FROM Simpangan_Baku ORDER BY rowid")
        stdev_data = cur.fetchall()
        r = [value for pair in stdev_data for value in pair]
        
        try:
            # Ambil urutan dari tabel Gabung_Data_T2_T4 berdasarkan Titik_Pantau
            cur.execute("SELECT DISTINCT Titik_Pantau FROM Gabung_Data_T2_T4 ORDER BY rowid")
            titik_pantau = [row[0].lower() for row in cur.fetchall()]

            # Ambil urutan dari tabel Simpangan_Baku berdasarkan STA
            cur.execute("SELECT DISTINCT STA FROM Simpangan_Baku ORDER BY rowid")
            sta = [row[0].lower() for row in cur.fetchall()]

            # Buat simbol dengan prefiks 'x' dan 'y' berdasarkan urutan dari database
            all_variables_t2_t4 = sp.symbols(' '.join([f'x{point} y{point}' for point in titik_pantau]))
            all_variables_sta = sp.symbols(' '.join([f'x{point} y{point}' for point in sta]))

            # Gabungkan semua variabel dengan tetap mempertahankan urutan
            all_variables = all_variables_t2_t4 + all_variables_sta

            #simpan variabel simbolik untuk penggunaan berikutnya
            self.all_variables_t2_t4 = all_variables_t2_t4
            self.all_variables_sta = all_variables_sta
            self.all_variables = all_variables   

            for i in range(2):
                if r[i] == 0:
                    self.update_result_text(f"Semua variabel simbolik telah dibuat:\n{all_variables}\nBanyaknya Parameter Pantau :{len(all_variables_t2_t4)}")
                    #print(f"Nilai r[{i}] adalah 0. Menggunakan Metode Parameter.")
                else:
                    self.update_result_text(f"Semua variabel simbolik telah dibuat:\n{all_variables}\nBanyaknya Parameter Pantau :{len(all_variables)}")
                    #print(f"Nilai r[{i}] tidak 0. Menggunakan Metode Parameter Berbobot.")

            #self.update_result_text(f"Semua variabel simbolik telah dibuat:\n{all_variables}\nBanyaknya Parameter Pantau :{len(all_variables_t2_t4)}")
            return all_variables, all_variables_sta, all_variables_t2_t4
        finally:
            conn.close()

    def fetch_coordinate_values(self):
        """Fetch coordinate values dynamically from two different tables in the database."""
        db_path = self.selected_db_path.get()
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        try:
            # Ambil Titik_Pantau dari Koordinat_Pendekatan
            titik_t2_t4 = [row[0] for row in cur.execute("SELECT DISTINCT Titik_Pantau FROM Koordinat_Pendekatan").fetchall()]
            
            # Ambil STA dari Simpangan_Baku
            simpangan_baku_titik = [row[0] for row in cur.execute("SELECT DISTINCT STA FROM Simpangan_Baku").fetchall()]
            
            # Ambil koordinat dari Koordinat_Pendekatan
            koordinat_t2_t4 = []
            for titik in titik_t2_t4:
                x = cur.execute("SELECT X_Target FROM Koordinat_Pendekatan WHERE Titik_Pantau = ?", (titik,)).fetchone()
                y = cur.execute("SELECT Y_Target FROM Koordinat_Pendekatan WHERE Titik_Pantau = ?", (titik,)).fetchone()
                if x and y:  # Pastikan nilai tidak None
                    koordinat_t2_t4.append([float(x[0]), float(y[0])])

            # Ambil koordinat dari Simpangan_Baku
            koordinat_simpangan_baku = []
            for titik in simpangan_baku_titik:
                x = cur.execute("SELECT coord_x FROM Simpangan_Baku WHERE STA = ?", (titik,)).fetchone()
                y = cur.execute("SELECT coord_y FROM Simpangan_Baku WHERE STA = ?", (titik,)).fetchone()
                if x and y:  # Pastikan nilai tidak None
                    koordinat_simpangan_baku.append([float(x[0]), float(y[0])])

            # Gabungkan koordinat
            self.koordinat = np.array(koordinat_t2_t4 + koordinat_simpangan_baku, dtype=float)

            # Debug bentuk data
            print(f"Koordinat diambil dari database (Shape): {self.koordinat.shape}")
            print(f"Koordinat Data:\n{self.koordinat}")

            # Validasi bentuk koordinat
            if self.koordinat.ndim != 2 or self.koordinat.shape[1] != 2:
                raise ValueError("Koordinat awal harus berupa array 2D dengan pasangan x dan y.")

            # Flatten koordinat
            self.flattened_koordinat = self.koordinat.flatten()
            self.update_result_text(message=f"Array Koordinat:\n{self.koordinat}")

            return self.koordinat, self.flattened_koordinat

        finally:
            conn.close()

    def calculate_jacobian_matrix(self):
        """
        Calculate the Jacobian matrices A1 using symbolic differentiation
        and handle cases where the coordinate length is 38 or 58.
        """
        try:
            db_path = self.selected_db_path.get()
            conn = sqlite3.connect(db_path)
            curr = conn.cursor()

            curr.execute("SELECT stdev_x, stdev_y FROM Simpangan_Baku ORDER BY rowid")
            stdev_data = curr.fetchall()
            r = [value for pair in stdev_data for value in pair]

            # Pastikan koordinat sudah diinisialisasi
            if not hasattr(self, 'koordinat') or self.koordinat is None:
                raise ValueError("Koordinat belum diinisialisasi. Jalankan fetch_coordinate_values() terlebih dahulu.")

            # Ambil koordinat lengkap untuk digunakan dalam kondisi tertentu
            _, koordinat_lengkap = self.fetch_coordinate_values()

            # Variabel simbolik dan rumus
            all_variables, all_variables_sta, all_variables_t2_t4 = self.fetch_all_variables_from_db()
            _, rumus_detik = self.generate_rumus_and_validate()

            # Flatten koordinat
            flattened_koord = self.koordinat.flatten()

            # Deklarasi awal matriks
            A1, A2 = None, None

            for i in range(2):
                if r[i] == 0:
                    self.update_result_text(f"[{i}] Nilai simpangan baku koordinat adalah 0. Menggunakan Metode Parameter.")
                    #print(f"Nilai r[{i}] adalah 0. Menggunakan metode parameter.")

                    if len(flattened_koord) == len(all_variables_sta):
                        flattened_koord = np.concatenate(
                            [flattened_koord, koordinat_lengkap.flatten()[len(all_variables_t2_t4):]]
                        )

                    valid_variables = all_variables[:len(all_variables_t2_t4)]
                    valid_variables_ = all_variables[len(all_variables_t2_t4):]

                    f = sp.Matrix([sp.sympify(expr) for expr in rumus_detik])
                    g = sp.Matrix(valid_variables_)

                    JacobianMatrixSymbolic1 = f.jacobian(valid_variables)
                    JacobianMatrixSymbolic2 = g.jacobian(valid_variables_)

                    JacobianFunction1 = sp.lambdify(all_variables, JacobianMatrixSymbolic1, 'numpy')
                    JacobianFunction2 = sp.lambdify(all_variables_sta, JacobianMatrixSymbolic2, 'numpy')

                    A1 = np.array(JacobianFunction1(*flattened_koord), dtype=float)
                    A2 = np.array(JacobianFunction2(*koordinat_lengkap.flatten()[len(all_variables_t2_t4):]), dtype=float)
                    # Tampilkan hasil
                    result = f"Matriks A1:\n{A1}"
                    self.update_result_text(result)
                    print(result)
                else:
                    print(f"Nilai r[{i}] adalah {r[i]}. Menggunakan Metode Parameter Berbobot.")

                    valid_coordinates = [val for val in flattened_koord if val is not None]
                    valid_variables = all_variables
                    valid_variables_ = all_variables_sta

                    f = sp.Matrix([sp.sympify(expr) for expr in rumus_detik])
                    g = sp.Matrix(valid_variables_)

                    JacobianMatrixSymbolic1 = f.jacobian(valid_variables)
                    JacobianMatrixSymbolic2 = g.jacobian(valid_variables_)

                    JacobianFunction1 = sp.lambdify(valid_variables, JacobianMatrixSymbolic1, 'numpy')
                    JacobianFunction2 = sp.lambdify(valid_variables_, JacobianMatrixSymbolic2, 'numpy')

                    A1 = np.array(JacobianFunction1(*valid_coordinates), dtype=float)
                    A2 = np.array(JacobianFunction2(*valid_coordinates), dtype=float)
                    # Tampilkan hasil
                    result = f"Matriks A1:\n{A1}\n\nMatriks A2:\n{A2}"
                    self.update_result_text(result)
                    print(result)
            

            return A1, A2

        except Exception as e:
            error_message = f"Error in calculate_jacobian_matrix: {e}"
            print(error_message)
            self.update_result_text(error_message)
            return None, None
  
    def initialize_koordinat_dict(self):
        """Initialize or update koordinat_dict using the latest values in self.koordinat."""
        # Pastikan koordinat sudah diinisialisasi
        if not hasattr(self, 'koordinat') or self.koordinat is None:
            raise ValueError("Koordinat belum diinisialisasi. Jalankan least_squares atau set koordinat terlebih dahulu.")
        
        # Ambil variabel simbolik
        all_variables, _, _ = self.fetch_all_variables_from_db()
        
        # Perbarui koordinat_dict berdasarkan koordinat terbaru
        self.koordinat_dict = {
            str(var): float(self.koordinat.flatten()[idx])  # Gunakan koordinat terbaru
            for idx, var in enumerate(all_variables)
        }
        
        print(f"Koordinat Dictionary (Diperbarui): {self.koordinat_dict}")  # Debugging
        return self.koordinat_dict

    def normalize_angle(self, angle):
        """Pastikan sudut berada di dalam rentang 0-180"""
        if angle is None or np.isnan(angle):
            print(f"Angle {angle} is None or NaN.")
            return None

        angle = angle % 360  # Ubah sudut ke rentang 0-360
        if 0 <= angle <= 180:  # Jika sudah di rentang 0-180, biarkan
            return angle
        elif angle > 180:  # Jika lebih dari 180, normalisasi
            angle = 360 - angle
        return angle

    def calculate_distance(self):
        """Calculate the distances using the provided rumus_derajat."""
        # Pastikan koordinat_dict telah diperbarui
        self.initialize_koordinat_dict()
        
        self.distances = []
        print(f"Evaluating distances with koordinat_dict: {self.koordinat_dict}")
        
        for rumus in self.rumus_derajat:
            if "**2" in str(rumus):  # Hanya rumus yang memiliki kuadrat
                try:
                    # Evaluasi rumus menggunakan koordinat_dict
                    result = eval(str(rumus), {"math": math, "sqrt": math.sqrt}, self.koordinat_dict)
                    self.distances.append(result)
                    print(f"Evaluated distance for {rumus}: {result}")
                except Exception as e:
                    print(f"Error in distance formula: {rumus} - {e}")
        
        if not self.distances:
            print("Tidak ada jarak yang berhasil dihitung.")
        else:
            print(f"Calculated Distances: {self.distances}")
        
        return self.distances

    def calculate_angles(self):
        """Calculate the angles using the provided rumus_derajat."""
        # Pastikan koordinat_dict telah diperbarui
        self.initialize_koordinat_dict()
        
        self.angles = []  # Reset list of angles
        print(f"Evaluating angles with koordinat_dict: {self.koordinat_dict}")
        
        for idx, rumus in enumerate(self.rumus_derajat):
            if rumus.has(sp.atan2):  # Periksa apakah rumus memiliki atan2
                try:
                    # Lambdify untuk evaluasi
                    rumus_func = sp.lambdify(list(self.koordinat_dict.keys()), rumus, modules=["numpy"])
                    result = rumus_func(**self.koordinat_dict)
                    
                    print(f"Rumus ke-{idx}: {rumus}")
                    print(f"Hasil evaluasi dari rumus {rumus}: {result}")
                    
                    if result is None or np.isnan(result):
                        print(f"Error: result ({result}) adalah None atau NaN.")
                        continue
                    
                    # Normalisasi sudut
                    result = self.normalize_angle(result)
                    self.angles.append(result)
                    print(f"Calculated Angle [{idx}]: {result}")
                except Exception as e:
                    print(f"Error in angle formula ({idx}): {rumus} - {e}")
        
        if not self.angles:
            print("Tidak ada sudut yang berhasil dihitung.")
        else:
            print(f"Jumlah sudut yang dihitung: {len(self.angles)}")
        
        return self.angles

    def matrix_L1(self):
        """Combine distances and angles into the L1 matrix."""
        # Pastikan koordinat_dict diperbarui sebelum menghitung
        self.initialize_koordinat_dict()
        
        # Ambil rumus derajat
        self.rumus_derajat, _ = self.generate_rumus_and_validate()
        
        # Hitung jarak dan sudut
        self.distances = self.calculate_distance()
        result_angles = self.calculate_angles()  # Pastikan result_angles adalah list
        
        # Gabungkan distances dan angles ke dalam matriks L1
        try:
            L1 = np.array(self.distances + result_angles)  # Menggabungkan list distances dan result_angles
        except Exception as e:
            print(f"Error creating L1 matrix: {e}")
            L1 = None
        
        # Cetak matriks L1 secara rapi
        if L1 is not None:
            L1_str = "\n".join([f"{value:.4f}" for value in L1])  # Format ke baris baru dengan 4 desimal
            print(f"Matriks L1 (len: {len(L1)}):\n{L1_str}")
            self.update_result_text(f"Matriks L1:\n{L1_str}")
        
        return L1

    def matrix_L01(self):
        """Create matrix L01 by extracting Jarak_P and Sudut from the database."""
        db_path = self.selected_db_path.get()
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try:
            cur.execute("SELECT Jarak_P FROM Gabung_Data_T2_T4")
            rows = cur.fetchall()

            cur.execute("SELECT Sudut FROM Gabung_Data_T2_T4")
            rowz = cur.fetchall()    

            array_jarak = np.array([row[0] for row in rows])
            array_sudut = np.array([row[0] for row in rowz])

            L01 = np.concatenate((array_jarak, array_sudut))
            
            # Cetak matriks L01 secara rapi
            L01_str = "\n".join([f"{value:.4f}" for value in L01])  # Format ke baris baru dengan 4 desimal
            print(f"Matriks L01 (len: {len(L01)}):\n{L01_str}")
            self.update_result_text(f"Matriks L01:\n{L01_str}")
            
            return L01
        finally:
            conn.close()

    def matrix_F1(self):
        """
        Calculate matrix F1 as the difference between L1 and L01.
        """
        # Pastikan L1 dan L01 dihitung dengan data terbaru
        self.L1 = self.matrix_L1()  # Menggunakan data terbaru untuk L1
        self.L01 = self.matrix_L01()  # Menggunakan data terbaru untuk L01

        # Periksa apakah panjang L1 dan L01 sama
        if len(self.L01) != len(self.L1):
            # Beri peringatan jika panjangnya berbeda
            error_message = (
                f"List memiliki panjang yang berbeda! Tidak dapat menghitung matriks F1.\n"
                f"Panjang L1: {len(self.L1)}, Panjang L01: {len(self.L01)}"
            )
            print(error_message)
            self.update_result_text(error_message)
            return None  # Kembalikan None jika panjang tidak sama

        # Hitung perbedaan L1 dan L01
        F1_ = [l1 - l01 for l01, l1 in zip(self.L01, self.L1)]
        F1 = np.array(F1_).reshape(-1, 1)  # Konversi F1 ke vektor kolom
        self.update_result_text(f"Matriks F1:\n{F1}")
        return F1

    def matrix_L2(self):
        """Calculate the L2 matrix and display the results."""
        # Ambil path dari database yang dipilih
        db_path = self.selected_db_path.get()
        if not db_path:
            self.update_result_text("Database belum dipilih!", result_number=8)
            return

        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Query to get the STA order from Simpangan_Baku
            query_order = """
            SELECT STA
            FROM Simpangan_Baku;
            """
            cursor.execute(query_order)
            sta_order = [row[0] for row in cursor.fetchall()]

            # Dictionary to store recalculated coordinates
            recalculated_coordinates = {}

            # Query data where unique values are in the STA column
            query_sta = """
            SELECT g.STA, g.BS, g.Jarak_I, s.coord_x AS x_sta, s.coord_y AS y_sta, b.coord_x AS x_bs, b.coord_y AS y_bs
            FROM Gabung_Data_T2_T4 g
            JOIN Simpangan_Baku s ON g.STA = s.STA
            JOIN Simpangan_Baku b ON g.BS = b.STA;
            """
            cursor.execute(query_sta)
            data_sta = cursor.fetchall()

            # Process STA data
            for sta, bs, jarak_i, x_sta, y_sta, x_bs, y_bs in data_sta:
                if jarak_i > 0:  # Only recalculate for non-zero distances
                    azimuth = math.atan2(x_bs - x_sta, y_bs - y_sta)
                    x_recalculated = x_sta + jarak_i * math.sin(azimuth)
                    y_recalculated = y_sta + jarak_i * math.cos(azimuth)
                    recalculated_coordinates[bs] = (x_recalculated, y_recalculated)

            # Query data where unique values are in the BS column
            query_bs = """
            SELECT g.BS, g.STA, g.Jarak_I, s.coord_x AS x_bs, s.coord_y AS y_bs, b.coord_x AS x_sta, b.coord_y AS y_sta
            FROM Gabung_Data_T2_T4 g
            JOIN Simpangan_Baku s ON g.BS = s.STA
            JOIN Simpangan_Baku b ON g.STA = b.STA;
            """
            cursor.execute(query_bs)
            data_bs = cursor.fetchall()

            # Process BS data
            for bs, sta, jarak_i, x_bs, y_bs, x_sta, y_sta in data_bs:
                if jarak_i > 0:  # Only recalculate for non-zero distances
                    azimuth = math.atan2(x_sta - x_bs, y_sta - y_bs)
                    x_recalculated = x_bs + jarak_i * math.sin(azimuth)
                    y_recalculated = y_bs + jarak_i * math.cos(azimuth)
                    recalculated_coordinates[sta] = (x_recalculated, y_recalculated)

            # Print recalculated coordinates in the order of STA from Simpangan_Baku
            result_text = "=" * 60 + "\n"
            result_text += "Koordinat Pendekatan Stasiun (L2):\n"
            for sta in sta_order:
                if sta in recalculated_coordinates:
                    x, y = recalculated_coordinates[sta]
                    result_text += f"Koordinat: {sta:<10} x': {x:>15.6f}  y': {y:>15.6f}\n"
            result_text += "=" * 60

            self.update_result_text(result_text)

            # Prepare recalculated coordinates as list array
            L2 = []
            for sta in sta_order:
                if sta in recalculated_coordinates:
                    x, y = recalculated_coordinates[sta]
                    L2.extend([x, y])

            print(f"L2 Array (len: {len(L2)}): {L2}")  # Debugging
            self.update_result_text(f"L2 Array (len: {len(L2)}):\n{L2}")
            return L2

        except Exception as e:
            self.update_result_text(f"Terjadi kesalahan saat menghitung L2: {e}")
        
        finally:
            # Close the database connection
            conn.close()

    def matrix_L02(self):
        """Create matrix L02 using coordinates from Simpangan_Baku table."""
        db_path = self.selected_db_path.get()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            query = "SELECT STA, coord_x, coord_y FROM Simpangan_Baku ORDER BY rowid;"
            cursor.execute(query)
            simpangan_baku_data = cursor.fetchall()

            ordered_coordinates = [(row[0], row[1], row[2]) for row in simpangan_baku_data]
            L02 = [value for row in ordered_coordinates for value in row[1:]]
            
            self.update_result_text(f"L02 matrix:\n{L02}")
            return L02
        finally:
            conn.close()

    def matrix_F2(self):
        """Calculate matrix F2 as the difference between L2 and L02."""
        self.L2 = self.matrix_L2()
        self.L02 = self.matrix_L02()
        F2 = None
        if len(self.L02) == len(self.L2):
            F2_ = [l2 - l02 for l02, l2 in zip(self.L02, self.L2)]
            F2 = np.array(F2_).reshape(-1, 1)  # Convert F2 to a column vector
            self.update_result_text(f"Matriks F2:\n{F2}")
        else:
            self.update_result_text("List memiliki panjang yang berbeda!")
        return F2

    def calculate_variances_and_matrices(self):
        """Calculate the variances and form matrices P1 and P2."""
        db_path = self.selected_db_path.get()
        conn = sqlite3.connect(db_path)
        curr = conn.cursor()

        try:
            # Ambil data dari database
            curr.execute("SELECT Jarak_P FROM Gabung_Data_T2_T4 ORDER BY rowid")
            jarak_p = [row[0] for row in curr.fetchall()]

            curr.execute("SELECT Jarak_I FROM Gabung_Data_T2_T4 ORDER BY rowid")
            jarak_i = [row[0] for row in curr.fetchall()]

            curr.execute("SELECT Sudut FROM Gabung_Data_T2_T4 ORDER BY rowid")
            sudut = [row[0] for row in curr.fetchall()]

            curr.execute("SELECT stdev_x, stdev_y FROM Simpangan_Baku ORDER BY rowid")
            stdev_data = curr.fetchall()
            r = [value for pair in stdev_data for value in pair]

            # Variabel konstanta
            c1, c2, c3, sigt = 0.001, 0.001, 0.001, 0.001
            m, d, b, a = 30, 1, 2, 2

            # Hitung v1 untuk semua jarak_p
            v1 = np.array([(a**2 + (b**2 * (jarak / 1000)**2)) for jarak in jarak_p])

            # Hitung v2 berdasarkan sudut
            v2 = np.zeros(len(sudut))
            for i in range(len(sudut)):
                Bc = ((c1**2 / jarak_p[i]**2) + (c2**2 / jarak_i[i]**2) + 
                    (c3**2 / (jarak_p[i]**2 * jarak_i[i]**2)) * 
                    ((jarak_p[i]**2 + jarak_i[i]**2 - 2 * jarak_p[i]**2 * jarak_i[i]**2 * np.cos(np.radians(sudut[i]))))) 
                Br = (3 * d)**2 / (2 * 4**2)
                Bp = (60 / m)**2 / 4
                Bt = (jarak_p[i]**2 + jarak_i[i]**2) / (jarak_p[i]**2 * jarak_i[i]**2) * sigt**2 
                v2[i] = ((Bc) + (Br) + (Bp) + (Bt))
            
            # Gabungkan v1 dan v2 menjadi V
            V = np.concatenate((v1, v2))

            # Buat matriks P1
            w = len(jarak_p) + len(v2)
            P1 = np.zeros((w, w))
            for i in range(w):
                P1[i, i] = 1 / V[i]

            # Buat matriks P2
            rl = len(r)
            P2 = np.zeros((rl, rl))
            for i in range(rl):
                if r[i] == 0:
                    P2[i, i] = r[i]**2/1
                else:
                    P2[i, i] = 1 / r[i]**2


            # Ambil diagonal dari P1 dan P2, dan tampilkan dengan format rapi
            diagonal_P1 = np.diagonal(P1)
            diagonal_P2 = np.diagonal(P2)

            # Format hasil ke dalam string
            diagonal_P1_str = "\n".join([f"{value:.6f}" for value in diagonal_P1])
            diagonal_P2_str = "\n".join([f"{value:.6f}" for value in diagonal_P2])

            # Tampilkan hasil diagonal
            self.update_result_text(f"Matriks Diagonal P1:\n{diagonal_P1_str}\n\nMatriks Diagonal P2:\n{diagonal_P2_str}")

            return P1, P2, w
        finally:
            conn.close()

    def delta_x(self):
        """
        Hitung delta X untuk memperbarui koordinat di memori.
        Returns:
            delta_X (numpy.ndarray): Perubahan koordinat.
            koordinat_baru (numpy.ndarray): Koordinat yang telah diperbarui.
        """
        try:
            db_path = self.selected_db_path.get()
            conn = sqlite3.connect(db_path)
            curr = conn.cursor()

            curr.execute("SELECT stdev_x, stdev_y FROM Simpangan_Baku ORDER BY rowid")
            stdev_data = curr.fetchall()
            r = [value for pair in stdev_data for value in pair]

            # Pastikan self.koordinat sudah diinisialisasi
            if not hasattr(self, 'koordinat') or self.koordinat is None:
                raise ValueError("Koordinat belum diinisialisasi. Jalankan least_squares() terlebih dahulu.")

            # Ambil koordinat yang relevan (hanya 19 pasangan koordinat pertama)
            koordinat_relevan = self.koordinat[:19, :]  # Hanya ambil 19 pasangan koordinat
            print(f"Koordinat relevan untuk perhitungan: {koordinat_relevan.shape}")

            # Hitung matriks Jacobian
            jacobian_result = self.calculate_jacobian_matrix()
            if jacobian_result is None or not isinstance(jacobian_result, tuple) or len(jacobian_result) != 2:
                raise ValueError("Matriks Jacobian tidak valid. Pastikan calculate_jacobian_matrix() menghasilkan A1 dan A2.")
            self.A1, self.A2 = jacobian_result  # Pisahkan A1 dan A2 dari hasil

            # Hitung matriks varians dan matriks P
            self.P1, self.P2, _ = self.calculate_variances_and_matrices()

            # Hitung matriks residual F1
            self.F1 = self.matrix_F1()

            # Debugging dimensi
            print(f"Dimensi A1: {self.A1.shape}")
            print(f"Dimensi P1: {self.P1.shape}")
            print(f"Dimensi F1: {self.F1.shape}")
            for i in range(len(r)):
                if r[i] == 0:
                    # Jika P2 Tidak Valid
                    print("P2 tidak valid, mengandung nilai kosong atau infinite. Menggunakan hanya A1, P1, dan F1.")

                    # Hitung delta_X
                    X = -np.linalg.pinv(
                        np.transpose(self.A1) @ self.P1 @ self.A1
                    ) @ (
                        np.transpose(self.A1) @ self.P1 @ self.F1
                    )
                else:
                    # Jika P2 valid
                    print("P2 valid. Menggunakan A1, P1, F1, serta A2, P2, F2.")
                    self.F2 = self.matrix_F2()  # Pastikan F2 dihitung jika diperlukan
                    X = -np.linalg.pinv(
                        np.transpose(self.A1) @ self.P1 @ self.A1 +
                        np.transpose(self.A2) @ self.P2 @ self.A2
                    ) @ (
                        np.transpose(self.A1) @ self.P1 @ self.F1 +
                        np.transpose(self.A2) @ self.P2 @ self.F2
                    )

            # Bentuk ulang delta_X menjadi matriks koordinat 2 kolom
            delta_X = X.reshape(-1, 2)

            # Validasi dimensi delta_X
            if delta_X.shape != koordinat_relevan.shape:
                raise ValueError(f"Dimensi delta_X ({delta_X.shape}) tidak cocok dengan koordinat relevan ({koordinat_relevan.shape})")

            # Perbarui koordinat menggunakan delta_X
            koordinat_baru = koordinat_relevan + delta_X

            # Tampilkan hasil
            message = f"delta_X berhasil dihitung:\n{delta_X}\n\nKoordinat baru:\n{koordinat_baru}"
            self.update_result_text(message)

            return delta_X, koordinat_baru

        except Exception as e:
            error_message = f"Error during delta_X calculation: {e}"
            print(error_message)
            self.update_result_text(error_message)
            raise

    def least_squares(self, iterasi_max=1, toleransi=1e-3):
        """
        Jalankan perataan kuadrat terkecil (least squares) dengan iterasi.
        """
        try:
            # Pastikan koordinat diinisialisasi jika belum ada
            if not hasattr(self, 'koordinat') or self.koordinat is None:
                self.koordinat, _ = self.fetch_coordinate_values()

            iterasi_aktual = 0
            for iterasi in range(iterasi_max):
                iterasi_aktual = iterasi + 1
                print(f"=== Iterasi {iterasi_aktual} ===")

                # Perbarui matriks Jacobian, matriks F1/F2, dan matriks varians
                self.A1 = self.calculate_jacobian_matrix()
                self.F1 = self.matrix_F1()

                # Hitung delta_X menggunakan koordinat dan matriks terbaru
                delta_X, koordinat_baru = self.delta_x()

                # Perhitungan perubahan
                perubahan = np.linalg.norm(delta_X)
                print(f"Perubahan pada iterasi {iterasi_aktual}: {perubahan:.6f}")

                # Perbarui koordinat untuk iterasi berikutnya
                self.koordinat = koordinat_baru

                # Periksa konvergensi
                if perubahan < toleransi:
                    print(f"Konvergensi tercapai pada iterasi {iterasi_aktual}.")
                    break

            # Tampilkan hasil iterasi terakhir
            result_message = f"=== Hasil Iterasi {iterasi_aktual} ===\n"
            for i, (x, y) in enumerate(self.koordinat):
                result_message += f"Titik {i + 1}: x = {x}, y = {y}\n"

            self.update_result_text(result_message)

            return self.koordinat

        except Exception as e:
            error_message = f"Terjadi kesalahan dalam least_squares: {e}"
            print(error_message)
            self.update_result_text(error_message)
            raise

    def request_global_test_input(self):
        """
        Menampilkan input untuk uji global di bawah tombol utama.
        """
        try:
            # Hapus teks sebelumnya di result_text_combined
            self.update_result_text("")

            # Tambahkan instruksi ke area hasil
            self.update_result_text("Masukkan parameter untuk Uji Global:\n")

            # Tambahkan Frame untuk input di bawah tombol
            input_frame = tk.Frame(self.button_frame, bg="#15395b")
            input_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            # Label dan Entry untuk input 'Jumlah Observasi (n)'
            tk.Label(input_frame, text="Jumlah Observasi (n):", bg="#15395b", fg="white").grid(row=0, column=0, sticky="w", padx=5)
            n_entry = tk.Entry(input_frame, width=10)
            n_entry.grid(row=0, column=1, padx=5, pady=2)

            # Label dan Entry untuk input 'Jumlah Parameter (p)'
            tk.Label(input_frame, text="Jumlah Parameter (p):", bg="#15395b", fg="white").grid(row=1, column=0, sticky="w", padx=5)
            p_entry = tk.Entry(input_frame, width=10)
            p_entry.grid(row=1, column=1, padx=5, pady=2)

            # Tombol konfirmasi
            confirm_button = ttk.Button(
                input_frame,
                text="Lakukan Uji Global",
                command=lambda: self.uji_global(n_entry.get(), p_entry.get())
            )
            confirm_button.grid(row=0, column=2, rowspan=2, padx=5, pady=2, sticky="ew")

        except Exception as e:
            error_message = f"Terjadi kesalahan: {e}"
            print(error_message)
            self.update_result_text(error_message)

    def calculate_vtpv(self, A1, X_, residuals_F1, P1):
        """
        Menghitung VTPV menggunakan matriks A1, residuals_F1, dan P1.
        """
        try:
            # Validasi dimensi
            if A1.shape[0] != residuals_F1.shape[0]:
                raise ValueError(f"Dimensi A1 ({A1.shape}) tidak cocok dengan residuals_F1 ({residuals_F1.shape})")

            # Hitung v1 dan VTPV
            v1 = A1 @ X_ + residuals_F1.reshape(-1, 1)
            vtpv = (v1.T @ P1 @ v1).item()  # Hasil skalar

            return vtpv

        except Exception as e:
            print(f"Terjadi kesalahan dalam perhitungan VTPV: {e}")
            raise

    def uji_global(self, n, p):
        """
        Melakukan uji global berdasarkan input pengguna.
        """
        try:
            # Validasi input
            n, p = int(n), int(p)
            if n <= p:
                raise ValueError("Jumlah observasi (n) harus lebih besar dari jumlah parameter (p).")

            t = n - p  # Degrees of Freedom

            # Hitung residuals dan matriks
            residuals_F1 = self.F1.flatten()
            jacobian_result = self.calculate_jacobian_matrix()
            if jacobian_result is None or not isinstance(jacobian_result, tuple) or len(jacobian_result) != 2:
                raise ValueError("Matriks Jacobian tidak valid. Pastikan calculate_jacobian_matrix() menghasilkan A1 dan A2.")
            A1, A2 = jacobian_result  # Pisahkan A1 dan A2 dari hasil

            if A1.shape[0] != residuals_F1.shape[0]:
                raise ValueError(f"Dimensi A1 ({A1.shape}) tidak cocok dengan residuals_F1 ({residuals_F1.shape})")

            # Ambil delta_X
            delta_X = self.delta_x()[0].reshape(-1, 2)  # Bentuk ulang menjadi pasangan x, y

            # Ambil hanya 19 pasangan koordinat utama dari self.koordinat
            koordinat_utama = self.koordinat[:19]  # Pastikan hanya mengambil 19 pasangan koordinat
            if koordinat_utama.shape != delta_X.shape:
                raise ValueError(
                    f"Dimensi delta_X ({delta_X.shape}) tidak cocok dengan koordinat utama ({koordinat_utama.shape}). "
                    "Pastikan delta_X dan koordinat utama memiliki dimensi yang sama."
                )

            # Hitung koordinat baru
            koordinat_baru = koordinat_utama + delta_X

            # Hitung VTPV
            X_ = delta_X.flatten().reshape(-1, 1)
            vtpv_scalar = self.calculate_vtpv(A1, X_, residuals_F1, self.P1)

            # Nilai Aposteriori
            sigma_apost2 = vtpv_scalar / t
            R = sigma_apost2 / 1  # Apriori diasumsikan 1

            # Fisher Threshold
            fisher_threshold = 1.40483
            lolos_uji_global = R <= fisher_threshold

            # Hitung simpangan baku (stdev)
            sigxx = sigma_apost2 * np.linalg.pinv(np.transpose(A1) @ self.P1 @ A1)
            diag_sigxx = np.copy(np.diag(sigxx))
            diag_sigxx[diag_sigxx < 0] = 0  # Set elemen negatif menjadi nol
            stdev = np.sqrt(diag_sigxx) * 1000  # Dalam milimeter

            # Ambil nama variabel
            variable_names, _, _ = self.fetch_all_variables_from_db()
            variable_names = variable_names[:38]  # Ambil hanya untuk 19 pasangan x, y

            # Format koordinat baru dan simpangan baku hanya untuk 19 pasangan koordinat utama
            formatted_data = "\n".join(
                f"{x_name}: {new_coord[0]:+.6f}, σ:(±{stdev[2*i]:.3f} mm)"
                f"  {y_name}: {new_coord[1]:+.6f}, σ:(±{stdev[2*i+1]:.3f} mm)"
                for i, ((x_name, y_name), new_coord) in enumerate(
                    zip(zip(variable_names[::2], variable_names[1::2]), koordinat_baru)
                )
            )

            # Format hasil
            result = f"Hasil Uji Global:\n"
            result += f"Derajat Kebebasan (t): {t}\n"
            result += f"R = (VTPV / DOF) = {sigma_apost2:.6f}\n"
            result += f"Fisher Threshold = {fisher_threshold}\n"
            result += "Hasil: " + ("Lolos Uji Global" if lolos_uji_global else "Tidak Lolos Uji Global")
            result += f"\n\nKoordinat Baru dan Simpangan Baku:\n{formatted_data}\n"

            # Tampilkan hasil
            self.update_result_text(result)
            print(result)

            return R, lolos_uji_global

        except Exception as e:
            error_message = f"Error in uji_global: {e}"
            print(error_message)
            self.update_result_text(error_message)
            raise

  # "Back" button functionality
    def kembali_to_awal(self):
        self.label_frame.destroy()  
        new_window1()

    def data_snooping_test(self):
        """
        Melakukan uji data snooping untuk mendeteksi kesalahan tak acak pada residu.
        """
        try:
            # Pastikan uji global telah dilakukan untuk mendapatkan sigma apost dan stdev
            if not hasattr(self, "F1") or not hasattr(self, "F2"):
                raise ValueError("Residuals F1 dan F2 belum dihitung. Lakukan uji global terlebih dahulu.")

            if not hasattr(self, "stdev"):
                raise ValueError("Simpangan baku (stdev) belum tersedia. Pastikan uji global selesai.")

            # Hitung delta_X untuk mendapatkan residuals (residu = delta_X)
            delta_X, koordinat_baru = self.delta_x()

            # Flatten delta_X menjadi vektor 1D untuk pengujian
            residuals = delta_X.flatten()

            # Variansi dihitung dari simpangan baku (stdev)
            variances = self.stdev**2  # Kuadratkan stdev untuk mendapatkan variansi

            # Validasi dimensi residuals dan variances
            if len(residuals) != len(variances):
                raise ValueError(
                    f"Dimensi residu (delta_X: {len(residuals)}) tidak cocok dengan variansi ({len(variances)})"
                )

            # Fisher Threshold
            fisher_threshold = 1.40483  # Threshold berdasarkan tingkat signifikansi

            # Lakukan pengujian untuk setiap residu
            hasil_uji = []
            for i, (vi, sigma_vi) in enumerate(zip(residuals, np.sqrt(variances))):
                if sigma_vi != 0:  # Pastikan sigma_vi tidak nol
                    nilai_uji = abs(vi / sigma_vi)  # Hitung statistik uji
                    lolos = nilai_uji <= fisher_threshold
                    hasil_uji.append((i + 1, vi, sigma_vi, nilai_uji, lolos))

            # Format hasil
            hasil_string = "Hasil Data Snooping:\n"
            for idx, vi, sigma_vi, nilai_uji, lolos in hasil_uji:
                status = "Lolos" if lolos else "Tidak Lolos"
                hasil_string += f"Residu ke-{idx}: |{vi:.4f} / {sigma_vi:.4f}| = {nilai_uji:.4f} ({status})\n"

            # Tampilkan hasil
            self.update_result_text(hasil_string)
            print(hasil_string)

            return hasil_uji

        except Exception as e:
            error_message = f"Terjadi kesalahan dalam data snooping: {e}"
            print(error_message)
            self.update_result_text(error_message)

new_window1()
win.mainloop()



