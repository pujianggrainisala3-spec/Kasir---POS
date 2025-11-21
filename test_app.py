import unittest
from unittest.mock import MagicMock, patch
import database
import auth
import admin
import cashier

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

    def test_database_connection_success(self):
        # Test that get_db_connection returns the mock when passed
        conn = database.get_db_connection(mock_db=self.mock_conn)
        self.assertEqual(conn, self.mock_conn)

    @patch('builtins.input', side_effect=['admin', 'admin'])
    def test_login_success(self, mock_input):
        # Setup mock return for fetch_query inside auth.login
        # It expects a list of dicts
        self.mock_cursor.fetchall.return_value = [{
            'id_karyawan': 'K01', 
            'role_karyawan': 'admin', 
            'username_login': 'admin',
            'password_login': 'admin'
        }]
        
        role, uid, username = auth.login(self.mock_conn)
        
        self.assertEqual(role, 'admin')
        self.assertEqual(uid, 'K01')
        self.assertEqual(username, 'admin')

    @patch('builtins.input', side_effect=['wrong', 'pass'])
    def test_login_fail(self, mock_input):
        self.mock_cursor.fetchall.return_value = []
        
        role, uid, username = auth.login(self.mock_conn)
        
        self.assertIsNone(role)

    @patch('builtins.input', side_effect=['1', '5']) # 1: View, 5: Exit
    @patch('sys.stdout') # Suppress print output
    def test_admin_menu_view(self, mock_stdout, mock_input):
        # Mock fetch_query for view_products
        self.mock_cursor.fetchall.return_value = [
            {'id_produk': 'P01', 'nama_produk': 'Tes', 'kategori_produk': 'Makanan', 'harga': 1000, 'stok': 10}
        ]
        
        admin.admin_menu(self.mock_conn)
        
        # Check if query was executed
        self.mock_cursor.execute.assert_any_call("SELECT * FROM tb_produk")

    @patch('builtins.input', side_effect=['P02', 'Baru', 'Minuman', '5000', '20'])
    def test_admin_add_product(self, mock_input):
        admin.add_product(self.mock_conn)
        
        # Verify INSERT called
        expected_query = "INSERT INTO tb_produk (id_produk, nama_produk, kategori_produk, harga, stok) VALUES (%s, %s, %s, %s, %s)"
        expected_params = ('P02', 'Baru', 'Minuman', 5000, 20)
        self.mock_cursor.execute.assert_called_with(expected_query, expected_params)

    @patch('builtins.input', side_effect=['P01', '1', 'selesai', '1', '5000']) # Product P01, qty 1, finish, Cash, Pay 5000
    def test_cashier_transaction_cash(self, mock_input):
        # Mock product fetch
        self.mock_cursor.fetchall.return_value = [
            {'id_produk': 'P01', 'nama_produk': 'Tes', 'kategori_produk': 'Makanan', 'harga': 3000, 'stok': 10}
        ]
        
        cashier.process_transaction(self.mock_conn, 'K02')
        
        # Verify inserts
        # 1. tb_metode_pembayaran
        # 2. tb_pemesanan
        # 3. tb_detail_pemesanan
        # 4. Update stock
        
        # We can check if commit was called
        self.mock_conn.commit.assert_called()
        
        # Check for update stock call
        update_calls = [call for call in self.mock_cursor.execute.call_args_list if "UPDATE tb_produk" in call[0][0]]
        self.assertTrue(len(update_calls) > 0)

if __name__ == '__main__':
    unittest.main()
