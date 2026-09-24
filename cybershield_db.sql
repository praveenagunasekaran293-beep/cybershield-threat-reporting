-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 24, 2026 at 10:44 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cybershield_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `threat_reports`
--

CREATE TABLE `threat_reports` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `threat_type` varchar(100) NOT NULL,
  `severity` varchar(20) NOT NULL,
  `status` varchar(30) NOT NULL DEFAULT 'Open',
  `reported_by` varchar(100) NOT NULL,
  `source` varchar(255) DEFAULT NULL,
  `reported_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `threat_reports`
--

INSERT INTO `threat_reports` (`id`, `title`, `description`, `threat_type`, `severity`, `status`, `reported_by`, `source`, `reported_at`, `updated_at`) VALUES
(1, 'Suspicious Phishing Email', 'A suspicious email containing a malicious\r\nlink was reported by the user.', 'Phishing', 'High', 'Open', 'admin', 'email', '2026-09-24 18:39:13', NULL),
(2, 'Fake Bank Phishing Email', 'A suspicious email was received containing a fake banking login link', 'Phishing', 'High', 'Open', 'admin', 'email', '2026-09-24 19:16:46', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(0, 'admin', 'admin29@gmail.com', 'scrypt:32768:8:1$6mQwjXF9Rzy7rB9x$3f4188bb8e328e84be214eacce8ed2e4413311f439b249aabf192f13965423f5765b005fd47cc28f076b7d37d13be6bcfed7c55261457ec8124f49b6291a2a56', '2026-09-24 17:58:45');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `threat_reports`
--
ALTER TABLE `threat_reports`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `threat_reports`
--
ALTER TABLE `threat_reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
