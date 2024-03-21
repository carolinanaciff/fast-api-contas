from app.shared.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        raise Exception(ex)
    finally:
        db.close()