from flask import Flask, jsonify, request
from flask_cors import CORS
import db_utils as db

app = Flask(__name__)
CORS(app)

@app.route('/products', methods=['GET'])
def get_products():
    products = db.get_all_produk()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    db.insert_produk(data['id_produk'], data['nama_produk'], data['kategori_produk'], data['harga'], data['stok'])
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    db.update_produk(product_id, data['nama_produk'], data['kategori_produk'], data['harga'], data['stok'])
    return jsonify({'message': 'Product updated successfully'}), 200

@app.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    db.delete_produk(product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db.get_user_by_credentials(username, password)

    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = db.get_all_employees()
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    db.insert_employee(data['id_karyawan'], data['role'], data['username'], data['password'])
    return jsonify({'message': 'Employee added successfully'}), 201

@app.route('/employees/<string:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    db.update_employee(employee_id, data['role'], data['username'], data['password'])
    return jsonify({'message': 'Employee updated successfully'}), 200

@app.route('/employees/<string:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    db.delete_employee(employee_id)
    return jsonify({'message': 'Employee deleted successfully'}), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    stats = db.get_sales_stats()
    return jsonify(stats)

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = db.get_laporan_penjualan()
    return jsonify(reports)

@app.route('/history/<string:id_karyawan>', methods=['GET'])
def get_history(id_karyawan):
    history = db.get_transaction_history_by_cashier(id_karyawan)
    return jsonify(history)

@app.route('/transactions', methods=['POST'])
def process_transaction():
    data = request.get_json()
    id_karyawan = data.get('id_karyawan')
    keranjang = data.get('keranjang')
    total_harga = data.get('total_harga')

    try:
        db.save_transaksi(id_karyawan, keranjang, total_harga)
        for item in keranjang:
            db.update_stok_produk(item['id_produk'], item['jumlah'])
        return jsonify({'message': 'Transaksi berhasil'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
