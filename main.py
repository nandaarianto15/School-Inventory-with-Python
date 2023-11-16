# Library prettytable yang digunakan untuk membuat / mengeluarkan data dalam bentuk tabel.
from prettytable import PrettyTable

# Library tinyDB sebagai Database atau media storage untuk menyimpan data.
from tinydb import TinyDB, Query

# Library untuk mendapatkan data tanggal dan waktu
import datetime

#Library untuk menyembunyikan password
import getpass

#library random
import random

# Library OS digunakan untuk berinteraksi dengan sistem operasi.
from os import system, name

# Menginisialisasi library TinyDB untuk menyimpan data user ke dalam file JSON "user.json".
db_user = TinyDB("json/user.json")

# Menginisialisasi library TinyDB untuk menyimpan data barang ke dalam file JSON "barang.json".
db_barang = TinyDB("json/barang.json")

# Menginisialisasi library TinyDB untuk meminjam barang ke dalam file JSON "pinjam.json".
db_pinjam = TinyDB("json/pinjam.json")

# Akun admin
admin = "admin"
adminPass = "admin123"


# Ini adalah fungsi untuk memilih menu login, register, maupun exit
def chooseLogin():
    table = PrettyTable()
    header = ["No", "SELAMAT DATANG di SCHOOL INVENTORY"]
    table.field_names = header
    table.align = "l"
    table.add_row([1, "Login"])
    table.add_row([2, "Register"])
    table.add_row([3, "Exit"])
    print(table)

    pilih = input("Masukkan pilihan menu anda : ")
    if pilih.isnumeric():
        pilih_int = int(pilih)
        if 1 <= pilih_int <= 3:
            if pilih_int == 1:
                login()
            elif pilih_int == 2:
                register()
            elif pilih_int == 3:
                system("cls")
                exit()
        else:
            system("cls")
            print("="*43)
            print("             Pilihan tidak ada")
            print("="*43)
    elif pilih == "" or not pilih.strip():
        system("cls")
        print("="*43)
        print("         Input tidak boleh kosong")
        print("="*43)
    else:
        system("cls")
        print("="*43)
        print("Input invalid. Masukkan hanya angka integer")
        print("="*43)


# Ini adalah fungsi untuk register
def register():
    data = {}

    for d in db_user.all():
        for key, value in d.items():
            data[key] = value

    while True:
        username = input("Masukkan username anda : ")
        if username == "" or not username.strip():
            system("cls")
            print("="*33)
            print("Input username tidak boleh kosong")
            print("="*33)
        elif username in data:
            system("cls")
            print("=" * 45)
            print("Username sudah digunakan. Pilih Username lain")
            print("=" * 45)
        else:
            password = getpass.getpass("Masukkan password anda : ")
            if password == "" or not password.strip():
                system("cls")
                print("="*33)
                print("Input password tidak boleh kosong")
                print("="*33)
                continue
            else:
                print("test")
                db_user.insert({username: password})
                system("cls")
                print("=" * 43)
                print("            Akun berhasil dibuat.")
                print("=" * 43)
                break


# Ini adalh fungsi untuk login
def login():
    data = db_user.all()
    username = input("Masukkan username anda : ")
    if username == "" or not username.strip():
        system("cls")
        print("="*33)
        print("Input username tidak boleh kosong")
        print("="*33)
        
    password = getpass.getpass("Masukkan password anda : ")
    if password == "" or not password.strip():
        system("cls")
        print("="*33)
        print("Input password tidak boleh kosong")
        print("="*33)
    
    if username == admin and password == adminPass:
        system("cls")
        menu_admin()
    else:
        for a in data:
            if username in a and password == a[username]:
                system("cls")
                menu_user()


#Ini adalah fungsi untuk pinjam barang
def pinjam_barang():
    system("cls")
    data = {}
    for d in db_pinjam.all():
        for key, value in d.items():
            data[key] = value
    
    while True:
        show_barang_inventory()
        uuid_barang = input("Masukkan uuid barang : ")
        
        data_user = db_user.all()
        username = input("Masukkan username anda : ")
        for a in data_user:
            if username in a:
                if uuid_barang.isnumeric():
                    uuid_barang_int = int(uuid_barang)
                    data_query = Query()
                    if any(d["uuid"] == uuid_barang_int for d in db_barang.all()):    
                        
                        get_value = db_barang.get(data_query.uuid == uuid_barang_int)['jumlah']
                        new_value = get_value - 1

                        db_barang.update({"jumlah": new_value}, data_query.uuid == uuid_barang_int)
                        db_barang.all()
                        
                        data = db_barang.all()
                        for i in range(0, len(data)):
                            nama = data[i]["nama"]
                            jenis = data[i]["jenis"]
                            kondisi = data[i]["kondisi"]
                            uuid = data[i]["uuid"]

                        masuk = str(datetime.date.today())
                        
                        if any(d["peminjam"] == username for d in db_pinjam.all()):    

                            get_value = db_pinjam.get(data_query.peminjam == username)['jumlah']
                            new_value = get_value + 1
                            db_pinjam.update({"jumlah": new_value}, data_query.peminjam == username)
                            db_pinjam.all()
                            system("cls")
                            print("=" * 41)
                            print("   Barang berhasil di pinjam.")
                            print("=" * 41)
                            break
                        else:
                            db_pinjam.insert(
                                {
                                    "uuid": uuid, 
                                    "peminjam": username,   
                                    "nama": nama,
                                    "jenis": jenis,
                                    "jumlah": 1,
                                    "kondisi": kondisi,
                                    "masuk": masuk
                                }
                            )
                            
                            system("cls")
                            print("=" * 23)
                            print("Data berhasil di pinjam")
                            print("=" * 23)
                            break
                        
                    else:
                        system("cls")
                        print("=" * 23)
                        print("    UUID Tidak ada.")
                        print("=" * 23)
                    
                elif uuid_barang == "" or not uuid_barang.strip():
                    system("cls")
                    print("="*42)
                    print("        Input tidak boleh kosong")
                    print("="*42)
                    continue
                else:
                    system("cls")
                    print("="*43)
                    print("Input invalid. Masukkan hanya angka integer")
                    print("="*43)
                    continue
            else:
                system("cls")
                print("Username tidak ada di database")
        break
                    

#Ini adalah fungsi untuk kembalikan barang
def kembalikan_barang():
    data_user = db_user.all()
    username = input("Masukkan username anda : ")
    for a in data_user:
        if username in a:
    
            data_query = Query()
            result = db_pinjam.search(data_query.peminjam == username)
    
            table = PrettyTable()
            data = result
            header = ["No.", "UUID", "Data Peminjam", "Nama Barang", "Jenis Barang", "Jumlah Barang", "Kondisi Barang", "Tanggal Barang Masuk"]
            table.field_names = header
            table.align = "l"

            for i in range(0, len(data)):
                table.add_row(
                    [
                        i + 1,
                        data[i]["uuid"],
                        data[i]["peminjam"],
                        data[i]["nama"],
                        data[i]["jenis"],
                        data[i]["jumlah"],
                        data[i]["kondisi"],
                        data[i]["masuk"],
                    ]
                )

            print(table)
    
    uuid_barang = input("Masukkan uuid barang : ")
    if uuid_barang.isnumeric():
        uuid_barang_int = int(uuid_barang)
        data_query = Query()
        data = db_pinjam.all()
        for i in range(0, len(data)):
            peminjam = username
            nama = data[i]["nama"]
            jenis = data[i]["jenis"]
            kondisi = data[i]["kondisi"]
            jumlah = data[i]["jumlah"]
            masuk = data[i]["masuk"]
        
        if any(d["uuid"] == uuid_barang_int and d["nama"] == nama and d["jenis"] == jenis and d["kondisi"] == kondisi and d["masuk"] == masuk for d in db_barang.all()):    
                        
                    
            get_value = db_barang.get(data_query.uuid == uuid_barang_int)['jumlah']
            new_value = get_value + jumlah

            db_barang.update({"jumlah": new_value}, data_query.uuid == uuid_barang_int)
            db_barang.all()             
            
            db_pinjam.remove(data_query.uuid == uuid_barang_int and data_query.peminjam == peminjam)
            db_pinjam.all()
            
        else:
            print("test")
                            
        system("cls")
        print("=" * 23)
        print("Data berhasil di kembalikan")
        print("=" * 23)
                
    elif uuid_barang == "" or not uuid_barang.strip():
        system("cls")
        print("="*42)
        print("        Input tidak boleh kosong")
        print("="*42)
    else:
        system("cls")
        print("=" * 23)
        print("    UUID Tidak ada.")
        print("=" * 23)
            

# Ini adalah fungsi untuk tampilan menu user
def menu_user():
    header = ["No", "SELAMAT DATANG"]
    table = PrettyTable()
    table.field_names = header
    table.align = "l"
    table.add_row([1, "Lihat data barang di inventory"])
    table.add_row([2, "Lihat data barang yang di pinjam"])
    table.add_row([3, "Pinjam barang"])
    table.add_row([4, "Kembalikan barang"])
    table.add_row([5, "Logout"])
    
    while True:
        print(table)
        pilih = input("Masukkan pilihan menu anda : ")
        if pilih.isnumeric():
            pilih_int = int(pilih)
            if pilih_int == 1:
                system("cls")
                show_barang_inventory()
                print("Klik tombol enter untuk ke menu")
                getpass.getpass("")
                system("cls")
            elif pilih_int == 2:
                system("cls")
                show_barang_pinjam_user()
                print("Klik tombol enter untuk ke menu")
                getpass.getpass("")
                system("cls")
            elif pilih_int == 3:
                system("cls")
                pinjam_barang()
            elif pilih_int == 4:
                system("cls")
                kembalikan_barang()
            elif pilih_int == 5:
                system("cls")
                break
            
        elif pilih == "" or not pilih.strip():
            system("cls")
            print("="*42)
            print("        Input tidak boleh kosong")
            print("="*42)
            continue
        else:
            system("cls")
            print("="*43)
            print("Input invalid. Masukkan hanya angka integer")
            print("="*43)
            continue



# Ini adalah fungsi untuk tampilan menu admin
def menu_admin():
    header = ["No", "SELAMAT DATANG ADMIN"]
    table = PrettyTable()
    table.field_names = header
    table.align = "l"
    table.add_row([1, "Lihat data user yang terdaftar"])
    table.add_row([2, "Lihat data barang di inventory"])
    table.add_row([3, "Lihat data barang yang di pinjam"])
    table.add_row([4, "Tambah barang ke inventory"])
    table.add_row([5, "Ubah data barang di inventory"])
    table.add_row([6, "Hapus barang di inventory"])
    table.add_row([7, "Logout"])

    while True:
        print(table)
        pilih = input("Masukkan pilihan menu anda : ")
        if pilih.isnumeric():
            pilih_int = int(pilih)
            if pilih_int == 1:
                system("cls")
                show_user()
                print("Klik tombol enter untuk ke menu")
                getpass.getpass("")
                system("cls")
            elif pilih_int == 2:
                system("cls")
                show_barang_inventory()
                print("Klik tombol enter untuk ke menu")
                getpass.getpass("")
                system("cls")
            elif pilih_int == 3:
                system("cls")
                show_barang_pinjam()
                print("Klik tombol enter untuk ke menu")
                getpass.getpass("")
                system("cls")
            elif pilih_int == 4:
                system("cls")
                tambah_barang()
            elif pilih_int == 5:
                system("cls")
                ubah_barang()
            elif pilih_int == 6:
                system("cls")
                hapus_barang()
            elif pilih_int == 7:
                system("cls")
                break
        elif pilih == "" or not pilih.strip():
            system("cls")
            print("="*42)
            print("        Input tidak boleh kosong")
            print("="*42)
            continue
        else:
            system("cls")
            print("="*43)
            print("Input invalid. Masukkan hanya angka integer")
            print("="*43)
            continue


# Ini adalah fungsi untuk menampilkan semua data user
def show_user():
    header = ["No", "Nama User"]
    table = PrettyTable()
    table.field_names = header
    table.align = "l"
    data = db_user.all()

    for i, j in enumerate(data):
        for key, value in j.items():
            table.add_row([i + 1, key])

    print(table)


# Ini adalah fungsi untuk menampilkan semua data barang di inventory
def show_barang_inventory():
    table = PrettyTable()
    data = db_barang.all()
    header = ["No.", "UUID", "Nama Barang", "Jenis Barang", "Jumlah Barang", "Kondisi Barang", "Tanggal Barang Masuk"]
    table.field_names = header
    table.align = "l"

    for i in range(0, len(data)):
        table.add_row(
            [
                i + 1,
                data[i]["uuid"],
                data[i]["nama"],
                data[i]["jenis"],
                data[i]["jumlah"],
                data[i]["kondisi"],
                data[i]["masuk"],
            ]
        )

    print(table)  
    
  
#Ini adalah fungsi untuk menampikan semua data barang yang di pinjam 
def show_barang_pinjam():
    table = PrettyTable()
    data = db_pinjam.all()
    header = ["No.", "UUID", "Nama Peminjam","Nama Barang", "Jenis Barang", "Jumlah Barang", "Kondisi Barang", "Tanggal Barang Masuk"]
    table.field_names = header
    table.align = "l"

    for i in range(0, len(data)):
        table.add_row(
            [
                i + 1,
                data[i]["uuid"],
                data[i]["peminjam"],
                data[i]["nama"],
                data[i]["jenis"],
                data[i]["jumlah"],
                data[i]["kondisi"],
                data[i]["masuk"],
            ]
        )

    print(table)  
  
  
#Ini adalah fungsi untuk menampilkan barang yang di pinjam sesuai nama user
def show_barang_pinjam_user():
    
    data_user = db_user.all()
    username = input("Masukkan username anda : ")
    for a in data_user:
        if username in a:
    
            data_query = Query()
            result = db_pinjam.search(data_query.peminjam == username)
    
            table = PrettyTable()
            data = result
            header = ["No.", "UUID", "Data Peminjam", "Nama Barang", "Jenis Barang", "Jumlah Barang", "Kondisi Barang", "Tanggal Barang Masuk"]
            table.field_names = header
            table.align = "l"

            for i in range(0, len(data)):
                table.add_row(
                    [
                        i + 1,
                        data[i]["uuid"],
                        data[i]["peminjam"],
                        data[i]["nama"],
                        data[i]["jenis"],
                        data[i]["jumlah"],
                        data[i]["kondisi"],
                        data[i]["masuk"],
                    ]
                )

            print(table)

# Ini adalah fungsi untuk menambahkan barang ke inventory
def tambah_barang():
    system("cls")
    data = {}
    for d in db_barang.all():
        for key, value in d.items():
            data[key] = value
    while True:
        nama = input("Masukkan nama barang : ")
        
        if nama == "" or not nama.strip():
            system("cls")
            print("="*24)
            print("Input tidak boleh kosong")
            print("="*24)
            continue
        
        table_jenis = PrettyTable()
        table_jenis.field_names = ["No", "Jenis Barang"]
        table_jenis.align = "l"
        table_jenis.add_row([1, "Alat tulis"])
        table_jenis.add_row([2, "Mebel atau perabot"])
        table_jenis.add_row([3, "Alat kebersihan"])
        table_jenis.add_row([4, "Barang lainnya"])
        print(table_jenis)
        
        jenis = input("Masukkan nomor jenis barang : ")
        if jenis.isnumeric():
            jenis_int = int(jenis)
            if jenis_int == 1:
                jenis_str = "Alat tulis"
            elif jenis_int == 2:
                jenis_str = "Mebel atau perabot"
            elif jenis_int == 3:
                jenis_str = "Alat kebersihan"
            elif jenis_int == 4:
                jenis_str = "Barang lainnya"
        elif jenis == "" or not jenis.strip():
            system("cls")
            print("="*24)
            print("Input tidak boleh kosong")
            print("="*24)
            continue
        
        table_kondisi = PrettyTable()
        table_kondisi.field_names = ["No", "Kondisi Barang"]
        table_kondisi.align = "l"
        table_kondisi.add_row([1, "Baik"])
        table_kondisi.add_row([2, "Rusak ringan"])
        print(table_kondisi)
        
        kondisi = input("Masukkan nomor kondisi barang : ")
        if kondisi.isnumeric():
            kondisi_int = int(kondisi)
            if kondisi_int == 1:
                kondisi_str = "Baik"
            elif kondisi_int == 2:
                kondisi_str = "Rusak ringan"
        elif kondisi == "" or not kondisi.strip():
            system("cls")
            print("="*24)
            print("Input tidak boleh kosong")
            print("="*24)
            continue
        else:
            system("cls")
            print("="*43)
            print("Input invalid. Masukkan hanya angka integer")
            print("="*43)
            continue
        
        amount = input("Masukkan jumlah barang : ")
        if amount.isnumeric():
            amount_int = int(amount)
            if amount_int == 0:
                system("cls")
                print("="*24)
                print("Tidak boleh berjumlah 0")
                print("="*24)
                continue
        elif amount == "" or not kondisi.strip():
            system("cls")
            print("="*24)
            print("Input tidak boleh kosong")
            print("="*24)
            continue
        else:
            system("cls")
            print("="*43)
            print("Input invalid. Masukkan hanya angka integer")
            print("="*43)
            continue
        
        masuk = str(datetime.date.today())
        
        id_barang = random.randint(0000, 9999)
        
        data_query = Query()
        
        
        if any(d["nama"] == nama and d["jenis"] == jenis_str and d["kondisi"] == kondisi_str and d["masuk"] == masuk for d in db_barang.all()):    

            get_value = db_barang.get(data_query.nama == nama)['jumlah']
            new_value = get_value + amount_int
            db_barang.update({"jumlah": new_value}, data_query.nama == nama)
            db_barang.all()
            system("cls")
            print("=" * 41)
            print("   Barang berhasil masuk ke inventory.")
            print("=" * 41)
            break
        else:
            db_barang.insert(
                {
                    "uuid": id_barang, 
                    "nama": nama,
                    "jenis": jenis_str,
                    "jumlah": amount_int,
                    "kondisi": kondisi_str,
                    "masuk": masuk
                }
            )
            print("=" * 41)
            print("   Barang berhasil masuk ke inventory.")
            print("=" * 41)
            break



# Ini adalah fungsi untuk merubah data barang di inventory
def ubah_barang():
    data_barang = db_barang.all()
    system("cls")

    show_barang_inventory()
    uuid = int(input("Masukkan uuid barang : "))
    
    db_barang.all()
    table = PrettyTable()
    header = ["No", "MENU UBAH"]
    table.field_names = header
    table.align = "l"
    table.add_row([1, "Nama"])
    table.add_row([2, "Jenis"])
    table.add_row([3, "Jumlah"])
    table.add_row([4, "Kondisi"])
    table.add_row([5, "Keluar"])

    while True:
        print(table)
        pilih = int(input("Masukkan pilihan menu untuk mengubah data barang : "))

        data = Query()

        if pilih == 1:
            nama_baru = input("Masukkan nama barang yang baru : ")
            db_barang.update({"nama": nama_baru}, data.uuid == uuid)
            db_barang.all()

            
            system("cls")
            show_barang_inventory()
            print("=" * 21)
            print("Data berhasil di ubah")
            print("=" * 21)

        elif pilih == 2:
            jenis_baru = input("Masukkan jenis barang yang baru : ")
            db_barang.update({"jenis": jenis_baru}, data.id == uuid)
            db_barang.all()

            system("cls")
            show_barang_inventory()
            print("=" * 21)
            print("Data berhasil di ubah")
            print("=" * 21)

        elif pilih == 3:
            try:
                jumlah_baru = int(input("Masukkan jumlah barang yang baru : "))
                db_barang.update({"jumlah": jumlah_baru}, data.id == uuid)
                db_barang.all()

                system("cls")
                show_barang_inventory()
                print("=" * 21)
                print("Data berhasil di ubah")
                print("=" * 21)
            except:
                system("cls")
                print("=" * 30)
                print("Input jumlah tidak boleh huruf")
                print("=" * 30)

        elif pilih == 4:
            kondisi_baru = input("Masukkan kondisi barang yang baru : ")
            show_barang_inventory()
            db_barang.update({"kondisi": kondisi_baru}, data.id == uuid)
            db_barang.all()

            system("cls")
            print("=" * 21)
            print("Data berhasil di ubah")
            print("=" * 21)

        elif pilih == 5:
            system("cls")
            break


# Ini adalah fungsi untuk menghapus data barang
def hapus_barang():
    show_barang_inventory()
    
    data_query = Query()

    uuid = int(input("Masukkan nama barang yang ingin di hapus : "))
    if uuid == "":
        system("cls")
        print("="*24)
        print("Input tidak boleh kosong")
        print("="*24)
    
    print("Klik tombol enter untuk hapus")
    getpass.getpass("")
    
    db_barang.remove(data_query.uuid == uuid)
    db_barang.all()

    system("cls")
    print("=" * 41)
    print("         Data berhasil di hapus")
    print("=" * 41)
    

if __name__ == "__main__":
    while True:
        chooseLogin()
