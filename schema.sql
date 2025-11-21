-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 19, 2025 at 10:10 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_angkringan`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_detail_pemesanan`
--

DROP TABLE IF EXISTS `tb_detail_pemesanan`;
CREATE TABLE `tb_detail_pemesanan` (
  `id_produk` varchar(20) NOT NULL,
  `id_transaksi` varchar(20) DEFAULT NULL,
  `subtotal` int DEFAULT NULL,
  `jumlah` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_karyawan`
--

DROP TABLE IF EXISTS `tb_karyawan`;
CREATE TABLE `tb_karyawan` (
  `id_karyawan` varchar(20) NOT NULL,
  `role_karyawan` varchar(20) DEFAULT NULL,
  `username_login` varchar(20) DEFAULT NULL,
  `password_login` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_metode_pembayaran`
--

DROP TABLE IF EXISTS `tb_metode_pembayaran`;
CREATE TABLE `tb_metode_pembayaran` (
  `id_transaksi` varchar(20) NOT NULL,
  `jenis_transaksi` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_pemesanan`
--

DROP TABLE IF EXISTS `tb_pemesanan`;
CREATE TABLE `tb_pemesanan` (
  `id_transaksi` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `total_harga` int DEFAULT NULL,
  `tanggal_transaksi` date DEFAULT NULL,
  `waktu_transaksi` timestamp NULL DEFAULT NULL,
  `id_karyawan` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_produk`
--

DROP TABLE IF EXISTS `tb_produk`;
CREATE TABLE `tb_produk` (
  `id_produk` varchar(20) NOT NULL,
  `nama_produk` varchar(20) DEFAULT NULL,
  `kategori_produk` varchar(20) DEFAULT NULL,
  `harga` int DEFAULT NULL,
  `stok` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_detail_pemesanan`
--
ALTER TABLE `tb_detail_pemesanan`
  ADD KEY `id_transaksi` (`id_transaksi`),
  ADD KEY `id_produk` (`id_produk`);

--
-- Indexes for table `tb_karyawan`
--
ALTER TABLE `tb_karyawan`
  ADD PRIMARY KEY (`id_karyawan`);

--
-- Indexes for table `tb_metode_pembayaran`
--
ALTER TABLE `tb_metode_pembayaran`
  ADD PRIMARY KEY (`id_transaksi`);

--
-- Indexes for table `tb_pemesanan`
--
ALTER TABLE `tb_pemesanan`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_karyawan` (`id_karyawan`);

--
-- Indexes for table `tb_produk`
--
ALTER TABLE `tb_produk`
  ADD PRIMARY KEY (`id_produk`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_detail_pemesanan`
--
ALTER TABLE `tb_detail_pemesanan`
  ADD CONSTRAINT `tb_detail_pemesanan_ibfk_1` FOREIGN KEY (`id_transaksi`) REFERENCES `tb_pemesanan` (`id_transaksi`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `tb_detail_pemesanan_ibfk_2` FOREIGN KEY (`id_produk`) REFERENCES `tb_produk` (`id_produk`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `tb_pemesanan`
--
ALTER TABLE `tb_pemesanan`
  ADD CONSTRAINT `tb_pemesanan_ibfk_1` FOREIGN KEY (`id_karyawan`) REFERENCES `tb_karyawan` (`id_karyawan`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `tb_pemesanan_ibfk_2` FOREIGN KEY (`id_transaksi`) REFERENCES `tb_metode_pembayaran` (`id_transaksi`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- DUMPING DATA (SEED)
--

INSERT INTO `tb_karyawan` (`id_karyawan`, `role_karyawan`, `username_login`, `password_login`) VALUES
('K01', 'admin', 'admin', 'admin'),
('K02', 'kasir', 'kasir', 'kasir');

INSERT INTO `tb_produk` (`id_produk`, `nama_produk`, `kategori_produk`, `harga`, `stok`) VALUES
('P001', 'Nasi Kucing', 'Makanan', 3000, 50),
('P002', 'Sate Usus', 'Makanan', 2000, 50),
('P003', 'Es Teh', 'Minuman', 3000, 50),
('P004', 'Kopi Hitam', 'Minuman', 4000, 50);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
