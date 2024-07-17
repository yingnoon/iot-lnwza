from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router_v1.get('/info')
async def get_info(db: Session = Depends(get_db)):
    return db.query(models.Info).all()


@router_v1.post('/info')
async def create_Info(Info: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newInfo = models.Info( firstname=Info['firstname'], surname=Info['surname'], id=Info['id'], birth=Info['birth'], gender=Info['gender'])
    db.add(newInfo)
    db.commit()
    db.refresh(newInfo)
    response.status_code = 201
    return newInfo

@router_v1.put('/info/{info_id}')
async def update_Info(info_id: str, Info: dict, response: Response, db: Session = Depends(get_db)):

    modify = db.query(models.Info).filter(models.Info.id == info_id).first()
    if modify is None:
        raise HTTPException(status_code=404, detail="Student not found")

    modify.firstname = Info.get('firstname', modify.firstname)
    modify.surname = Info.get('surname', modify.surname)
    modify.birth = Info.get('birth', modify.birth)
    modify.gender = Info.get('gender', modify.gender)

    db.commit()
    db.refresh(modify)
    response.status_code = 200
    return modify



@router_v1.delete('/info/{info_id}')
async def delete_Info(info_id: str, response: Response, db: Session = Depends(get_db)):

    delete_Info = db.query(models.Info).filter(models.Info.id == info_id).first()
    if delete_Info is None:
        raise HTTPException(status_code=404, detail="Student not found")


    db.delete(delete_Info)
    db.commit()

    response.status_code = 200
    return {"detail": "Student deleted successfully"}


app.include_router(router_v1)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
