from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from app.database import get_db
from app.services import db_export

from app.routes import category
from app.routes import user 
from app.routes import auth
from app.routes import product
from app.routes import contact
from app.routes import cart
from app.routes import order
from app.routes import location
from app.routes import analytics
from app.routes import admin
from app.routes import favorite
from app.routes import reports

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping-db")
def ping_db():
    try:
        # Get a connection from the pool
        db_gen = get_db()
        db = next(db_gen)
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return {"status": "Database connected successfully!", "result": result}
    except Exception as e:
        return {"error": str(e)}

app.include_router(category.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(contact.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(location.router)
app.include_router(analytics.router)
app.include_router(admin.router)
app.include_router(favorite.router)
app.include_router(reports.router)



if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8020, reload=False)