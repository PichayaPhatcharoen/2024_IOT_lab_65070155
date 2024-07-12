from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
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

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/student/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

@router_v1.post('/student')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newstudent = models.Student(surname=student['surname'], lastname=student['lastname'], id=student['id'], birthdate=student['birthdate'], gender=student['gender'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

@router_v1.patch('/student/{student_id}')
async def update_student(student_id: int, student: dict, response: Response, db: Session = Depends(get_db)):
    currentstudent = db.query(models.Student).filter(models.Student.id == student_id).first()
    if currentstudent:
        currentstudent.id = student['id']
        currentstudent.surname = student['surname']
        currentstudent.lastname = student['lastname']
        currentstudent.birthdate = student['birthdate']
        currentstudent.gender = student['gender']
        
        db.commit()
        db.refresh(currentstudent)
        response.status_code = 202
        return currentstudent
    else:
        response.status_code = 404
        return {'message': 'Student not found'}

@router_v1.delete('/student/{student_id}')
async def delete_student(student_id: int, response: Response, db: Session = Depends(get_db)):
    delstudent = db.query(models.Student).filter(models.Student.id == student_id).first()
    if delstudent:
        db.delete(delstudent)
        db.commit()
        response.status_code = 202
        return { 'deleted' }
    else:
        response.status_code = 404
        return { 'message' : 'student not found'}


app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
