# Implementasi Algoritma Iterative Deepening A* (IDA*)

## 1. Deskripsi Kasus

### 1.1 Latar Belakang

Permasalahan *Airline Travel Problem* merupakan permasalahan pencarian rute penerbangan dari kota asal menuju kota tujuan dengan mempertimbangkan biaya perjalanan. Terdapat beberapa alternatif rute yang dapat dipilih, baik melalui penerbangan langsung maupun melalui kota transit.

Pada implementasi ini, algoritma **Iterative Deepening A* (IDA*)** digunakan untuk mencari rute penerbangan dari Medan menuju Bali berdasarkan biaya tiket pada setiap jalur penerbangan dan nilai heuristik masing-masing kota.

IDA* merupakan algoritma *informed search* yang menggabungkan evaluasi biaya seperti pada A* dengan pendekatan pencarian mendalam yang menggunakan batas nilai evaluasi (*threshold*). Algoritma ini mengulangi pencarian dengan menaikkan threshold apabila tujuan belum ditemukan.

### 1.2 Tujuan

Tujuan implementasi ini adalah:

1. Mengimplementasikan algoritma IDA* menggunakan bahasa pemrograman Python.
2. Menemukan rute penerbangan dari kota asal menuju kota tujuan.
3. Menghitung total biaya penerbangan berdasarkan jalur yang ditemukan.
4. Memahami proses pencarian menggunakan nilai evaluasi dan threshold.
5. Mengidentifikasi kelebihan dan kekurangan algoritma IDA*.

## 2. Formulasi Masalah

### 2.1 Initial State

Kota awal adalah A, yaitu Medan.

### 2.2 Goal State

Kota tujuan adalah G, yaitu Bali.

### 2.3 Actions

Aksi yang dapat dilakukan adalah berpindah dari suatu kota ke kota lain melalui rute penerbangan yang tersedia pada graf.

### 2.4 Path Cost

Biaya perjalanan merupakan akumulasi biaya penerbangan dari kota awal hingga kota yang sedang dikunjungi.

Nilai biaya aktual perjalanan dinyatakan dengan:

`g(n) = total biaya perjalanan dari start menuju node n`

### 2.5 Heuristic Function

Fungsi heuristik merupakan estimasi biaya dari kota saat ini menuju kota tujuan.

Nilai heuristik yang digunakan:

| Node | Kota       | Heuristik h(n) |
| ---- | ---------- | -------------: |
| A    | Medan      |             10 |
| B    | Palembang  |              8 |
| C    | Jakarta    |              6 |
| D    | Surabaya   |              3 |
| E    | Yogyakarta |              5 |
| G    | Bali       |              0 |

### 2.6 Graf dan Biaya Penerbangan

Graf direpresentasikan sebagai kumpulan node yang terhubung oleh sisi berbobot. Setiap sisi menunjukkan rute penerbangan dan biaya tiketnya.

| Rute  | Biaya |
| ----- | ----: |
| A → B |     1 |
| A → C |     4 |
| B → D |     2 |
| B → E |     1 |
| B → G |    12 |
| C → D |     2 |
| D → G |     3 |
| E → G |     6 |

## 3. Dasar Algoritma IDA*

IDA* menggunakan fungsi evaluasi:

`f(n) = g(n) + h(n)`

Keterangan:

* `f(n)` adalah nilai evaluasi total untuk node n.
* `g(n)` adalah biaya aktual dari node awal menuju node n.
* `h(n)` adalah estimasi biaya dari node n menuju tujuan.

IDA* memulai pencarian dengan threshold awal sebesar nilai heuristik node awal. Selama pencarian, node dengan nilai `f(n)` yang melebihi threshold tidak dieksplorasi lebih lanjut pada iterasi tersebut.

Apabila tujuan belum ditemukan, algoritma menentukan nilai `f(n)` terkecil yang melampaui threshold sebelumnya. Nilai tersebut digunakan sebagai threshold pada iterasi selanjutnya.

Proses berulang hingga tujuan ditemukan atau tidak ada lagi node yang dapat dieksplorasi.

## 4. Implementasi Program

Program ditulis menggunakan bahasa Python dengan graf dan nilai heuristik sebagai data masukan.

```python
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 1, 'G': 12},
    'C': {'D': 2},
    'D': {'G': 3},
    'E': {'G': 6},
    'G': {}
}

heuristic = {
    'A': 10,
    'B': 8,
    'C': 6,
    'D': 3,
    'E': 5,
    'G': 0
}

start = 'A'
goal = 'G'


def search(node, cost, path, threshold):
    f = cost + heuristic[node]

    print(f"  Kunjungi {node}: g={cost}, h={heuristic[node]}, f={f}")

    if f > threshold:
        return f, None

    if node == goal:
        return f, (path, cost)

    min_exceeded = float('inf')

    for neighbor, edge_cost in graph[node].items():
        if neighbor in path:
            continue

        next_threshold, solution = search(
            neighbor,
            cost + edge_cost,
            path + [neighbor],
            threshold
        )

        if solution is not None:
            return next_threshold, solution

        min_exceeded = min(min_exceeded, next_threshold)

    return min_exceeded, None


def ida_star():
    threshold = heuristic[start]

    while True:
        print(f"\nThreshold = {threshold}")

        next_threshold, solution = search(
            start, 0, [start], threshold
        )

        if solution is not None:
            path, total_cost = solution
            return path, total_cost

        if next_threshold == float('inf'):
            return None, None

        threshold = next_threshold


path, total_cost = ida_star()

print("\n=== HASIL IDA* ===")

if path is not None:
    print("Jalur terbaik yang ditemukan:", " -> ".join(path))
    print("Total biaya:", total_cost)
else:
    print("Tidak ditemukan jalur menuju tujuan.")
```

## 5. Alur Logika Program

### 5.1 Mendefinisikan Graf Penerbangan

Program diawali dengan mendefinisikan graf menggunakan struktur dictionary Python.

```python
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 1, 'G': 12},
    'C': {'D': 2},
    'D': {'G': 3},
    'E': {'G': 6},
    'G': {}
}
```

Setiap key merupakan kota asal, sedangkan dictionary di dalamnya berisi kota tujuan dan biaya penerbangan.

Sebagai contoh, `'A': {'B': 1, 'C': 4}` menunjukkan bahwa dari kota A tersedia penerbangan menuju B dengan biaya 1 dan menuju C dengan biaya 4.

Kota G memiliki dictionary kosong karena tidak terdapat rute lanjutan yang didefinisikan dari kota tujuan.

### 5.2 Mendefinisikan Nilai Heuristik

```python
heuristic = {
    'A': 10,
    'B': 8,
    'C': 6,
    'D': 3,
    'E': 5,
    'G': 0
}
```

Dictionary `heuristic` menyimpan estimasi biaya menuju kota tujuan untuk setiap node.

Nilai heuristik digunakan dalam perhitungan fungsi evaluasi `f(n) = g(n) + h(n)`. Pada kota G, nilai heuristik adalah 0 karena kota tersebut merupakan tujuan.

### 5.3 Menentukan Kota Awal dan Tujuan

```python
start = 'A'
goal = 'G'
```

Variabel `start` menunjukkan kota awal, yaitu Medan. Sementara itu, `goal` menunjukkan kota tujuan, yaitu Bali.

Kedua variabel ini digunakan oleh algoritma untuk memulai pencarian dan menentukan kapan tujuan telah tercapai.

### 5.4 Membuat Fungsi Pencarian Rekursif

```python
def search(node, cost, path, threshold):
```

Fungsi `search()` merupakan inti dari implementasi IDA*. Fungsi ini menerima empat parameter:

* `node`: kota yang sedang dikunjungi.
* `cost`: total biaya aktual dari kota awal hingga kota saat ini.
* `path`: daftar kota yang sudah dilalui pada jalur saat ini.
* `threshold`: batas nilai evaluasi yang berlaku pada iterasi pencarian.

Fungsi ini menggunakan rekursi untuk mengeksplorasi rute berikutnya hingga tujuan ditemukan atau jalur tersebut tidak dapat dilanjutkan dalam batas yang berlaku.

### 5.5 Menghitung Nilai Evaluasi

```python
f = cost + heuristic[node]
```

Program menghitung nilai evaluasi berdasarkan jumlah biaya aktual dan estimasi biaya menuju tujuan.

Contohnya, ketika program mengunjungi B melalui A → B:

* Biaya aktual `g(B) = 1`.
* Heuristik `h(B) = 8`.
* Nilai evaluasi `f(B) = 1 + 8 = 9`.

Nilai tersebut kemudian dibandingkan dengan threshold yang sedang digunakan.

### 5.6 Menampilkan Proses Pencarian

```python
print(f"  Kunjungi {node}: g={cost}, h={heuristic[node]}, f={f}")
```

Perintah `print()` menampilkan node yang sedang diproses beserta nilai biaya aktual, heuristik, dan evaluasinya.

Informasi ini digunakan untuk mengamati urutan eksplorasi dan memahami keputusan algoritma selama pencarian.

### 5.7 Memeriksa Threshold

```python
if f > threshold:
    return f, None
```

Jika nilai evaluasi node melebihi threshold, node tersebut tidak dieksplorasi lebih lanjut pada iterasi saat ini.

Fungsi mengembalikan nilai `f` sebagai kandidat threshold berikutnya dan `None` karena belum ditemukan solusi melalui jalur tersebut.

Jika nilai evaluasi masih berada dalam batas, pencarian dapat dilanjutkan.

### 5.8 Memeriksa Apakah Tujuan Telah Dicapai

```python
if node == goal:
    return f, (path, cost)
```

Setelah node lolos pemeriksaan threshold, program memeriksa apakah node tersebut sama dengan kota tujuan.

Jika benar, pencarian berhasil. Fungsi mengembalikan jalur yang ditemukan dan total biaya aktualnya.

Urutan pemeriksaan ini penting agar node tujuan yang nilai evaluasinya melebihi threshold tidak langsung diterima sebagai solusi pada iterasi tersebut.

### 5.9 Menyiapkan Nilai Threshold Berikutnya

```python
min_exceeded = float('inf')
```

Variabel `min_exceeded` digunakan untuk menyimpan nilai evaluasi terkecil yang melampaui threshold selama eksplorasi cabang-cabang pencarian.

Nilai awalnya adalah tak hingga (`inf`) karena belum ada nilai kandidat yang ditemukan.

### 5.10 Mengeksplorasi Kota Tetangga

```python
for neighbor, edge_cost in graph[node].items():
```

Perulangan ini mengambil setiap kota tetangga yang dapat dicapai dari node saat ini beserta biaya penerbangannya.

Sebagai contoh, ketika node saat ini adalah A, program akan mempertimbangkan B dan C sesuai urutan yang didefinisikan dalam graf.

### 5.11 Menghindari Siklus pada Jalur Saat Ini

```python
if neighbor in path:
    continue
```

Bagian ini memeriksa apakah kota tetangga sudah terdapat pada jalur yang sedang dibentuk.

Jika kota tersebut sudah pernah dilewati dalam jalur saat ini, program melewati tetangga tersebut untuk menghindari siklus berulang pada jalur yang sama.

Pemeriksaan ini tidak menghapus kemungkinan mengunjungi kota yang sama melalui jalur alternatif pada cabang pencarian yang berbeda.

### 5.12 Memanggil Pencarian secara Rekursif

```python
next_threshold, solution = search(
    neighbor,
    cost + edge_cost,
    path + [neighbor],
    threshold
)
```

Program memanggil kembali fungsi `search()` untuk mengeksplorasi kota tetangga.

Biaya aktual diperbarui dengan menambahkan biaya penerbangan pada sisi yang dilalui. Jalur juga diperbarui dengan menambahkan kota tetangga tersebut.

Threshold tetap sama selama satu iterasi pencarian. Setiap pemanggilan rekursif menerapkan batas yang sama agar pencarian dalam iterasi tersebut konsisten.

### 5.13 Mengembalikan Solusi yang Ditemukan

```python
if solution is not None:
    return next_threshold, solution
```

Jika pencarian rekursif menemukan tujuan, solusi langsung dikembalikan ke pemanggilnya.

Dengan demikian, pencarian dapat berhenti tanpa harus mengeksplorasi seluruh cabang lainnya pada iterasi tersebut.

### 5.14 Memilih Threshold Berikutnya

```python
min_exceeded = min(min_exceeded, next_threshold)
```

Jika suatu cabang belum menghasilkan solusi, program membandingkan nilai threshold kandidat yang dikembalikan dengan kandidat minimum yang sudah tersimpan.

Program mempertahankan nilai terkecil di antara kandidat yang melampaui threshold. Nilai ini digunakan agar iterasi berikutnya dimulai pada batas evaluasi berikutnya yang relevan.

Setelah seluruh tetangga diperiksa, fungsi mengembalikan:

```python
return min_exceeded, None
```

Jika tidak ditemukan solusi pada iterasi saat ini, fungsi mengembalikan kandidat threshold berikutnya dan menandakan bahwa solusi belum ditemukan.

### 5.15 Memulai Algoritma IDA*

```python
def ida_star():
    threshold = heuristic[start]
```

Fungsi `ida_star()` mengatur proses pencarian secara keseluruhan.

Threshold awal diambil dari heuristik kota awal. Pada kasus ini, threshold pertama adalah 10 karena `heuristic['A'] = 10`.

### 5.16 Mengulang Pencarian

```python
while True:
    print(f"\nThreshold = {threshold}")

    next_threshold, solution = search(
        start, 0, [start], threshold
    )
```

Perulangan menjalankan pencarian dari kota awal dengan biaya awal 0 dan jalur yang hanya berisi A.

Pada setiap iterasi, algoritma menggunakan threshold yang berlaku saat itu. Jika tujuan ditemukan, jalur dan total biayanya dikembalikan.

Jika belum ditemukan, algoritma memeriksa apakah masih ada kandidat threshold untuk pencarian berikutnya.

### 5.17 Menghentikan Pencarian

```python
if solution is not None:
    path, total_cost = solution
    return path, total_cost
```

Jika solusi ditemukan, program mengembalikan jalur dan total biaya aktualnya.

Jika tidak ada kandidat threshold berikutnya:

```python
if next_threshold == float('inf'):
    return None, None
```

Program mengembalikan `None` untuk menandakan bahwa tidak ditemukan solusi yang dapat dilanjutkan berdasarkan proses pencarian.

Jika masih terdapat kandidat threshold, batas diperbarui:

```python
threshold = next_threshold
```

Kemudian pencarian diulang dari kota awal dengan threshold baru.

### 5.18 Menampilkan Hasil Akhir

```python
path, total_cost = ida_star()
```

Program menjalankan algoritma dan menyimpan hasilnya dalam variabel `path` serta `total_cost`.

Jika jalur ditemukan, program menampilkan urutan kota dan total biaya penerbangan. Jika tidak, program menampilkan pesan bahwa tidak ditemukan jalur menuju tujuan.

## 6. Simulasi Proses Pencarian

### 6.1 Threshold Awal

Threshold awal adalah:

`threshold = h(A) = 10`

Pencarian dimulai dari A dengan biaya aktual 0.

| Node | Jalur         | g(n) | h(n) | f(n) | Keputusan        |
| ---- | ------------- | ---: | ---: | ---: | ---------------- |
| A    | A             |    0 |   10 |   10 | Dieksplorasi     |
| B    | A → B         |    1 |    8 |    9 | Dieksplorasi     |
| D    | A → B → D     |    3 |    3 |    6 | Dieksplorasi     |
| G    | A → B → D → G |    6 |    0 |    6 | Tujuan ditemukan |

Node G ditemukan sebelum threshold perlu dinaikkan. Oleh karena itu, program berhenti pada iterasi pertama.

### 6.2 Menghitung Total Biaya

Jalur yang ditemukan adalah:

`A → B → D → G`

Biaya aktualnya:

`g(G) = biaya(A → B) + biaya(B → D) + biaya(D → G)`

`g(G) = 1 + 2 + 3 = 6`

Dengan demikian, total biaya jalur yang ditemukan adalah 6 satuan biaya.

### 6.3 Output Program

Output utama yang diharapkan dari implementasi ini adalah:

```text
Threshold = 10
  Kunjungi A: g=0, h=10, f=10
  Kunjungi B: g=1, h=8, f=9
  Kunjungi D: g=3, h=3, f=6
  Kunjungi G: g=6, h=0, f=6

=== HASIL IDA* ===
Jalur terbaik yang ditemukan: A -> B -> D -> G
Total biaya: 6
```

Output menunjukkan bahwa algoritma menemukan jalur A → B → D → G dengan total biaya 6.

## 7. Kelebihan Algoritma IDA*

### 7.1 Penggunaan Memori Relatif Hemat

IDA* menggunakan pendekatan pencarian mendalam secara rekursif dan tidak perlu menyimpan seluruh node yang dihasilkan dalam struktur antrean seperti pada A* konvensional.

Hal ini membuat IDA* cocok dipertimbangkan pada permasalahan pencarian dengan keterbatasan memori.

### 7.2 Memanfaatkan Informasi Heuristik

IDA* menggunakan fungsi heuristik untuk memperkirakan biaya yang diperlukan menuju tujuan. Informasi ini membantu menentukan node yang masih layak dieksplorasi berdasarkan threshold.

Dengan demikian, pencarian tidak hanya mengandalkan biaya aktual yang sudah ditempuh.

### 7.3 Struktur Algoritma Relatif Sederhana

IDA* memiliki struktur utama berupa pencarian rekursif, pemeriksaan threshold, dan pengulangan dengan threshold baru.

Struktur ini relatif mudah dipisahkan menjadi fungsi-fungsi kecil sehingga proses implementasi, pengujian, dan penelusuran kesalahan dapat dilakukan secara bertahap.

## 8. Kekurangan Algoritma IDA*

### 8.1 Melakukan Eksplorasi Ulang

Setiap kali threshold dinaikkan, pencarian dimulai kembali dari node awal.

Akibatnya, node yang sebelumnya sudah dieksplorasi dapat dikunjungi kembali. Pengulangan ini dapat meningkatkan waktu eksekusi.

### 8.2 Sensitif terhadap Kualitas Heuristik

Kualitas heuristik memengaruhi urutan dan jumlah node yang perlu dieksplorasi.

Heuristik yang kurang informatif dapat menyebabkan pencarian mengeksplorasi banyak node. Selain itu, jaminan optimalitas IDA* bergantung pada asumsi heuristik dan karakteristik biaya yang digunakan.

### 8.3 Dapat Mengalami Waktu Pencarian yang Tinggi

Walaupun penggunaan memorinya relatif hemat, IDA* dapat memerlukan waktu yang besar ketika ruang pencarian luas dan banyak node perlu diperiksa berulang kali.

Oleh sebab itu, penggunaan IDA* perlu mempertimbangkan ukuran graf, pola biaya, dan kualitas heuristik.

## 9. Evaluasi Heuristik pada Kasus

Nilai heuristik pada kasus ini digunakan sesuai tabel soal. Namun, nilai tersebut perlu diperiksa sebelum hasil program dinyatakan sebagai solusi optimal.

Untuk menjamin optimalitas IDA* pada permasalahan biaya nonnegatif, heuristik pada umumnya perlu bersifat *admissible*, yaitu tidak melebih-lebihkan biaya minimum sebenarnya dari setiap node menuju tujuan.

Berdasarkan graf yang diberikan:

| Node | Heuristik h(n) | Biaya minimum aktual menuju G |
| ---- | -------------: | ----------------------------: |
| A    |             10 |                             6 |
| B    |              8 |                             5 |
| C    |              6 |                             5 |
| D    |              3 |                             3 |
| E    |              5 |                             6 |
| G    |              0 |                             0 |

Nilai biaya minimum aktual diperoleh dari rute-rute yang tersedia pada graf. Sebagai contoh, biaya minimum dari B menuju G adalah 5 melalui B → D → G.

Tabel menunjukkan bahwa heuristik pada A, B, dan C melebihi biaya minimum aktual menuju G. Oleh karena itu, heuristik yang diberikan **tidak admissible**.

Akibatnya, walaupun program menemukan jalur dengan biaya 6 pada iterasi pertama, hasil tersebut tidak boleh dinyatakan optimal hanya berdasarkan jaminan teoretis IDA*. Dalam kasus ini, jalur tersebut memang memiliki biaya minimum di antara jalur yang tercantum, tetapi kesimpulan tersebut diperoleh dengan memeriksa biaya rute yang tersedia.

## 10. Kesimpulan

Algoritma Iterative Deepening A* (IDA*) berhasil diimplementasikan menggunakan Python untuk mencari rute penerbangan dari Medan menuju Bali. Program menggunakan graf berbobot, nilai heuristik, fungsi evaluasi `f(n) = g(n) + h(n)`, serta threshold untuk mengendalikan eksplorasi.

Pada data dan urutan eksplorasi yang digunakan, program menemukan jalur A → B → D → G dengan total biaya 6 satuan biaya. Proses pencarian selesai pada threshold awal sebesar 10 karena tujuan ditemukan sebelum threshold perlu dinaikkan.

IDA* memiliki keunggulan dalam penggunaan memori yang relatif hemat dan struktur pencarian yang teratur. Namun, algoritma ini dapat mengulang eksplorasi node sehingga waktu pencariannya meningkat. Selain itu, kualitas heuristik memengaruhi efisiensi pencarian dan jaminan optimalitas.

Pada kasus ini, heuristik yang diberikan tidak admissible karena beberapa nilainya melebihi biaya minimum aktual menuju tujuan. Oleh sebab itu, hasil program perlu dianalisis bersama data graf, dan optimalitasnya tidak dapat dijamin hanya berdasarkan sifat umum IDA*.

## 11. Referensi

* Materi perkuliahan *Informed Search (Heuristic) & Eksplorasinya*, Konsep Kecerdasan Artifisial, Departemen Teknik Informatika.
* Materi perkuliahan *Informed Search problem and solution*, contoh pengerjaan algoritma IDA*.
