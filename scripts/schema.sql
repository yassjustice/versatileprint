"""
Database initialization script.
Creates all tables with proper constraints and indexes.
Run this script to set up the database schema.
"""

-- Drop existing tables if they exist (for clean reinstall)
-- Uncomment these lines if you need to reset the database
-- SET FOREIGN_KEY_CHECKS = 0;
-- DROP TABLE IF EXISTS audit_logs;
-- DROP TABLE IF EXISTS notifications;
-- DROP TABLE IF EXISTS orders;
-- DROP TABLE IF EXISTS csv_imports;
-- DROP TABLE IF EXISTS quota_topups;
-- DROP TABLE IF EXISTS client_quotas;
-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS roles;
-- SET FOREIGN_KEY_CHECKS = 1;

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_role_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) DEFAULT NULL,
  role_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  last_login TIMESTAMP NULL DEFAULT NULL,
  CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT,
  INDEX idx_users_email (email),
  INDEX idx_users_role (role_id),
  INDEX idx_users_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create client_quotas table
CREATE TABLE IF NOT EXISTS client_quotas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  month DATE NOT NULL COMMENT 'Normalized as YYYY-MM-01',
  bw_limit INT NOT NULL DEFAULT 3000,
  color_limit INT NOT NULL DEFAULT 2000,
  bw_used INT NOT NULL DEFAULT 0,
  color_used INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  bw_alert_sent BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Track if 80% alert sent for B&W',
  color_alert_sent BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Track if 80% alert sent for Color',
  UNIQUE KEY uq_client_month (client_id, month),
  CONSTRAINT fk_cq_client FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_cq_client_month (client_id, month),
  INDEX idx_cq_month (month),
  CHECK (bw_limit >= 0),
  CHECK (color_limit >= 0),
  CHECK (bw_used >= 0),
  CHECK (color_used >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create quota_topups table
CREATE TABLE IF NOT EXISTS quota_topups (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  admin_id INT NOT NULL COMMENT 'Administrator performing top-up',
  bw_added INT NOT NULL DEFAULT 0,
  color_added INT NOT NULL DEFAULT 0,
  transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notes TEXT DEFAULT NULL,
  CONSTRAINT fk_qt_client FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_qt_admin FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_qt_client_date (client_id, transaction_date),
  INDEX idx_qt_admin (admin_id),
  INDEX idx_qt_date (transaction_date),
  CHECK (bw_added >= 0),
  CHECK (color_added >= 0),
  CHECK (bw_added > 0 OR color_added > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create csv_imports table
CREATE TABLE IF NOT EXISTS csv_imports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  uploaded_by INT NOT NULL COMMENT 'Must be Administrator',
  original_filename VARCHAR(255) NOT NULL,
  stored_filepath VARCHAR(500) NOT NULL,
  status ENUM('pending_validation','validated','rejected') NOT NULL DEFAULT 'pending_validation',
  uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  validated_by INT NULL DEFAULT NULL,
  validated_at TIMESTAMP NULL DEFAULT NULL,
  notes TEXT DEFAULT NULL COMMENT 'Admin review notes',
  row_count INT DEFAULT 0 COMMENT 'Total rows in CSV',
  valid_rows INT DEFAULT 0 COMMENT 'Valid rows after validation',
  error_rows INT DEFAULT 0 COMMENT 'Rows with errors',
  CONSTRAINT fk_ci_uploader FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE RESTRICT,
  CONSTRAINT fk_ci_validator FOREIGN KEY (validated_by) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_ci_uploader_status (uploaded_by, status),
  INDEX idx_ci_status (status),
  INDEX idx_ci_uploaded_at (uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL COMMENT 'Must be Client role',
  agent_id INT NULL DEFAULT NULL COMMENT 'Agent who created/owns; NULL if client created',
  status ENUM('pending','validated','processing','completed') NOT NULL DEFAULT 'pending',
  bw_quantity INT NOT NULL DEFAULT 0,
  color_quantity INT NOT NULL DEFAULT 0,
  paper_dimensions VARCHAR(50) DEFAULT NULL COMMENT 'e.g., A4, A3, 210x297mm',
  paper_type VARCHAR(100) DEFAULT NULL COMMENT 'e.g., matte, glossy, standard',
  finishing VARCHAR(100) DEFAULT NULL COMMENT 'e.g., staple, bind, none',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  import_id INT NULL DEFAULT NULL COMMENT 'FK to csv_imports if from CSV',
  external_order_id VARCHAR(100) NULL DEFAULT NULL COMMENT 'For idempotency/deduplication',
  notes TEXT DEFAULT NULL,
  CONSTRAINT fk_orders_client FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE RESTRICT,
  CONSTRAINT fk_orders_agent FOREIGN KEY (agent_id) REFERENCES users(id) ON DELETE SET NULL,
  CONSTRAINT fk_orders_import FOREIGN KEY (import_id) REFERENCES csv_imports(id) ON DELETE SET NULL,
  INDEX idx_orders_client_status (client_id, status),
  INDEX idx_orders_agent_status (agent_id, status),
  INDEX idx_orders_import (import_id),
  INDEX idx_orders_status (status),
  INDEX idx_orders_created_at (created_at),
  INDEX idx_orders_external_id (external_order_id),
  CHECK (bw_quantity >= 0),
  CHECK (color_quantity >= 0),
  CHECK (bw_quantity > 0 OR color_quantity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  message TEXT NOT NULL,
  related_order_id INT NULL DEFAULT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notification_type VARCHAR(50) DEFAULT 'info' COMMENT 'info, warning, error, success',
  CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_notif_order FOREIGN KEY (related_order_id) REFERENCES orders(id) ON DELETE CASCADE,
  INDEX idx_notif_user_read (user_id, is_read),
  INDEX idx_notif_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NULL DEFAULT NULL COMMENT 'NULL for system actions',
  action VARCHAR(100) NOT NULL COMMENT 'e.g., ORDER_STATUS_CHANGE, CSV_VALIDATED, USER_LOGIN',
  details JSON NULL DEFAULT NULL COMMENT 'Structured context',
  ip_address VARCHAR(45) NULL DEFAULT NULL COMMENT 'IPv4 or IPv6',
  user_agent TEXT NULL DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  INDEX idx_audit_action_date (action, created_at),
  INDEX idx_audit_user (user_id),
  INDEX idx_audit_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed initial roles
INSERT INTO roles (name) VALUES ('Client'), ('Agent'), ('Administrator')
ON DUPLICATE KEY UPDATE name=name;
