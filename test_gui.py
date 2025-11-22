import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from gui import AngkringanApp

class TestGUI(unittest.TestCase):

    def setUp(self):
        # We need a root window to create the AngkringanApp, but we don't want it to show up.
        # So we create it and immediately withdraw it.
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = AngkringanApp(self.root)

    def tearDown(self):
        # Destroy the root window after each test.
        self.root.destroy()

    @patch('gui.db')
    @patch('gui.messagebox')
    def test_add_menu_screen_submit_success(self, mock_messagebox, mock_db):
        """
        Tests that the submit logic in the add menu screen correctly calls the database
        and shows a success message when the database operation is successful.
        """
        # We need to navigate to the add menu screen to create the necessary tk variables
        self.app.add_menu_screen()

        # Simulate user input by setting the tk variables
        self.app.id_var.set("P001")
        self.app.nama_var.set("Test Produk")
        self.app.kategori_var.set("Test Kategori")
        self.app.harga_var.set(1000)
        self.app.stok_var.set(10)

        # Mock the create_main_menu method to prevent it from creating UI elements
        self.app.create_main_menu = MagicMock()

        # Call the private submit method directly to test the logic without UI interaction
        self.app._submit_add_menu()

        # Assert that the database insert method was called with the correct data
        mock_db.insert_produk.assert_called_once_with("P001", "Test Produk", "Test Kategori", 1000, 10)

        # Assert that the success message was shown to the user
        mock_messagebox.showinfo.assert_called_once_with("Sukses", "Produk berhasil ditambahkan!")

        # Assert that the app navigates back to the main menu
        self.app.create_main_menu.assert_called_once()

    @patch('gui.db')
    @patch('gui.messagebox')
    def test_add_menu_screen_submit_error(self, mock_messagebox, mock_db):
        """
        Tests that the submit logic in the add menu screen shows an error message
        when the database operation fails.
        """
        self.app.add_menu_screen()

        self.app.id_var.set("P001")
        self.app.nama_var.set("Test Produk")
        self.app.kategori_var.set("Test Kategori")
        self.app.harga_var.set(1000)
        self.app.stok_var.set(10)

        # Simulate a database error
        mock_db.insert_produk.side_effect = Exception("Database error")

        self.app.create_main_menu = MagicMock()

        self.app._submit_add_menu()

        mock_db.insert_produk.assert_called_once_with("P001", "Test Produk", "Test Kategori", 1000, 10)
        mock_messagebox.showerror.assert_called_once_with("Error", "Database error")
        self.app.create_main_menu.assert_not_called()

    @patch('gui.db')
    @patch('gui.messagebox')
    def test_update_menu_screen_submit_success(self, mock_messagebox, mock_db):
        """
        Tests that the submit logic in the update menu screen correctly calls the database
        and shows a success message when the database operation is successful.
        """
        self.app.update_menu_screen()

        self.app.id_var.set("P001")
        self.app.nama_var.set("Test Produk Updated")
        self.app.kategori_var.set("Test Kategori Updated")
        self.app.harga_var.set(2000)
        self.app.stok_var.set(20)

        self.app.create_main_menu = MagicMock()

        self.app._submit_update_menu()

        mock_db.update_produk.assert_called_once_with("P001", "Test Produk Updated", "Test Kategori Updated", 2000, 20)
        mock_messagebox.showinfo.assert_called_once_with("Sukses", "Produk berhasil diupdate!")
        self.app.create_main_menu.assert_called_once()

if __name__ == '__main__':
    unittest.main()
