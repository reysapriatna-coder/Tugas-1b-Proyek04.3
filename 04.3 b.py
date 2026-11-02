class Node:
    """Satu simpul = satu pegawai / jabatan."""

    def __init__(self, id_pegawai, nama, jabatan):
        self.id_pegawai = id_pegawai   # ID unik, contoh: "R001"
        self.nama = nama               # nama pegawai
        self.jabatan = jabatan         # jabatan di organisasi
        self.atasan = None             # pointer ke parent (None jika root)
        self.children = []             # list bawahan (boleh banyak)

    def add_child(self, child):
        child.atasan = self
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def level(self):
        """Level node: root = 0, bawahan langsung root = 1, dst."""
        level, p = 0, self.atasan
        while p is not None:
            level += 1
            p = p.atasan
        return level

    def __str__(self):
        return f"[{self.id_pegawai}] {self.nama} - {self.jabatan}"


class Tree:
    """General Tree: setiap node boleh punya banyak anak."""

    def __init__(self):
        self.root = None               # tree kosong di awal

    def insert_node(self, atasan, id_pegawai, nama, jabatan):
        """Menyisipkan pegawai baru sebagai bawahan dari 'atasan'
        (atasan dicari berdasarkan nama ATAU jabatan secara persis)."""
        # 1. Cegah ID ganda
        if any(n.id_pegawai == id_pegawai for n in self.preorder()):
            print(f"Gagal: ID {id_pegawai} sudah dipakai.")
            return False

        node_baru = Node(id_pegawai, nama, jabatan)

        # 2. Jika tree masih kosong, node pertama menjadi root
        if self.root is None:
            self.root = node_baru
            return True

        # 3. Cari atasan, lalu pasang node baru sebagai anaknya
        hasil = self.search_node(atasan, exact=True)
        if not hasil:
            print(f"Gagal: atasan '{atasan}' tidak ditemukan.")
            return False
        hasil[0].add_child(node_baru)
        return True

    def search_node(self, keyword, exact=False):
        """Mencari pegawai berdasarkan nama atau jabatan.
        Mengembalikan list node yang cocok (kosong jika tidak ada)."""
        hasil = []
        self._cari(self.root, keyword.lower(), exact, hasil)
        return hasil

    def _cari(self, node, keyword, exact, hasil):
        if node is None:                       # base case
            return
        nama, jabatan = node.nama.lower(), node.jabatan.lower()
        if exact:
            cocok = (keyword == nama) or (keyword == jabatan)
        else:
            cocok = (keyword in nama) or (keyword in jabatan)
        if cocok:
            hasil.append(node)
        for child in node.children:            # lanjut ke setiap anak
            self._cari(child, keyword, exact, hasil)

    def preorder(self):
        """Pre-order: NODE -> anak-anak (kiri ke kanan)."""
        hasil = []
        def kunjungi(node):
            if node is None:
                return
            hasil.append(node)                 # 1) kunjungi node dulu
            for child in node.children:        # 2) lalu semua anak
                kunjungi(child)
        kunjungi(self.root)
        return hasil

    def inorder(self):
        """In-order (General Tree): anak PERTAMA -> NODE -> sisa anak.
        (Untuk node dengan <=2 anak ini sama persis dengan kiri-node-kanan.)"""
        hasil = []
        def kunjungi(node):
            if node is None:
                return
            if node.children:
                kunjungi(node.children[0])     # 1) subtree anak pertama
            hasil.append(node)                 # 2) kunjungi node
            for child in node.children[1:]:    # 3) sisa anak
                kunjungi(child)
        kunjungi(self.root)
        return hasil

    def postorder(self):
        """Post-order: semua anak -> NODE."""
        hasil = []
        def kunjungi(node):
            if node is None:
                return
            for child in node.children:        # 1) semua anak dulu
                kunjungi(child)
            hasil.append(node)                 # 2) node paling akhir
        kunjungi(self.root)
        return hasil

    def height(self, node="ROOT"):
        """Tinggi tree = jumlah edge pada jalur terpanjang root -> leaf."""
        if node == "ROOT":
            node = self.root
        if node is None:
            return -1
        if node.is_leaf():
            return 0
        return 1 + max(self.height(c) for c in node.children)

    def count(self):
        return len(self.preorder())

    def tampilkan_struktur(self):
        """Cetak tree dengan indentasi sesuai level (mudah dibaca)."""
        for node in self.preorder():
            print("    " * node.level() + "- " + node.nama)

    def delete_node(self, keyword):
        """(Bonus) Hapus node + seluruh bawahannya (subtree)."""
        hasil = self.search_node(keyword, exact=True)
        if not hasil:
            return False
        target = hasil[0]
        if target is self.root:
            self.root = None
        else:
            target.atasan.children.remove(target)
        return True

def cetak(judul, daftar_node):
    print(f"\n{judul}")
    print(" -> ".join(n.nama for n in daftar_node))


# ============================================================
#  PROGRAM UTAMA (demo)
# ============================================================
if __name__ == "__main__":
    org = Tree()

    # --- Membangun struktur organisasi (insert_node) ---
    org.insert_node(None,            "R001", "Prof. Dr. Hj. Leny Nofianti, M.S., S.E., M.Si., Ak.", "Rektor")
    org.insert_node("Rektor",        "R002", "Prof. Dr. H. Raihani, M.Ed., Ph.D.", "Wakil Rektor I")
    org.insert_node("Rektor",        "R003", "Assoc. Prof. Dr. Alex Wenda, S.T., M.Eng.", "Wakil Rektor II")
    org.insert_node("Rektor",        "R004", "Dr. Harris Simaremare, S.T., M.T.", "Wakil Rektor III")
    org.insert_node("Rektor",        "D001", "Dr. Yuslenita Muda, S.Si., M.Sc.", "Dekan Fakultas Sains dan Teknologi")
    org.insert_node("Dekan Fakultas Sains dan Teknologi", "D002", "Dr. Ir. Kunaifi, S.T., PgDipEnSt., M.Sc.", "Wakil Dekan I")
    org.insert_node("Dekan Fakultas Sains dan Teknologi", "D003", "Dr. Lestari Handayani, S.T., M.Kom", "Wakil Dekan II")
    org.insert_node("Dekan Fakultas Sains dan Teknologi", "D004", "Dr. Alwis Nazir, M.Kom", "Wakil Dekan III")
    org.insert_node("Dekan Fakultas Sains dan Teknologi", "P001", "Muhammad Affandes, S.T., M.T.", "Ketua Program Studi Teknik Informatika")
    org.insert_node("Ketua Program Studi Teknik Informatika", "P002", "Siska Kurnia Gusti, S.T., M.Sc.", "Dosen Teknik Informatika")
    org.insert_node("Ketua Program Studi Teknik Informatika", "P003", "Yusra, S.T., M.T.", "Dosen Teknik Informatika")
    org.insert_node("Ketua Program Studi Teknik Informatika", "P004", "Kurnia Sari, S.T", "Staf Administrasi Prodi")

    print("=== STRUKTUR ORGANISASI ===")
    org.tampilkan_struktur()
    print(f"\nJumlah node : {org.count()}")
    print(f"Tinggi tree : {org.height()}")

    # --- Insert tambahan ---
    print("\n=== INSERT: tambah Kepala Laboratorium di bawah Ketua Prodi ===")
    ok = org.insert_node("Ketua Program Studi Teknik Informatika",
                         "P005", "Suwanto Sanjaya, S.T., M.Kom.", "Kepala Laboratorium Komputer")
    print("Berhasil:", ok)
    print("Atasan tidak ada:", org.insert_node("Rektor Palsu", "X999", "Tes", "Tes"))

    # --- Search ---
    print("\n=== SEARCH ===")
    for kata in ["Affandes", "dosen", "Bupati"]:
        hasil = org.search_node(kata)
        print(f"Cari '{kata}': ", end="")
        print("; ".join(str(n) for n in hasil) if hasil else "tidak ditemukan")

    # --- Traversal ---
    cetak("=== PREORDER  (node -> anak) ===",      org.preorder())
    cetak("=== INORDER   (anak 1 -> node -> sisa anak) ===", org.inorder())
    cetak("=== POSTORDER (anak -> node) ===",      org.postorder())

    # --- Soal 11: struktur organisasi baru ---
    uji = Tree()
    def tambah(atasan, nama):
        uji.insert_node(atasan, f"U{uji.count()+1:02d}", nama, nama)

    tambah(None, "Rektor")
    for x in ["Senat Universitas", "Wakil Rektor I", "Wakil Rektor II",
              "Wakil Rektor III", "Dekan Fakultas Sains dan Teknologi"]:
        tambah("Rektor", x)
    D = "Dekan Fakultas Sains dan Teknologi"
    for x in ["Wakil Dekan I", "Wakil Dekan II", "Wakil Dekan III",
              "Ketua Program Studi Teknik Informatika"]:
        tambah(D, x)
    K = "Ketua Program Studi Teknik Informatika"
    for x in ["Sekretaris Program Studi", "Kepala Laboratorium Komputer", "Koordinator Dosen"]:
        tambah(K, x)
    tambah("Kepala Laboratorium Komputer", "Asisten Laboratorium")
    tambah("Kepala Laboratorium Komputer", "Teknisi Laboratorium")
    tambah("Koordinator Dosen", "Dosen Pembimbing Akademik")
    tambah("Koordinator Dosen", "Dosen Pengampu Mata Kuliah")
    tambah("Dosen Pembimbing Akademik", "Mahasiswa Bimbingan")

    print("\n\n######## SOAL 11 ########")
    uji.tampilkan_struktur()
    cetak("PREORDER",  uji.preorder())
    cetak("INORDER",   uji.inorder())
    cetak("POSTORDER", uji.postorder())