-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 26, 2025 at 09:57 AM
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
-- Database: `airline`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `location`, `email`, `phone_number`, `password`) VALUES
(1, 'Rahul Raval', 'navsari', 'rahul9raval@gmail.com', '7016849279', 'rahul123');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `feedback` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plan`
--

CREATE TABLE `plan` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `passanger` int(11) DEFAULT NULL,
  `general` int(11) DEFAULT NULL,
  `business` int(11) DEFAULT NULL,
  `departure` varchar(100) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `landing_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plan`
--

INSERT INTO `plan` (`id`, `name`, `passanger`, `general`, `business`, `departure`, `destination`, `time`, `landing_time`) VALUES
(11, 'IndiGo 6E101', 180, 50, 10, 'Mumbai', 'Delhi', '2025-02-14 08:30:00', '2025-02-14 10:45:00'),
(12, 'Air India AI302', 200, 40, 8, 'Delhi', 'Bengaluru', '2025-02-15 09:00:00', '2025-02-15 11:30:00'),
(13, 'SpiceJet SG505', 190, 45, 12, 'Bengaluru', 'Kolkata', '2025-02-16 14:30:00', '2025-02-16 17:15:00'),
(14, 'Vistara UK745', 150, 30, 6, 'Chennai', 'Hyderabad', '2025-02-17 07:00:00', '2025-02-17 08:45:00'),
(15, 'GoAir G8116', 160, 35, 5, 'Pune', 'Goa', '2025-02-18 16:00:00', '2025-02-18 17:10:00');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` varchar(12) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `bonus_count` int(11) DEFAULT 0,
  `email` varchar(100) NOT NULL,
  `wallet_balance` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `location`, `birthday`, `password`, `bonus_count`, `email`, `wallet_balance`) VALUES
('priyansh@856', 'priyansh', 'kolkata', '2001-05-15', 'jadugar69', 0, 'jadugar69@gmail.com', 0.00),
('Rahul@169685', 'Rahul Raval', 'navsari', '2005-08-12', 'riddhiraval1285', 0, 'rahularaval2912@gmail.com', 0.00),
('Rahul@393341', 'Rahul Raval', 'gandhinagar', '2001-07-14', 'sagar0798', 0, 'sagar1285@gmail.com', 0.00),
('Rahul@860978', 'Rahul Raval', 'navsari', '2005-08-12', 'riddhiraval1285', 0, 'rahul9raval@gmail.com', 0.00),
('Riddhi@53013', 'Riddhi Ashokkumar Raval', 'billimora', '2005-08-12', 'riddhiD4', 0, 'riddhi98raval@gmail.com', 0.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `plan`
--
ALTER TABLE `plan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plan`
--
ALTER TABLE `plan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
