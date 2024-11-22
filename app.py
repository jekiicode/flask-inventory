from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Data Gudang (simulasi)
gudang_data = []
penambahan_data = []
pengurangan_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        jumlah = int(request.form['jumlah'])
        # Cek apakah barang dengan kode yang sama sudah ada
        for item in gudang_data:
            if item['kode'] == kode:
                item['jumlah'] += jumlah
                return render_template('tambah.html', success=True)
        # Jika barang belum ada, tambahkan barang baru
        gudang_data.append({'kode': kode, 'nama': nama, 'jumlah': jumlah})
        penambahan_data.append({'kode': kode, 'nama': nama, 'jumlah': jumlah, 'waktu': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return render_template('tambah.html', success=True)
    return render_template('tambah.html')

@app.route('/tambah-jumlah', methods=['GET', 'POST'])
def tambah_jumlah():
    if request.method == 'POST':
        kode = request.form['kode']
        jumlah = int(request.form['jumlah'])
        nama_barang = None
        waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ambil waktu saat ini
        
        # Cek apakah barang dengan kode yang sama ada dan ambil nama barangnya
        for item in gudang_data:
            if item['kode'] == kode:
                item['jumlah'] += jumlah
                nama_barang = item['nama']  # Ambil nama barang
                penambahan_data.append({'kode': kode, 'nama': nama_barang, 'jumlah': jumlah, 'waktu': waktu})
                return render_template('tambah_jumlah.html', success=True)
        
        # Jika barang tidak ditemukan
        return render_template('tambah_jumlah.html', error="Barang tidak ditemukan")
    
    return render_template('tambah_jumlah.html')

@app.route('/kurangi', methods=['GET', 'POST'])
def kurangi():
    if request.method == 'POST':
        kode = request.form['kode']
        jumlah = int(request.form['jumlah'])
        keterangan = request.form['penjelasan']
        waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Waktu saat pengurangan barang

        nama_barang = None  # Variabel untuk menyimpan nama barang berdasarkan kode
        
        # Logika untuk mengurangi barang
        for item in gudang_data:
            if item['kode'] == kode:
                if item['jumlah'] >= jumlah:
                    item['jumlah'] -= jumlah
                    nama_barang = item['nama']  # Ambil nama barang berdasarkan kode
                    pengurangan_data.append({
                        'kode': kode,
                        'nama': nama_barang,  # Menambahkan nama barang
                        'jumlah': jumlah,     # Menambahkan jumlah barang yang dikurangi
                        'keterangan': keterangan,  # Mengganti penjelasan dengan keterangan
                        'waktu': waktu        # Menambahkan waktu
                    })
                    return render_template('kurangi.html', success=True)
                else:
                    return render_template('kurangi.html', error="Jumlah tidak cukup")
        
        # Jika kode barang tidak ditemukan
        return render_template('kurangi.html', error="Barang tidak ditemukan")
    
    return render_template('kurangi.html')

@app.route('/data-barang')
def data_barang():
    return render_template('data_barang.html', gudang=gudang_data, penambahan=penambahan_data, pengurangan=pengurangan_data)

if __name__ == '__main__':
    app.run(debug=True)
