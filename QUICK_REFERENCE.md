# BrightBuy Analytics - Quick Reference Card

## 🚀 Installation (One-Time Setup)

```bash
cd backend
python database/apply_new_procedures.py
```

## ▶️ Start Server

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8020 --reload
```

## 🧪 Test Everything

```bash
python test_analytics_endpoints.py
```

## 📊 API Endpoints Cheat Sheet

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analytics/cart/{user_id}` | GET | Cart details |
| `/analytics/products/category?category_id=1` | GET | Products by category |
| `/analytics/inventory/low-stock?threshold=10` | GET | Low stock alerts |
| `/analytics/sales/report?start_date=...&end_date=...` | GET | Sales report |
| `/analytics/orders/{order_id}/status` | PUT | Update order status |
| `/analytics/products/top-selling?limit=10&days=30` | GET | Best sellers |
| `/analytics/customers/{user_id}/order-history` | GET | Order history |

## 💻 Quick Test Commands

```bash
# Cart
curl http://127.0.0.1:8020/analytics/cart/1

# Low Stock
curl "http://127.0.0.1:8020/analytics/inventory/low-stock?threshold=10"

# Sales Report
curl "http://127.0.0.1:8020/analytics/sales/report"

# Top Sellers
curl "http://127.0.0.1:8020/analytics/products/top-selling?limit=5"

# Order History
curl http://127.0.0.1:8020/analytics/customers/1/order-history

# Update Status
curl -X PUT "http://127.0.0.1:8020/analytics/orders/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "Shipped"}'
```

## 🌐 Interactive Docs

**Swagger UI:** http://127.0.0.1:8020/docs  
**ReDoc:** http://127.0.0.1:8020/redoc

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app/routes/analytics.py` | API endpoints |
| `backend/database/new_stored_procedures.sql` | SQL procedures |
| `backend/app/main.py` | Router registration |
| `API_ENDPOINTS.md` | Full documentation |

## 🔧 Troubleshooting

**Procedures not found?**
```bash
python database/apply_new_procedures.py
```

**Server not starting?**
```bash
# Check main.py location
cd backend
python -m uvicorn app.main:app --reload
```

**Import error?**
```python
# Verify in app/main.py:
from app.routes import analytics
app.include_router(analytics.router)
```

## 📱 Frontend Integration

```javascript
// Get cart
const cart = await axios.get(`http://127.0.0.1:8020/analytics/cart/${userId}`);

// Low stock
const lowStock = await axios.get('http://127.0.0.1:8020/analytics/inventory/low-stock', {
  params: { threshold: 10 }
});

// Sales report
const sales = await axios.get('http://127.0.0.1:8020/analytics/sales/report', {
  params: { start_date: '2025-01-01', end_date: '2025-10-16' }
});
```

## ✅ Checklist

- [ ] Procedures installed
- [ ] Server running
- [ ] Endpoints tested
- [ ] Docs reviewed
- [ ] Frontend integrated

---

**Need help?** Check `IMPLEMENTATION_COMPLETE.md` or `API_ENDPOINTS.md`
