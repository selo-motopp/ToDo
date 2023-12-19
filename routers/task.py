from datetime import date, datetime, time
<<<<<<< Updated upstream
from fastapi import APIRouter, Depends,Query
from db.models import DbUser
=======
from fastapi import APIRouter, Depends,Query, status, UploadFile, File 
from db.models import DbUser, Tag
>>>>>>> Stashed changes
from schemas import TaskBase, TaskDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_tasks
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme


router=APIRouter( prefix='/task',
                 tags=['task'])

#Create task
@router.post('/new',response_model=TaskDisplay)
def create_task(request: TaskBase,
                db: Session=Depends(get_db),
                priority: str = Query("Normal", enum=['Low', 'Normal', 'High','Critical']),
                current_user: DbUser = Depends(get_current_user)):
    return db_tasks.create_task(db,request,priority,current_user)

#Read all tasks
@router.get('/all',response_model=List[TaskDisplay])
def get_all_tasks(db:Session=Depends(get_db),current_user: DbUser = Depends(get_current_user)): #, token: str = Depends(oauth2_scheme)
    return db_tasks.get_all_tasks(db,current_user)

#Read one task
@router.get('/{id}',response_model=TaskDisplay)
def get_task(id:int,db:Session=Depends(get_db),current_user: DbUser = Depends(get_current_user)):
    return db_tasks.get_task(db,id,current_user)


#Update tasks
@router.put('/{id}')
def update_task(id:int,
                request:TaskBase,
                db:Session=Depends(get_db),
                status: str = Query('New', enum=['New', 'In progress', 'Done']),
                priority: str = Query('Normal', enum=['Low', 'Normal', 'High','Critical']),
                folder_id:int=Query("1"),
                flag:bool=Query(False,enum=[False,True]), 
                current_user: DbUser = Depends(get_current_user),
                date: str = Query(..., alias="dd.mm.yyyy"),
                time:str=Query(...,alias="hh:mm")
):
    date_iso = datetime.strptime(date, "%d.%m.%Y").date()
    time_iso = datetime.strptime(time, "%H:%M").time()
    return db_tasks.update_task(id,request,db,status,priority,flag,date_iso,time_iso,folder_id,current_user)

@router.delete('/{id}')
def delete_task(id:int=None, db: Session = Depends(get_db),delete_all:bool=Query(...,enum=[False,True]),current_user: DbUser = Depends(get_current_user)):
    if delete_all:
        return db_tasks.delete_all_tasks(db, current_user)
    else:
        return db_tasks.delete_task(db, id, current_user)


# CRUD operations for Tags
@router.post("/tags/", response_model=Tag)
def create_tag(name: str, db: Session = Depends(get_db)):
    return db_tasks.create_tag(name)

@router.get("/tags/", response_model=List[Tag])
def get_all_tags(db: Session = Depends(get_db)):
    return db_tasks.get_all_tags()

@router.get("/tags/{tag_id}", response_model=Tag)
def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)):
    return db_tasks.get_tag_by_id(tag_id)

@router.put("/tags/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, name: str, db: Session = Depends(get_db)):
    return db_tasks.update_tag(tag_id, name)

@router.delete("/tags/{tag_id}", response_model=Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    return db_tasks.delete_tag(tag_id)