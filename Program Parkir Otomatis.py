# Library
from datetime import datetime
import random
import os
import time

class Kendaraan:
    def __init__(self, plat, jenis):
        self.plat = plat.upper()
        self.jenis = jenis.capitalize()
        self.waktu_masuk = datetime.now()
        self.kode_tiket = self.generate_tiket()
    def generate_tiket(self):
        return "PKR-" + str(random.randint(10000, 99999))


class SistemParkir:
    def __init__(self):
        # Slot parkir mobil 5x5
        self.slot_mobil = [[0 for _ in range(5)] for _ in range(5)]
        # Slot parkir motor 8x8
        self.slot_motor = [[0 for _ in range(8)] for _ in range(8)]
        # Database kendaraan aktif
        self.data_parkir = {}

    # CLEAR SCREEN
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # PAUSE SCREEN
    def pause(self):
        input("\nTekan ENTER untuk kembali ke menu...")

    # LOADING FFECT
    def loading(self):
        print("\nMemproses", end="")
        for i in range(3):
            time.sleep(0.4)
            print(".", end="")
        print("\n")

    # TAMPILKAN SLOT
    def tampilkan_slot(self, jenis):
        self.clear()
        if jenis == "Mobil":
            matrix = self.slot_mobil
        else:
            matrix = self.slot_motor
        print(f"\n===== SLOT {jenis.upper()} =====")

        print("\nKeterangan:")
        print("0 = Kosong")
        print("1 = Terisi\n")

        for row in matrix:
            for item in row:
                print(item, end=" ")
            print()
        self.pause()

    # CARI SLOT KOSONG
    def cari_slot(self, jenis):
        if jenis == "Mobil":
            matrix = self.slot_mobil
        else:
            matrix = self.slot_motor
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    matrix[i][j] = 1
                    return (i, j)
        return None

    # PARKIR MASUK

    def kendaraan_masuk(self):
        self.clear()
        print("\n===== KENDARAAN MASUK =====")
        plat = input("Masukkan plat nomor : ")
        jenis = input("Jenis kendaraan (Mobil/Motor): ").capitalize()

        if jenis not in ["Mobil", "Motor"]:
            print("\nJenis kendaraan tidak valid!")
            self.pause()
            return
        self.loading()

        kendaraan = Kendaraan(plat, jenis)

        slot = self.cari_slot(jenis)
        if slot is None:
            print("Maaf, parkiran penuh!")
            self.pause()
            return
        self.data_parkir[kendaraan.kode_tiket] = {
            "kendaraan": kendaraan,
            "slot": slot
        }

        print("===================================")
        print("      TIKET PARKIR DIGITAL")
        print("===================================")
        print(f"Kode Tiket : {kendaraan.kode_tiket}")
        print(f"Plat Nomor : {kendaraan.plat}")
        print(f"Jenis      : {kendaraan.jenis}")
        print(f"Waktu Masuk: {kendaraan.waktu_masuk.strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"Slot       : {slot}")
        print("===================================")
        self.pause()

    # HITUNG TARIF
    def hitung_tarif(self, jenis, durasi_jam):
        if jenis == "Mobil":
            if durasi_jam <= 2:
                return 5000
            else:
                return 5000 + ((durasi_jam - 2) * 3000)
        else:
            if durasi_jam <= 2:
                return 3000
            else:
                return 3000 + ((durasi_jam - 2) * 2000)

    # PARKIR KELUAR
    def kendaraan_keluar(self):
        self.clear()
        print("\n===== KENDARAAN KELUAR =====")
        kode = input("Masukkan kode tiket: ").upper()
        if kode not in self.data_parkir:
            print("\nKode tiket tidak ditemukan!")
            self.pause()
            return
        self.loading()

        data = self.data_parkir[kode]
        kendaraan = data["kendaraan"]
        slot = data["slot"]
        waktu_keluar = datetime.now()
        durasi = waktu_keluar - kendaraan.waktu_masuk
        durasi_jam = max(1, int(durasi.total_seconds() / 3600))
        biaya = self.hitung_tarif(kendaraan.jenis, durasi_jam)

        print("===================================")
        print("         STRUK PARKIR")
        print("===================================")
        print(f"Plat Nomor   : {kendaraan.plat}")
        print(f"Jenis        : {kendaraan.jenis}")
        print(f"Waktu Masuk  : {kendaraan.waktu_masuk.strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"Waktu Keluar : {waktu_keluar.strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"Durasi       : {durasi_jam} Jam")
        print(f"Total Biaya  : Rp {biaya:,}")
        print("===================================")
        bayar = int(input("Masukkan uang pembayaran : Rp "))
        if bayar < biaya:
            print(f"\nUang kurang Rp {biaya - bayar:,}")
            self.pause()
            return
        kembali = bayar - biaya
        print(f"\nKembalian : Rp {kembali:,}")

        # Kosongkan slot
        if kendaraan.jenis == "Mobil":
            self.slot_mobil[slot[0]][slot[1]] = 0
        else:
            self.slot_motor[slot[0]][slot[1]] = 0
        del self.data_parkir[kode]
        print("\nTerima kasih telah menggunakan parkir kami!")
        self.pause()

    # DASHBOARD
    def dashboard(self):
        self.clear()
        total_mobil = sum(row.count(1) for row in self.slot_mobil)
        total_motor = sum(row.count(1) for row in self.slot_motor)
        print("\n========== DASHBOARD ==========")
        print(f"Mobil Parkir           : {total_mobil}")
        print(f"Motor Parkir           : {total_motor}")
        print(f"Total Kendaraan Aktif  : {len(self.data_parkir)}")
        print("================================")
        self.pause()

    # CARI KENDARAAN
    def cari_kendaraan(self):
        self.clear()
        print("\n===== CARI KENDARAAN =====")
        plat = input("Masukkan plat nomor: ").upper()
        ditemukan = False
        for kode, data in self.data_parkir.items():
            kendaraan = data["kendaraan"]
            if kendaraan.plat == plat:
                print("\n===================================")
                print("        KENDARAAN DITEMUKAN")
                print("===================================")
                print(f"Kode Tiket : {kode}")
                print(f"Jenis      : {kendaraan.jenis}")
                print(f"Slot       : {data['slot']}")
                print(f"Waktu Masuk: {kendaraan.waktu_masuk.strftime('%d-%m-%Y %H:%M:%S')}")
                print("===================================")
                ditemukan = True
        if not ditemukan:
            print("\nKendaraan tidak ditemukan.")
        self.pause()

    # MENU UTAMA
    def menu(self):
        while True:
            self.clear()
            print("======================================")
            print(" SISTEM PORTAL PARKIR OTOMATIS")
            print("======================================")
            print("1. Kendaraan Masuk")
            print("2. Kendaraan Keluar")
            print("3. Dashboard")
            print("4. Cari Kendaraan")
            print("5. Lihat Slot Mobil")
            print("6. Lihat Slot Motor")
            print("7. Keluar")
            print("======================================")
            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                self.kendaraan_masuk()
            elif pilihan == "2":
                self.kendaraan_keluar()
            elif pilihan == "3":
                self.dashboard()
            elif pilihan == "4":
                self.cari_kendaraan()
            elif pilihan == "5":
                self.tampilkan_slot("Mobil")
            elif pilihan == "6":
                self.tampilkan_slot("Motor")
            elif pilihan == "7":
                self.clear()
                print("Program selesai.")
                break
            else:
                print("\nMenu tidak valid!")
                time.sleep(1.5)

# MENJALANKAN PROGRAM
parkir = SistemParkir()
parkir.menu()