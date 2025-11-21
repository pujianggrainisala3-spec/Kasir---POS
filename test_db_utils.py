import unittest
from unittest.mock import MagicMock, patch
import db_utils

class TestDBUtils(unittest.TestCase):
    
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        
    @patch('db_utils.get_connection')
    def test_get_produk_by_id(self, mock_get_conn):
        mock_get_conn.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = {'id_produk': 'P001', 'nama_produk': 'Test'}
        
        result = db_utils.get_produk_by_id('P001')
        
        self.assertEqual(result['nama_produk'], 'Test')
        self.mock_cursor.execute.assert_called_with("SELECT * FROM tb_produk WHERE id_produk = %s", ('P001',))

    @patch('db_utils.get_connection')
    def test_save_transaksi_flow(self, mock_get_conn):
        mock_get_conn.return_value = self.mock_conn
        
        keranjang = [
            {'id_produk': 'P001', 'subtotal': 5000, 'jumlah': 2},
            {'id_produk': 'P002', 'subtotal': 3000, 'jumlah': 1}
        ]
        total_harga = 8000
        id_karyawan = 'K02'
        
        id_transaksi = db_utils.save_transaksi(id_karyawan, keranjang, total_harga, jenis_transaksi="Cash")
        
        self.assertTrue(id_transaksi.startswith("TRX"))
        
        # Verify calls
        # 1. Insert Method
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO tb_metode_pembayaran (id_transaksi, jenis_transaksi) VALUES (%s, %s)", 
            (id_transaksi, "Cash")
        )
        
        # 2. Insert Pemesanan (We check if it was called, exact params hard to check due to dynamic dates)
        # But we can check the SQL string
        insert_pemesanan_calls = [c for c in self.mock_cursor.execute.call_args_list if "INSERT INTO tb_pemesanan" in c[0][0]]
        self.assertEqual(len(insert_pemesanan_calls), 1)
        
        # 3. Insert Details & Update Stock (Loop)
        insert_detail_calls = [c for c in self.mock_cursor.execute.call_args_list if "INSERT INTO tb_detail_pemesanan" in c[0][0]]
        self.assertEqual(len(insert_detail_calls), 2)
        
        update_stock_calls = [c for c in self.mock_cursor.execute.call_args_list if "UPDATE tb_produk SET stok" in c[0][0]]
        self.assertEqual(len(update_stock_calls), 2)
        
        self.mock_conn.commit.assert_called()

if __name__ == '__main__':
    unittest.main()
