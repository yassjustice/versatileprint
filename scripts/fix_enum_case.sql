-- =============================================================================
-- Fix Enum Case Mismatch - VersatilesPrint Database
-- =============================================================================
-- This script updates the orders table status enum from lowercase to uppercase
-- to match the Python OrderStatus enum definition.
-- 
-- Issue: Database has lowercase values ('pending', 'validated', etc.)
--        Python expects uppercase values ('PENDING', 'VALIDATED', etc.)
-- 
-- Run this script on the production/development database to fix the mismatch.
-- =============================================================================

USE versatileprint;

-- Step 1: Temporarily modify the column to allow both cases
ALTER TABLE orders 
MODIFY COLUMN status ENUM('pending','validated','processing','completed','PENDING','VALIDATED','PROCESSING','COMPLETED') NOT NULL DEFAULT 'pending';

-- Step 2: Update existing data to uppercase
UPDATE orders SET status = 'PENDING' WHERE status = 'pending';
UPDATE orders SET status = 'VALIDATED' WHERE status = 'validated';
UPDATE orders SET status = 'PROCESSING' WHERE status = 'processing';
UPDATE orders SET status = 'COMPLETED' WHERE status = 'completed';

-- Step 3: Change the enum to only allow uppercase values
ALTER TABLE orders 
MODIFY COLUMN status ENUM('PENDING','VALIDATED','PROCESSING','COMPLETED') NOT NULL DEFAULT 'PENDING';

-- Verify the change
SELECT COUNT(*) as total_orders, status 
FROM orders 
GROUP BY status;

SHOW COLUMNS FROM orders LIKE 'status';
