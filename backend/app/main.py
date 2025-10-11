from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text  
from app.database import SessionLocal

from app.routes import category
from app.routes import user 
from app.routes import auth
from app.routes import product
from app.routes import contact
from app.routes import cart

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
        db: Session = SessionLocal()
        db.execute(text("SELECT 1")) 
        return {"status": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}

app.include_router(category.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(contact.router)
app.include_router(cart.router)



if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8020, reload=False)