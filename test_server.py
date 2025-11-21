import unittest
from unittest.mock import patch
import json
from server import app

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('db_utils.get_all_produk')
    def test_get_products(self, mock_get_all_produk):
        mock_get_all_produk.return_value = [{'id_produk': 'P001', 'nama_produk': 'Nasi Kucing'}]
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertEqual(len(response.json), 1)

    @patch('db_utils.get_all_employees')
    def test_get_employees(self, mock_get_all_employees):
        mock_get_all_employees.return_value = [{'id_karyawan': 'K01', 'username_login': 'admin'}]
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertEqual(len(response.json), 1)

    @patch('db_utils.get_sales_stats')
    def test_get_stats(self, mock_get_sales_stats):
        mock_get_sales_stats.return_value = {'total_transactions': 10, 'total_revenue': 100000}
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_transactions', response.json)
        self.assertIn('total_revenue', response.json)

    @patch('db_utils.get_laporan_penjualan')
    def test_get_reports(self, mock_get_laporan_penjualan):
        mock_get_laporan_penjualan.return_value = [{'id_transaksi': 'TRX001', 'total_harga': 5000}]
        response = self.app.get('/reports')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertEqual(len(response.json), 1)

if __name__ == '__main__':
    unittest.main()
