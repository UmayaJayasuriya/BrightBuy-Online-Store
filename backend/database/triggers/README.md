# Email Validation Trigger

## Overview

This trigger validates email addresses before user insertion into the database, ensuring data integrity at the database level.

## Trigger Details

**Trigger Name:** `trg_check_email_before_insert`  
**Event:** BEFORE INSERT  
**Table:** User  
**Purpose:** Validate email format (must contain '@' symbol)

## SQL Code

```sql
DELIMITER $$

CREATE TRIGGER trg_check_email_before_insert
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    -- Check if email contains '@'
    IF NEW.email NOT LIKE '%@%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Please enter a valid email address. It must include the "@" symbol (e.g., name@example.com).';
    END IF;
END$$

DELIMITER ;
```

## Installation

### Method 1: Using Python Script (Recommended)

```bash
cd backend
python database/apply_email_trigger.py
```

### Method 2: Manual SQL Execution

```bash
cd backend/database/triggers
mysql -u your_username -p your_database < email_validation_trigger.sql
```

### Method 3: Direct MySQL Command

```bash
mysql -u root -p
use your_database;
source backend/database/triggers/email_validation_trigger.sql;
```

## How It Works

### 1. **Trigger Activation**

- Fires automatically BEFORE any INSERT into the User table
- Validates email before data is written to database

### 2. **Validation Logic**

- Checks if `NEW.email` contains '@' symbol
- Uses SQL `LIKE` operator: `NEW.email NOT LIKE '%@%'`

### 3. **Error Handling**

- If validation fails: Raises error with SQLSTATE '45000'
- Provides user-friendly error message
- Prevents invalid data from being inserted

### 4. **Backend Integration**

- FastAPI route catches trigger errors
- Converts database errors to HTTP 400 Bad Request
- Returns clear error message to frontend

## Multi-Layer Validation

This trigger is part of a **3-layer validation strategy**:

1. **Frontend Validation** (JavaScript)

   - HTML5 email input type
   - Immediate user feedback
   - Best user experience

2. **Backend Validation** (FastAPI/Pydantic)

   - Pydantic `EmailStr` type
   - Additional '@' check
   - Catches errors before database call

3. **Database Validation** (SQL Trigger) ⭐ **This Layer**
   - Final safety net
   - Ensures data integrity
   - Protects against direct database modifications

## Testing

### Test Valid Email

```bash
# Should succeed
curl -X POST http://127.0.0.1:8020/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "testuser",
    "email": "test@example.com",
    "name": "Test User",
    "password": "password123",
    "address": {
      "house_number": 123,
      "street": "Main St",
      "city": "Colombo",
      "state": "Western"
    }
  }'
```

### Test Invalid Email

```bash
# Should fail with trigger error
curl -X POST http://127.0.0.1:8020/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "testuser",
    "email": "invalidemail",
    "name": "Test User",
    "password": "password123",
    "address": {
      "house_number": 123,
      "street": "Main St",
      "city": "Colombo",
      "state": "Western"
    }
  }'
```

Expected error response:

```json
{
  "detail": "Please enter a valid email address. It must include the \"@\" symbol (e.g., name@example.com)."
}
```

## Verification

Check if trigger exists:

```sql
SHOW TRIGGERS FROM your_database WHERE `Trigger` = 'trg_check_email_before_insert';
```

View trigger details:

```sql
SHOW CREATE TRIGGER trg_check_email_before_insert;
```

## Error Codes

- **SQLSTATE 45000**: User-defined error (trigger validation failure)
- **HTTP 400**: Bad Request (invalid email format)

## Benefits

✅ **Data Integrity**: Guarantees all users have valid emails  
✅ **Defense in Depth**: Multiple validation layers  
✅ **User-Friendly**: Clear error messages  
✅ **Automatic**: No code changes needed for protection  
✅ **Consistent**: Works even with direct SQL inserts

## Maintenance

### Drop Trigger

```sql
DROP TRIGGER IF EXISTS trg_check_email_before_insert;
```

### Modify Trigger

1. Drop existing trigger
2. Create new version with updated logic
3. Test thoroughly

## Notes

- Trigger runs for ALL inserts (API, direct SQL, imports)
- Cannot be bypassed without admin privileges
- Minimal performance impact (simple string check)
- Works with stored procedure `AddUserWithAddress`

## Related Files

- `backend/database/triggers/email_validation_trigger.sql` - Trigger SQL
- `backend/database/apply_email_trigger.py` - Installation script
- `backend/app/routes/user.py` - User creation route with error handling
- `backend/app/schemas/user.py` - Pydantic validation (EmailStr)
