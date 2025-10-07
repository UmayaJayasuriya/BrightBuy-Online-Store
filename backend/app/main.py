from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text  # ✅ import this
from app.database import SessionLocal

from app.routes import category
from app.routes import user 
from app.routes import auth

app = FastAPI()

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



if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8020, reload=False)