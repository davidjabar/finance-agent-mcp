from enum import Enum


class TransactionCategory(str, Enum):
    TRANSPORTASI = "Transportasi"
    MAKAN = "Makan"
    BELANJA_PRIMER = "Belanja Kebutuhan Primer"
    BELANJA_SEKUNDER = "Belanja Kebutuhan Sekunder"
    TAGIHAN = "Bayar Tagihan"
    KESEHATAN = "Kesehatan"
    HIBURAN = "Hiburan"
    PENDIDIKAN = "Pendidikan"
    GAJI = "Gaji"
    BONUS = "Bonus/Hadiah"
    INVESTASI = "Investasi"
    LAINNYA = "Lainnya"