-- Update the Users table to increase column lengths
ALTER TABLE "Users" ALTER COLUMN email TYPE VARCHAR(100);
ALTER TABLE "Users" ALTER COLUMN passwrod TYPE VARCHAR(255);
ALTER TABLE "Users" ALTER COLUMN lastpassword TYPE VARCHAR(255);

-- Update the back table user_id column type
ALTER TABLE "back" ALTER COLUMN user_id TYPE VARCHAR(36);
