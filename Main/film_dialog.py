from PySide6.QtWidgets import (
    QDialog, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QLabel,
    QPushButton, QHBoxLayout, QVBoxLayout
)

from Logic.validation import Validasi

class CreateFilm(QDialog, Validasi):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Film")
        self.setMinimumWidth(350)
        
        layout_h = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        self.judul = QLineEdit()
        self.judul.setPlaceholderText("Masukkan judul film")

        self.genre = QComboBox()
        self.genre.addItems(["Action", "Drama", "Comedy", "Horror", "Sci-Fi"])
        layout_h.addWidget(QLabel("Genre"))
        layout_h.addWidget(self.genre)
        
        self.sutradara = QLineEdit()
        self.sutradara.setPlaceholderText("Masukkan sutradara film")

        self.tahun = QSpinBox()
        self.tahun.setRange(1900, 2030)
        layout_h.addWidget(QLabel("Tahun"))
        layout_h.addWidget(self.tahun)

        self.durasi = QSpinBox()
        self.durasi.setRange(0, 240)
        layout_h2.addWidget(QLabel("Durasi"))
        layout_h2.addWidget(self.durasi)

        self.rating = QDoubleSpinBox()
        self.rating.setRange(0, 10)
        self.rating.setSingleStep(0.1)
        layout_h2.addWidget(QLabel("Rating"))
        layout_h2.addWidget(self.rating)


        self.status = QComboBox()
        self.status.addItems(["Belum ditonton", "Sudah Menonton"])

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Judul Film"))
        input_layout.addWidget(self.judul)
        input_layout.addWidget(QLabel("Sutradara"))
        input_layout.addWidget(self.sutradara)
        input_layout.addLayout(layout_h)
        input_layout.addLayout(layout_h2)
        input_layout.addWidget(QLabel("Status Nonton"))
        input_layout.addWidget(self.status)

        # BUTTON
        self.btn_simpan = QPushButton("Simpan")
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("batal")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_simpan)
        btn_layout.addWidget(self.btn_batal)

        # MAIN LAYOUT
        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # SIGNAL
        self.btn_simpan.clicked.connect(self.simpan)
        self.btn_batal.clicked.connect(self.reject)

    def get_data(self):
        return {
            "judul": self.judul.text().strip(),
            "sutradara": self.sutradara.text().strip(),
            "genre": self.genre.currentText().strip(),
            "tahun": self.tahun.value(),
            "durasi": self.durasi.value(),
            "rating": self.rating.value(),
            "status": self.status.currentText().strip()
        }
        
    def simpan(self):
        judul = self.judul.text().strip()
        sutradara = self.sutradara.text().strip()
        tahun = self.tahun.value()
        durasi = self.durasi.value()
        rating = self.rating.value()

        if self.validasi_film(judul, sutradara, tahun, durasi, rating):
            self.accept()
        
	
class EditFilm(QDialog, Validasi):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Edit Film")

        self.film_id = data["id"] if data else None
        layout_h = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        self.judul = QLineEdit()

        self.genre = QComboBox()
        self.genre.addItems(["Action", "Drama", "Comedy", "Horror", "Sci-Fi"])
        layout_h.addWidget(QLabel("Genre"))
        layout_h.addWidget(self.genre)
        
        self.sutradara = QLineEdit()

        self.tahun = QSpinBox()
        self.tahun.setRange(1900, 2030)
        layout_h.addWidget(QLabel("Tahun"))
        layout_h.addWidget(self.tahun)

        self.durasi = QSpinBox()
        self.durasi.setRange(0, 240)
        layout_h2.addWidget(QLabel("Durasi"))
        layout_h2.addWidget(self.durasi)

        self.rating = QDoubleSpinBox()
        self.rating.setRange(0, 10)
        self.rating.setSingleStep(0.1)
        layout_h2.addWidget(QLabel("Rating"))
        layout_h2.addWidget(self.rating)


        self.status = QComboBox()
        self.status.addItems(["Belum ditonton", "Sudah Menonton"])

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Judul Film"))
        input_layout.addWidget(self.judul)
        input_layout.addWidget(QLabel("Sutradara"))
        input_layout.addWidget(self.sutradara)
        input_layout.addLayout(layout_h)
        input_layout.addLayout(layout_h2)
        input_layout.addWidget(QLabel("Status Nonton"))
        input_layout.addWidget(self.status)

        self.btn_simpan = QPushButton("Simpan")
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("batal")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_simpan)
        btn_layout.addWidget(self.btn_batal)

        # MAIN
        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # SIGNAL
        self.btn_simpan.clicked.connect(self.simpan)
        self.btn_batal.clicked.connect(self.reject)

        if data:
            self.set_data(data)

    def set_data(self, data):
        self.judul.setText(data["judul"])
        self.sutradara.setText(data["sutradara"])
        self.genre.setCurrentText(data["genre"])
        self.tahun.setValue(data["tahun"])
        self.durasi.setValue(data["durasi"])
        self.rating.setValue(data["rating"])
        self.status.setCurrentText(data["status"])

    def get_data(self):
        return {
            "id": self.film_id,
            "judul": self.judul.text(),
            "sutradara": self.sutradara.text(),
            "genre": self.genre.currentText(),
            "tahun": self.tahun.value(),
            "durasi": self.durasi.value(),
            "rating": self.rating.value(),
            "status": self.status.currentText(),
        }
        
    def simpan(self):
        judul = self.judul.text().strip()
        sutradara = self.sutradara.text().strip()
        tahun = self.tahun.value()
        durasi = self.durasi.value()
        rating = self.rating.value()

        if self.validasi_film(judul, sutradara, tahun, durasi, rating):
            self.accept()