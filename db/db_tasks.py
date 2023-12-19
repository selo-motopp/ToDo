from datetime import datetime,date,time
from sqlalchemy.orm.session import Session
from db.models import DbFolder, DbTask, DbUser, Tag
from schemas import TaskBase
<<<<<<< Updated upstream
from fastapi import  HTTPException, status
=======
from fastapi import  HTTPException,status
from db.database import SessionLocal
>>>>>>> Stashed changes

#Creating new task. By default it's status is 'New' and folder is 'Main'
def create_task(db:Session,request:TaskBase,option,current_user):
    new_task=DbTask(
        title=request.title,
        description=request.description,
        task_status='New',
        priority=option,
        flag=False,
        date=datetime.now().date(),
        time=datetime.now().time(),
        folder_id=1,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


#Read all tasks
def get_all_tasks(db:Session,current_user):
    return db.query(DbTask).filter(DbTask.user_id == current_user.id).all()


#Read task
def get_task(db:Session,id:int,current_user):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')
    if current_user.id != DbTask.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to read this task')  
    return task

#Update  task
def update_task(id:int,request:TaskBase,db:Session,Status:str,priority:str,flag:bool,date_iso,time_iso,folder_id:int,current_user):
    task=db.query(DbTask).filter(DbTask.id==id).first()
    folder=db.query(DbFolder).filter(DbFolder.id==folder_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found')
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Folder with id {folder_id} not found') 
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to update this task')
    if current_user.id !=DbFolder.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to place task in this folder')
    db.query(DbTask).filter(DbTask.id == id).update({
        DbTask.title: request.title,
        DbTask.description: request.description,
        DbTask.task_status:Status,
        DbTask.priority:priority,
        DbTask.flag:flag,
        DbTask.folder_id:folder_id,
        DbTask.date:date_iso,
        DbTask.time:time_iso
    })
    db.commit()
    return 'Success'


#Delete task
def delete_task(db:Session,id:int, current_user):
    task=db.query(DbTask).filter(DbTask.id==id ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} not found') 
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this task') 
    db.delete(task)
    db.commit()
    return 'Success'

def delete_all_tasks(db: Session, current_user):
    user = db.query(DbUser).filter(DbUser.id == current_user.id).first()
    if user:
        tasks_to_delete = db.query(DbTask).filter(DbTask.user_id == current_user.id).all()
        for task in tasks_to_delete:
            db.delete(task)
        db.commit()
        return 'Success'

# Create a new tag
def create_tag(name: str):
    db = SessionLocal()
    new_tag = Tag(name=name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    db.close()
    return new_tag

# Get all tags
def get_all_tags():
    db = SessionLocal()
    tags = db.query(Tag).all()
    db.close()
    return tags

# Get tag by ID
def get_tag_by_id(tag_id: int):
    db = SessionLocal()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    db.close()
    return tag

# Update tag by ID
def update_tag(tag_id: int, new_name: str):
    db = SessionLocal()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = new_name
        db.commit()
        db.refresh(tag)
    db.close()
    return tag

# Delete tag by ID
def delete_tag(tag_id: int):
    db = SessionLocal()
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    db.close()
    return tag