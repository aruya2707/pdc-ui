Tugas Quiz:
web flask wajib harus ada operasi :

- Membaca Citra jpg/png, [✓]
- Menampilkan Citra(Tampilan Grayscale,Binary) [✓]
- Menu Pilihan Operasi Morfologi : Dilasi, Erosi Opening (Erosi-Dilasi), Closing(Dilasi-Erosi). [✓]
- Tampilan Operasi Morfologi [✓]
- Counting objeck [✓]

#Penggunaan

- upload gambar yang ingin dihitung objeknya
- pilih menu count object
- citra hasil proses perhitungan dan nilai hitungan akan muncul di tampilan utama

1. **Membaca Citra JPG/PNG**:

   - mengunggah file citra dalam format JPG atau PNG.

2. **Menampilkan Citra**:

   - Citra yang diunggah akan ditampilkan di antarmuka web.

3. **Operasi Morfologi**:

   - Ada menu operasi morfologi, Dilasi, Erosi, Opening (Erosi-Dilasi), dan Closing (Dilasi-Erosi).

4. **Tampilan Operasi Morfologi**:

   - Hasil dari setiap operasi morfologi akan ditampilkan di antarmuka web.

5. **Counting Objek**:
   - Dapat melakukan penghitungan jumlah objek pada citra yang telah diolah.

# Count Objek pada Citra Menggunakan Metode Watershed

Projek ini merupakan implementasi penghitungan objek pada citra menggunakan metode watershed. Metode ini memungkinkan untuk mengidentifikasi dan menghitung jumlah objek yang terdapat pada citra.

## Alur Proses

1. **Pra-Pemrosesan Citra**:
   **Pembacaan Citra**: Citra dibaca menggunakan OpenCV (cv2) dengan mode grayscale (`cv2.imread('static/img/img_now.jpg', 0)`).
   **Penghapusan Noise**: Terkadang, citra dapat mengandung noise yang dapat memengaruhi hasil segmentasi. Oleh karena itu, citra dimurnikan dengan menggunakan filter Gaussian untuk mengurangi noise (`cv2.GaussianBlur(img, (5, 5), 0)`).

2. **Segmentasi Objek**:
   **Thresholding**: Proses thresholding dilakukan untuk mengubah citra menjadi citra biner, di mana setiap piksel diberi nilai 0 atau 255 berdasarkan ambang tertentu. Di sini, metode Otsu digunakan untuk menentukan nilai threshold secara otomatis (`cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)`).
   **Pembuatan Background dan Foreground yang Jelas**: Citra hasil thresholding diproses lebih lanjut untuk memisahkan area latar belakang dan area objek dengan melakukan operasi morfologi "Opening" (`cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)`).
   **Penghitungan Jumlah Objek**: Setelah mendapatkan area yang jelas untuk objek dan latar belakang, dilakukan proses segmentasi untuk mengidentifikasi objek secara terpisah. Proses ini dilakukan dengan menggunakan transformasi jarak (distance transform) untuk mengidentifikasi area terdekat dari setiap piksel ke tepi objek. Setelah itu, dilakukan segmentasi menggunakan algoritma watershed untuk memisahkan objek yang saling berdekatan.
   **Pembuatan Marker**: Untuk melakukan segmentasi menggunakan algoritma watershed, marker harus dibuat. Marker ini digunakan untuk menandai area objek dan area latar belakang pada citra.
   **Penggunaan Watershed**: Algoritma watershed digunakan untuk mengisi area yang telah ditandai dengan marker. Proses ini akan memisahkan objek yang berdekatan dengan tepi yang jelas.

3. **Penghitungan Objek**:
   Setelah proses watershed selesai, jumlah objek dihitung dengan menghitung jumlah label yang terbentuk pada hasil segmentasi, dikurangi dengan label untuk latar belakang dan ukuran citra.
   **Pemberian Label pada Citra**: Setelah penghitungan selesai, label tambahan ditambahkan pada citra untuk menandai area yang telah dihitung.
   **Penyimpanan Citra**: Citra hasil proses segmentasi dan penghitungan objek disimpan untuk visualisasi dan referensi lebih lanjut.
