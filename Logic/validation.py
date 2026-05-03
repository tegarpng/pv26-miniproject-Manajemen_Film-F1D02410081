from PySide6.QtWidgets import QMessageBox

class Validasi:
    def validasi_film(self, judul, sutradara, tahun, durasi, rating):
        if not judul:
            QMessageBox.warning(self, "Peringatan", "Judul tidak boleh kosong!")
            return False
        
        if not sutradara:
            QMessageBox.warning(self, "Peringatan", "Sutradara tidak boleh kosong!")
            return False
        
        if len(judul) < 2:
            QMessageBox.warning(self, "Peringatan", "Judul minimal 2 karakter!")
            return False
        
        if len(sutradara) < 2:
            QMessageBox.warning(self, "Peringatan", "Sutradara minimal 2 karakter!")
            return False

        return True