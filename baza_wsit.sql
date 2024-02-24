-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 21, 2024 at 07:22 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wsit`
--

-- --------------------------------------------------------

--
-- Table structure for table `komentari`
--

CREATE TABLE `komentari` (
  `id` int(11) NOT NULL,
  `sadrzaj` varchar(255) DEFAULT NULL,
  `datum_komentarisanja` datetime DEFAULT NULL,
  `Proizvodi_id` int(11) NOT NULL,
  `Korisnici_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `komentari`
--

INSERT INTO `komentari` (`id`, `sadrzaj`, `datum_komentarisanja`, `Proizvodi_id`, `Korisnici_id`) VALUES
(8, 'grmiii', '2024-02-19 14:07:58', 13, 33),
(9, 'odlican proizvod', '2024-02-21 19:17:56', 15, 33);

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(50) CHARACTER SET armscii8 COLLATE armscii8_general_ci DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `godiste` int(11) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `trenutno_stanje_novca` int(11) DEFAULT NULL,
  `tip_korisnika` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `username`, `password`, `email`, `godiste`, `image_path`, `trenutno_stanje_novca`, `tip_korisnika`) VALUES
(24, 'ogi123', 'ogi1233', 'ogi@raf.rs', 2003, '../frontend/public/users_images\\ogi123.jpeg', 6520, 'prodavac'),
(26, 'dstojanovic', '12345', 'dstojanovic@raf.rs', 2003, '../frontend/public/users_images\\dstojanovic.png', 0, 'admin'),
(27, 'jale123', 'jale123', 'jale@raf.rs', 2003, '../frontend/public/users_images\\jale123.png', 7315, 'prodavac'),
(33, 'aalizoti', '11111', 'aki@raf.rs', 2004, '../frontend/public/users_images\\aalizoti.png', 690, 'kupac');

-- --------------------------------------------------------

--
-- Table structure for table `korpa_proizvodi`
--

CREATE TABLE `korpa_proizvodi` (
  `id` int(11) NOT NULL,
  `korisnik_id` int(11) DEFAULT NULL,
  `proizvod_id` int(11) DEFAULT NULL,
  `kolicina` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kupovina`
--

CREATE TABLE `kupovina` (
  `id` int(11) NOT NULL,
  `datum_kupovine` date DEFAULT NULL,
  `Korisnici_id` int(11) NOT NULL,
  `proizvod_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `kupovina`
--

INSERT INTO `kupovina` (`id`, `datum_kupovine`, `Korisnici_id`, `proizvod_id`) VALUES
(12, '2024-02-21', 33, 4),
(13, '2024-02-21', 33, 5);

-- --------------------------------------------------------

--
-- Table structure for table `proizvodi`
--

CREATE TABLE `proizvodi` (
  `id` int(11) NOT NULL,
  `naziv` varchar(45) DEFAULT NULL,
  `opis` varchar(255) DEFAULT NULL,
  `cena` decimal(5,2) DEFAULT NULL,
  `kolicna_na_stanju` int(11) DEFAULT NULL,
  `opcija_za_snizenje` decimal(3,2) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `korisnici_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `proizvodi`
--

INSERT INTO `proizvodi` (`id`, `naziv`, `opis`, `cena`, `kolicna_na_stanju`, `opcija_za_snizenje`, `image_path`, `korisnici_id`) VALUES
(4, 'Domaca kafa', 'Ovo piće je veoma popularno u mnogim zemljama sveta. Kratko nakon konzumacije dolazi do blage nervne stimulacije što pojačava budnost, uzrokuje osećaj toplote, nesanicu, ubrzani rad srca', 220.00, 13, 1.00, '../../public/products/domaca.jpg', 27),
(5, 'Esspreso', 'Espreso je uglavnom gušći od kafe koja se pravi drugim metodama, ima veću koncentraciju suspendovanih i rastvorenih čvrstih materija, a na vrhu ima kremu', 240.00, 35, 1.00, '../../public/products/esspreso.jpg', 24),
(6, 'Frenezija', 'Kafa Frenezija, jedna je od mnogobrojnih vrsta hladnih kafa iz naše ponude i predstavlja pravo osveženje!', 450.00, 5, 1.00, '../../public/products/frenezija.jpg', 24),
(12, 'Topla cokolada', 'topla cokolada...', 320.00, 19, 1.00, '../frontend/public/products\\Topla.jpeg', 24),
(13, 'Bela topla cokolada', 'bela topla cokolada...', 350.00, 24, 5.00, '../frontend/public/products\\Bela.jpeg', 27),
(14, 'Makiato', 'Makiato kafa', 250.00, 8, 1.00, '../frontend/public/products\\Makiato.jpeg', 27),
(15, 'Latte', 'Latte makiato', 400.00, 20, 1.00, '../frontend/public/products\\Latte.jpeg', 24);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `komentari`
--
ALTER TABLE `komentari`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_Komentari_Proizvodi1_idx` (`Proizvodi_id`),
  ADD KEY `fk_Komentari_Korisnici1_idx` (`Korisnici_id`);

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `korpa_proizvodi`
--
ALTER TABLE `korpa_proizvodi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `korpa_proizvodi_ibfk_1` (`korisnik_id`),
  ADD KEY `korpa_proizvodi_ibfk_2` (`proizvod_id`);

--
-- Indexes for table `kupovina`
--
ALTER TABLE `kupovina`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_Kupovina_Korisnici1_idx` (`Korisnici_id`),
  ADD KEY `FK_proizvod_id` (`proizvod_id`);

--
-- Indexes for table `proizvodi`
--
ALTER TABLE `proizvodi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_proizvodi_korisnici1_idx` (`korisnici_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `komentari`
--
ALTER TABLE `komentari`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `korpa_proizvodi`
--
ALTER TABLE `korpa_proizvodi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `kupovina`
--
ALTER TABLE `kupovina`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `proizvodi`
--
ALTER TABLE `proizvodi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `komentari`
--
ALTER TABLE `komentari`
  ADD CONSTRAINT `fk_Komentari_Korisnici1` FOREIGN KEY (`Korisnici_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_Komentari_Proizvodi1` FOREIGN KEY (`Proizvodi_id`) REFERENCES `proizvodi` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `korpa_proizvodi`
--
ALTER TABLE `korpa_proizvodi`
  ADD CONSTRAINT `korpa_proizvodi_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `korpa_proizvodi_ibfk_2` FOREIGN KEY (`proizvod_id`) REFERENCES `proizvodi` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `kupovina`
--
ALTER TABLE `kupovina`
  ADD CONSTRAINT `FK_proizvod_id` FOREIGN KEY (`proizvod_id`) REFERENCES `proizvodi` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_Kupovina_Korisnici1` FOREIGN KEY (`Korisnici_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `proizvodi`
--
ALTER TABLE `proizvodi`
  ADD CONSTRAINT `fk_proizvodi_korisnici1` FOREIGN KEY (`korisnici_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
