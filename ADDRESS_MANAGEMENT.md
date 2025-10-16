# Address Management Implementation

## ✅ Implementation Complete!

### Changes Made:

## Backend Changes:

### 1. **New Location Routes** (`backend/app/routes/location.py`)

Created new API endpoints to fetch cities from the location table:

- `GET /locations/cities` - Get all available cities
- `GET /locations/cities/{city_name}` - Get specific city details

### 2. **Updated Order Schema** (`backend/app/schemas/order.py`)

Added new `AddressDetails` class:

```python
class AddressDetails(BaseModel):
    house_number: int
    street: str
    city: str
    state: str
```

Updated `CreateOrderRequest` to include:

- `address_details: Optional[AddressDetails]` - For creating new addresses

### 3. **Updated Order Routes** (`backend/app/routes/order.py`)

Enhanced checkout endpoint to:

- Accept address details in the request
- Automatically find `city_id` from the location table based on city name
- Create new address record in the address table
- Store the new `address_id` in the delivery record

**Address Creation Logic:**

1. Customer provides: house_number, street, city, state
2. Backend queries location table to find matching city
3. Retrieves `city_id` from location table
4. Creates new address record with all fields including `city_id`
5. Uses new `address_id` for the delivery record

### 4. **Registered Location Router** (`backend/app/main.py`)

Added location router to the FastAPI application

---

## Frontend Changes:

### 1. **Updated Checkout Form** (`frontend/src/pages/Checkout.jsx`)

#### New Address Fields (shown only for Home Delivery):

- **House Number** - Number input field
- **Street** - Text input field
- **City** - Dropdown select populated from location table
- **State** - Text input field

#### Features:

- ✅ Fields only appear when "Home Delivery" is selected
- ✅ City dropdown shows all cities from database
- ✅ Main cities are indicated with "(Main City)" label
- ✅ All fields required for home delivery
- ✅ Store pickup doesn't require address

### 2. **Dynamic City Loading**

- Fetches cities from `/locations/cities` endpoint on page load
- Populates dropdown with all available cities
- Shows whether city is a main city (affects delivery time)

### 3. **Address Submission**

Updated order creation to send:

```javascript
{
  user_id: user.user_id,
  payment_method: 'card' | 'cod',
  delivery_method: 'home_delivery' | 'store_pickup',
  address_details: {
    house_number: 123,
    street: 'Main Street',
    city: 'Dallas',
    state: 'Texas'
  }
}
```

---

## How It Works:

### Customer Flow:

1. **Select Delivery Method**

   - If "Store Pickup" → No address fields shown
   - If "Home Delivery" → Address fields appear

2. **Fill Address Details** (for Home Delivery):

   - Enter House Number (e.g., 123)
   - Enter Street Name (e.g., Main Street)
   - Select City from dropdown (automatically populated from database)
   - Enter State (e.g., Texas)

3. **Place Order**
   - Frontend sends address details to backend
   - Backend finds `city_id` from location table based on selected city
   - Creates new address record with all fields
   - Associates address with the delivery record

### Backend Processing:

```python
# 1. Receive address details from frontend
address_details = {
    house_number: 123,
    street: "Main Street",
    city: "Dallas",
    state: "Texas"
}

# 2. Find city_id from location table
location = db.query(Location).filter(Location.city == "Dallas").first()
city_id = location.city_id  # Gets city_id automatically

# 3. Create address record
new_address = Address(
    house_number=123,
    street="Main Street",
    city="Dallas",
    state="Texas",
    city_id=city_id  # Auto-populated from location table
)

# 4. Use address_id in delivery record
delivery = Delivery(
    order_id=order.order_id,
    address_id=new_address.address_id
)
```

---

## Database Structure:

### Location Table (Reference):

```
city_id | city      | Is_main_city
--------|-----------|-------------
1       | Dallas    | TRUE
2       | Houston   | TRUE
6       | Norman    | FALSE
```

### Address Table (Created during order):

```
address_id | house_number | street      | city    | state | city_id
-----------|--------------|-------------|---------|-------|--------
1          | 123          | Main Street | Dallas  | Texas | 1
```

### Delivery Table (Links to Address):

```
delivery_id | order_id | address_id | delivery_method
------------|----------|------------|----------------
1           | 1        | 1          | home_delivery
```

---

## Benefits:

✅ **Structured Address Data** - Separate fields for each address component  
✅ **City Validation** - Only allows cities that exist in location table  
✅ **Automatic city_id** - System automatically finds and stores city_id  
✅ **Main City Detection** - Knows if delivery is to main city (for delivery time calculation)  
✅ **Clean Data** - Normalized address structure in database  
✅ **Better UX** - Dropdown for cities prevents typos  
✅ **Store Pickup Support** - No address required for store pickup

---

## Example Usage:

### Main City Order (Dallas - Fast Delivery):

```
House Number: 123
Street: Main Street
City: Dallas (Main City)
State: Texas

→ city_id: 1 (automatically found)
→ Is_main_city: TRUE
→ Delivery Time: 5 days (if in stock) or 8 days (if out of stock)
```

### Other City Order (Norman - Standard Delivery):

```
House Number: 456
Street: Oak Avenue
City: Norman
State: Oklahoma

→ city_id: 10 (automatically found)
→ Is_main_city: FALSE
→ Delivery Time: 7 days (if in stock) or 10 days (if out of stock)
```

---

## Status: ✅ READY TO TEST

- ✅ Location routes created
- ✅ Cities endpoint working
- ✅ Address fields in checkout form
- ✅ City dropdown populated from database
- ✅ Automatic city_id lookup implemented
- ✅ Address creation integrated with order flow
- ✅ Fields only show for home delivery
- ✅ Backend server running

**Test the checkout page now! Select "Home Delivery" to see the new address fields with the city dropdown.** 🎉
