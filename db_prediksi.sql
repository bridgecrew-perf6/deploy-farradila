-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2022 at 11:13 AM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_prediksi`
--

-- --------------------------------------------------------

--
-- Table structure for table `kesiapan`
--

CREATE TABLE `kesiapan` (
  `id_kesiapan` int(10) NOT NULL,
  `tahun` varchar(10) NOT NULL,
  `bulan` varchar(10) NOT NULL,
  `nilai_kekuatan` int(10) NOT NULL,
  `nilai_pemeliharaan` int(10) NOT NULL,
  `nilai_kesiapan` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kesiapan`
--

INSERT INTO `kesiapan` (`id_kesiapan`, `tahun`, `bulan`, `nilai_kekuatan`, `nilai_pemeliharaan`, `nilai_kesiapan`) VALUES
(1, '2016', 'Januari', 230, 7, 213),
(2, '2016', 'Februari', 220, 8, 187),
(3, '2016', 'Maret', 229, 6, 203),
(4, '2016', 'April', 230, 7, 200),
(5, '2016', 'Mei', 228, 9, 220),
(6, '2016', 'Juni', 222, 18, 218),
(7, '2016', 'Juli', 226, 16, 205),
(8, '2016', 'Agustus', 230, 16, 213),
(9, '2016', 'September', 229, 20, 187),
(10, '2016', 'Oktober', 227, 4, 201),
(11, '2016', 'November', 221, 10, 195),
(12, '2016', 'Desember', 221, 17, 208),
(13, '2017', 'Januari', 250, 4, 215),
(14, '2017', 'Februari', 243, 6, 213),
(15, '2017', 'Maret', 239, 4, 214),
(16, '2017', 'April', 231, 11, 207),
(17, '2017', 'Mei', 237, 17, 213),
(18, '2017', 'Juni', 236, 17, 205),
(19, '2017', 'Juli', 240, 5, 212),
(20, '2017', 'Agustus', 246, 16, 223),
(21, '2017', 'September', 235, 12, 214),
(22, '2017', 'Oktober', 242, 17, 217),
(23, '2017', 'November', 230, 20, 197),
(24, '2017', 'Desember', 236, 10, 211),
(25, '2018', 'Januari', 239, 7, 212),
(26, '2018', 'Februari', 241, 8, 203),
(27, '2018', 'Maret', 250, 6, 226),
(28, '2018', 'April', 234, 5, 201),
(29, '2018', 'Mei', 245, 19, 216),
(30, '2018', 'Juni', 247, 14, 216),
(31, '2018', 'Juli', 241, 10, 214),
(32, '2018', 'Agustus', 244, 15, 216),
(33, '2018', 'September', 239, 12, 209),
(34, '2018', 'Oktober', 240, 20, 209),
(35, '2018', 'November', 247, 10, 218),
(36, '2018', 'Desember', 249, 6, 231),
(37, '2019', 'Januari', 256, 8, 230),
(38, '2019', 'Februari', 258, 4, 235),
(39, '2019', 'Maret', 250, 19, 217),
(40, '2019', 'April', 250, 8, 226),
(41, '2019', 'Mei', 262, 16, 244),
(42, '2019', 'Juni', 267, 8, 250),
(43, '2019', 'Juli', 255, 5, 232),
(44, '2019', 'Agustus', 267, 4, 245),
(45, '2019', 'September', 266, 19, 240),
(46, '2019', 'Oktober', 261, 8, 242),
(47, '2019', 'November', 254, 11, 232),
(48, '2019', 'Desember', 265, 12, 242),
(49, '2020', 'Januari', 293, 9, 270),
(50, '2020', 'Februari', 312, 17, 289),
(51, '2020', 'Maret', 299, 12, 286),
(52, '2020', 'April', 293, 14, 276),
(53, '2020', 'Mei', 315, 8, 293),
(54, '2020', 'Juni', 303, 16, 289),
(55, '2020', 'Juli', 310, 5, 293),
(56, '2020', 'Agustus', 312, 18, 290),
(57, '2020', 'September', 301, 16, 292),
(58, '2020', 'Oktober', 300, 12, 285),
(59, '2020', 'November', 299, 4, 292),
(60, '2020', 'Desember', 296, 8, 288),
(61, '2021', 'Januari', 340, 18, 309),
(62, '2021', 'Februari', 325, 20, 282),
(63, '2021', 'Maret', 339, 13, 296),
(64, '2021', 'April', 322, 10, 304),
(65, '2021', 'Mei', 336, 10, 303),
(66, '2021', 'Juni', 327, 8, 319),
(67, '2021', 'Juli', 320, 6, 311),
(68, '2021', 'Agustus', 326, 12, 319),
(69, '2021', 'September', 335, 5, 315),
(70, '2021', 'Oktober', 325, 8, 301),
(71, '2021', 'November', 330, 13, 311),
(72, '2021', 'Desember', 332, 13, 308),
(73, '2022', 'Januari', 331, 7, 300),
(74, '2022', 'Februari', 344, 19, 291),
(75, '2022', 'Maret', 333, 20, 304),
(76, '2022', 'April', 338, 4, 317),
(77, '2022', 'Mei', 339, 16, 299),
(78, '2022', 'Juni', 335, 15, 315),
(79, '2022', 'Juli', 341, 4, 318),
(80, '2022', 'Agustus', 326, 20, 302),
(81, '2022', 'September', 338, 9, 287),
(82, '2022', 'Oktober', 344, 5, 326),
(83, '2022', 'November', 335, 6, 317),
(84, '2022', 'Desember', 346, 11, 297),
(86, '2023', 'Januari', 361, 15, 302),
(87, '2023', 'Februari', 361, 13, 303),
(88, '2023', 'Maret', 346, 9, 312),
(89, '2023', 'April', 361, 8, 298),
(90, '2023', 'Mei', 364, 14, 304),
(91, '2023', 'Juni', 358, 19, 307),
(92, '2023', 'Juli', 365, 16, 312),
(93, '2023', 'Agustus', 355, 18, 294),
(94, '2023', 'September', 355, 16, 310),
(95, '2023', 'Oktober', 359, 14, 314),
(96, '2023', 'Nopember', 362, 16, 301),
(97, '2023', 'Desember', 360, 10, 300);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `level` enum('admin','user') NOT NULL,
  `confirmed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `username`, `email`, `password`, `level`, `confirmed`) VALUES
(1, 'Farradila', 'farradila429@gmail.com', 'farradila', 'admin', 1),
(20, 'Farra', '1841720074@student.polinema.ac.id', 'farra', 'admin', 1),
(23, 'User', '1841720074@student.polinema.ac.id', 'user', 'user', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kesiapan`
--
ALTER TABLE `kesiapan`
  ADD PRIMARY KEY (`id_kesiapan`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kesiapan`
--
ALTER TABLE `kesiapan`
  MODIFY `id_kesiapan` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
