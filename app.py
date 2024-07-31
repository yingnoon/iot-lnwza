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


@router_v1.get('/menu')
async def get_menu(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router_v1.get('/menu/{menu_id}')
async def get_menu(menu_id: int, response: Response, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

@router_v1.post('/menu')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    create_menu = models.Menu(name=menu['name'], price=menu['price'], detail=menu['detail'])
    db.add(create_menu)
    db.commit()
    db.refresh(create_menu)
    response.status_code = 201
    return create_menu

@router_v1.put('/menu/{menu_id}')
async def update_menu(menu_id: int, menu: dict, response: Response, db: Session = Depends(get_db)):

    modify = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if modify is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    modify.name = menu.get('name', modify.name)
    modify.price = menu.get('price', modify.price)
    modify.detail = menu.get('detail', modify.detail)

    db.commit()
    db.refresh(modify)
    response.status_code = 200
    return modify

@router_v1.delete('/menu/{menu_id}')
async def delete_menu(menu_id: int, response: Response, db: Session = Depends(get_db)):

    delete_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if delete_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(delete_menu)
    db.commit()

    response.status_code = 200
    return {"detail": "Menu deleted successfully"}

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, response: Response, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    create_book = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'], detail=book['detail'], summary=book['summary'], group=book['group'])
    db.add(create_book)
    db.commit()
    db.refresh(create_book)
    response.status_code = 201
    return create_book

@router_v1.put('/books/{book_id}')
async def update_book(book_id: int, book: dict, response: Response, db: Session = Depends(get_db)):

    modify = db.query(models.Book).filter(models.Book.id == book_id).first()
    if modify is None:
        raise HTTPException(status_code=404, detail="Book not found")

    modify.title = book.get('title', modify.title)
    modify.author = book.get('author', modify.author)
    modify.year = book.get('year', modify.year)
    modify.is_published = book.get('is_published', modify.is_published)
    modify.detail = book.get('detail', modify.detail)
    modify.summary = book.get('summary', modify.summary)
    modify.group = book.get('group', modify.group)

    db.commit()
    db.refresh(modify)
    response.status_code = 200
    return modify

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, response: Response, db: Session = Depends(get_db)):

    delete_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if delete_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(delete_book)
    db.commit()

    response.status_code = 200
    return {"detail": "Book deleted successfully"}

@router_v1.get('/orders')
async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    create_order = models.Order(name=order['name'], price=order['price'], total=order['total'], note=order['note'])
    db.add(create_order)
    db.commit()
    db.refresh(create_order)
    response.status_code = 201
    return create_order

@router_v1.get('/orders/{order_id}')
async def get_order(order_id: int, response: Response, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


app.include_router(router_v1)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
