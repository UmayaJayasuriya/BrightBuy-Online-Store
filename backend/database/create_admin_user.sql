-- Admin User Setup Script
-- Run this script to create or update an admin user in BrightBuy database

-- Option 1: Update an existing user to admin
-- Replace the email with the user you want to make admin
UPDATE user 
SET user_type = 'admin' 
WHERE email = 'admin@example.com';

-- To verify the change:
SELECT user_id, user_name, email, user_type 
FROM user 
WHERE user_type = 'admin';

-- Option 2: Create a new admin user from scratch
-- Note: You'll need to hash the password using bcrypt first
-- You can use the signup endpoint to create the user, then run this to upgrade to admin:

-- Example: Make user_id 1 an admin
UPDATE user 
SET user_type = 'admin' 
WHERE user_id = 1;

-- Option 3: Make all users with 'admin' in their email admin
UPDATE user 
SET user_type = 'admin' 
WHERE email LIKE '%admin%';

-- Check all admin users
SELECT user_id, user_name, email, name, user_type, address_id
FROM user 
WHERE user_type = 'admin'
ORDER BY user_id;

-- Check all user types in the system
SELECT user_type, COUNT(*) as count
FROM user
GROUP BY user_type;
