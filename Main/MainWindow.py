import csv
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QTableWidget, QFileDialog,
    QLabel, QMainWindow, QWidget, QLineEdit, QHeaderView, QComboBox, QMessageBox
)
from PySide6.QtGui import QAction, QKeySequence
from Main.film_dialog import CreateFilm, EditFilm
from Database.DB_film import Database

def load_stylesheet(filepath):
    """Load QSS dari file dan return sebagai string"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File QSS tidak ditemukan: {filepath}")
        return ""

class MainWindow(QMainWindow):
    def __init__(self, db_path="data_film.db"):
        super().__init__()
        self.setWindowTitle("Projektor")
        self.setGeometry(100, 100, 800, 600)

        self.db = Database(db_path)
        self.selected_id = None
        self.is_dark = False
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.action()
        self.menu_bar()
        self.central_widget()
        self.statusBar().showMessage("Ready")

    def action(self):
        self.export_data = QAction("Export", self)
        self.export_data.setStatusTip("Eksport Data")
        self.export_data.setShortcut("Ctrl+E")
        self.export_data.triggered.connect(self.export_file)
        
        self.import_data = QAction("Import", self)
        self.import_data.setStatusTip("Import Data")
        self.import_data.setShortcut("Ctrl+I")
        self.import_data.triggered.connect(self.import_file)
        
        self.mode = QAction("Dark Mode", self)
        self.mode.setCheckable(True)
        self.mode.setChecked(False)
        self.mode.triggered.connect(self.toggle_theme)
        
        self.exit = QAction("Exit", self)
        self.exit.triggered.connect(self.close)
        
        self.tambah = QAction("+ Tambah", self)
        self.tambah.setShortcut(QKeySequence.New)
        self.tambah.setStatusTip("Tambah data")
        self.tambah.triggered.connect(self.open_dialog)
        
        self.edit = QAction("Edit", self)
        self.edit.setStatusTip("Edit data")
        self.edit.setShortcut("Alt+E")
        self.edit.triggered.connect(self.open_edit)
        
        self.hapus = QAction("Hapus", self)
        self.hapus.setStatusTip("Hapus data")
        self.hapus.setShortcut("Ctrl+X")
        self.hapus.triggered.connect(self.delete_data)
        
        self.info = QAction("Information", self)
        self.info.setStatusTip("Informasi Aplikasi")
        self.info.triggered.connect(self.information)

    def menu_bar(self):
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.export_data)
        file_menu.addAction(self.import_data)
        file_menu.addAction(self.mode)
        file_menu.addSeparator()
        file_menu.addAction(self.exit)
        kelola_menu = self.menuBar().addMenu("&Kelola File")
        kelola_menu.addAction(self.tambah)
        kelola_menu.addAction(self.edit)
        kelola_menu.addAction(self.hapus)
        aplikasi_menu = self.menuBar().addMenu("&Tentang aplikasi")
        aplikasi_menu.addAction(self.info)

    def central_widget(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        header_layout = QHBoxLayout()
        layout_h = QHBoxLayout()

        self.label_nama = QLabel("MUHAMMAD TEGAR BIJANTA - F1D02410081")
        self.label_total_data = QLabel("Total data: 0")
        self.label_total_data.setObjectName("Label_total")
        self.label_total_tonton = QLabel("Total tonton: 0")
        self.label_total_tonton.setObjectName("Label_tonton")
        header_layout.addWidget(self.label_nama)
        header_layout.addWidget(self.label_total_data)
        header_layout.addWidget(self.label_total_tonton)
        
        self.labelf_genre = QLabel("Filter")
        self.filter = QComboBox()
        self.filter.addItems(["All","Action", "Drama", "Comedy", "Horror", "Sci-Fi"])
        layout_h.addWidget(self.labelf_genre)
        layout_h.addWidget(self.filter)

        self.filtercari = QLineEdit()
        self.filtercari.setPlaceholderText("Cari Film atau Sutradara")
        layout_h.addWidget(self.filtercari)
        
        self.filter.currentTextChanged.connect(self.filter_data)
        self.filtercari.textChanged.connect(self.filter_data)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Judul Film", "Sutradara",  "Genre", "Tahun Terbit", "Durasi", "Rating", "Status Tonton"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.clicked.connect(self.on_row_selected)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(layout_h)
        main_layout.addWidget(self.table)

        self.setCentralWidget(central_widget)
    
    def on_row_selected(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            item = self.table.item(selected_row, 0)
            if item:
                self.selected_id = int(item.text())

    def open_dialog(self):
        dialog = CreateFilm()

        if dialog.exec():
            data = dialog.get_data()
            self.db.tambah(
                data['judul'],
                data['sutradara'],
                data['genre'],
                data['tahun'],
                data['durasi'],
                data['rating'],
                data['status']
            )
            self.load_data()
            QMessageBox.information(self, "", "Data berhasil ditambahkan")
            
    def toggle_theme(self):
        self.is_dark = self.mode.isChecked()
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            style = load_stylesheet("Style/styledark.qss")
            if style:
                QApplication.instance().setStyleSheet(style)
                self.statusBar().showMessage("Dark Mode diaktifkan")
        else:
            style = load_stylesheet("Style/stylelight.qss")
            if style:
                QApplication.instance().setStyleSheet(style)
                self.statusBar().showMessage("Light Mode diaktifkan")
            
    def open_edit(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Peringatan", "Pilih film yang ingin diedit!")
            return
        # Asumsi urutan kolom: ID, Judul, Genre, Tahun, Durasi, Rating, Status
        data_film = {
            "id": int(self.table.item(selected_row, 0).text()),
            "judul": self.table.item(selected_row, 1).text(),
            "sutradara": self.table.item(selected_row, 2).text(),
            "genre": self.table.item(selected_row, 3).text(),
            "tahun": int(self.table.item(selected_row, 4).text()),
            "durasi": int(self.table.item(selected_row, 5).text()),
            "rating": float(self.table.item(selected_row, 6).text()),
            "status": self.table.item(selected_row, 7).text()
        }

        # 3. Buka Dialog Edit dengan membawa data tersebut
        dialog = EditFilm(data_film)
        
        if dialog.exec():
            # 4. Jika user klik Simpan, ambil data baru dari dialog
            updated_data = dialog.get_data()
            
            # 5. Kirim ke Database
            self.db.update(
                updated_data['id'],
                updated_data['judul'],
                updated_data['sutradara'],
                updated_data['genre'],
                updated_data['tahun'],
                updated_data['durasi'],
                updated_data['rating'],
                updated_data['status']
            )

            self.statusBar().showMessage("Data berhasil diperbarui")
            self.load_data()

    def delete_data(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih data di tabel yang akan dihapus!")
            return
        
        reply = QMessageBox.question(
            self, "Konfirmasi",
            "Yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.hapus(self.selected_id)
            self.load_data()
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")

    def information(self):
        QMessageBox.information(
            self, 
            "Information",
            "Projector\n\nAplikasi ini merupakan aplikasi manajemen film pribadi yang dimana pengguna dapat memasukkan film film, baik yang sudah ditonton atau belum. Rating langsung diberikan oleh pengguna aplikasi\n\nNama: Muhammad Tegar Bijanta\nNIM: F1D02410081"
        )

    def export_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
			self,
			"Export File",
			"",
			"CSV Files (*.csv);;All Files (*)"
		)
        
        if not file_path:
            return
        
        data = self.db.ambil_semua()
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                writer.writerow(["ID", "Judul", "Sutradara", "Genre", "Tahun Terbit", "Durasi", "Rating", "Status Tonton"])
                
                for row in data:
                    writer.writerow([row['id'], row['judul'], row['sutradara'], row['genre'], row['tahun'], row['durasi'], row['rating'], row['status']])
            
            QMessageBox.information(
                self, "Sukses",
                f"Data berhasil di-export!\n\nFile: {file_path}\nTotal: {len(data)} baris"
            )
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal export:\n{e}")

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import File",
            "",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader) 

                total = 0
                duplikat = 0
                error = 0

                for row in reader:
                    try:
                        success = self.db.tambah(
                            row[1],
                            row[2],
                            row[3],
                            int(row[4]),
                            int(row[5]),
                            float(row[6]),
                            row[7]
                        )

                        if success:
                            total += 1
                        else:
                            duplikat += 1

                    except (ValueError, IndexError):
                        error += 1

            self.load_data()
            QMessageBox.information(
                self,
                "Hasil Import",
                f"Import selesai!\n\n"
                f"Berhasil : {total}\n"
                f"Duplikat : {duplikat}\n"
                f"Error    : {error}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal import:\n{e}")
            
    def load_data(self):
        self.selected_id = None
        data = self.db.ambil_semua()
        self.tampilkan_ke_tabel(data)
        self.load_label_data(data)

    def load_label_data(self, data):
        total = len(data)
        self.label_total_data.setText(f"Total data: {total}")
        tonton = 0
        for row in data:
            if row['status'] == "Sudah Menonton":
                tonton+=1
        self.label_total_tonton.setText(f"Total sudah ditonton: {tonton}")
    

    def tampilkan_ke_tabel(self, data):
        self.table.setRowCount(0)
        
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(row_data['judul']))
            self.table.setItem(row, 2, QTableWidgetItem(row_data['sutradara']))
            self.table.setItem(row, 3, QTableWidgetItem(row_data['genre']))
            self.table.setItem(row, 4, QTableWidgetItem(str(row_data['tahun'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(row_data['durasi'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(row_data['rating'])))
            self.table.setItem(row, 7, QTableWidgetItem(row_data['status']))

    def filter_data(self):
        keyword = self.filtercari.text().strip()
        genre = self.filter.currentText()
        
        data = self.db.cari(keyword, genre)
        self.tampilkan_ke_tabel(data)
        
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Konfirmasi Keluar",
            "Apakah Anda yakin ingin menutup Projektor",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()