from app.shared.database import SessionLocal
from app.shared.exceptions import NotFound

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        if isinstance(ex, NotFound):
            raise  
        else:
            raise ex
    finally:
        db.close()