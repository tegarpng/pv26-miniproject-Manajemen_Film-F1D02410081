import sqlite3

class Database:

	def __init__(self, db_name='data_film.db'):
		self.db_name = db_name
		self.create_table()

	def get_connection(self):
		conn = sqlite3.connect(self.db_name)
		conn.row_factory = sqlite3.Row
		return conn

	def create_table(self):
		with self.get_connection() as conn:
			conn.execute('''
				CREATE TABLE IF NOT EXISTS film (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					judul TEXT NOT NULL,
					genre TEXT NOT NULL,
					sutradara TEXT NOT NULL,
					tahun INTEGER NOT NULL,
					durasi INTEGER NOT NULL,
					rating REAL NOT NULL,
					status TEXT NOT NULL
				)
			''')

	def tambah(self, judul,sutradara, genre, tahun, durasi, rating, status):
  
		if self.is_exist(judul, sutradara, tahun):
			return False

		try:
			with self.get_connection() as conn:
				conn.execute(
					'INSERT INTO film (judul, sutradara, genre, tahun, durasi, rating, status) VALUES (?,?,?,?,?,?,?)',
					(judul, sutradara, genre, tahun, durasi, rating, status)
				)
			return True
		except sqlite3.IntegrityError:
			return False

	def ambil_semua(self):
		with self.get_connection() as conn:
			return conn.execute('SELECT * FROM film ORDER BY judul').fetchall()
		
	def update(self, id, judul, sutradara, genre, tahun, durasi, rating, status):
		with self.get_connection() as conn:
			conn.execute('UPDATE film SET judul=?, sutradara=?, genre=?, tahun=?, durasi=?, rating=?, status=? WHERE id=?', (judul, sutradara, genre, tahun, durasi, rating, status, id))
   
	def cari(self, keyword, genre):
		with self.get_connection() as conn:
			if keyword and genre != 'All':
				return conn.execute(
					'SELECT * FROM film WHERE (judul LIKE ? OR sutradara LIKE ?) AND genre = ? ORDER BY judul',
					(f'%{keyword}%',f'%{keyword}%', genre)
				).fetchall()
			elif keyword:
				return conn.execute(
					'SELECT * FROM film WHERE judul LIKE ? OR sutradara LIKE ? ORDER BY judul',
					(f'%{keyword}%', f'%{keyword}%')
				).fetchall()
			elif genre != 'All':
				return conn.execute(
					'SELECT * FROM film WHERE genre = ? ORDER BY judul',
					(genre,)
				).fetchall()
			else:
				return conn.execute(
					'SELECT * FROM film ORDER BY judul'
				).fetchall()
 
	def hapus(self, id):
		with self.get_connection() as conn:
			conn.execute('DELETE FROM film WHERE id = ?', (id,))
   
	def is_exist(self, judul, sutradara, tahun):
		with self.get_connection() as conn:
			result = conn.execute(
				'''
				SELECT 1 FROM film 
				WHERE LOWER(TRIM(judul)) = LOWER(TRIM(?))
				AND LOWER(TRIM(sutradara)) = LOWER(TRIM(?))
				AND tahun = ?
				''',
				(judul, sutradara, tahun)
			).fetchone()
			return result is not None
