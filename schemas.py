from datetime import date, datetime, time
from pydantic import BaseModel
<<<<<<< Updated upstream
=======
from typing import Optional, List


class TagBase(BaseModel):
    name: str

class TagDisplay(BaseModel):
    id: int
    name: str

>>>>>>> Stashed changes

class TaskBase(BaseModel):
    title:str='Task'
    description:str='Something to do'
<<<<<<< Updated upstream
=======
    image_url: Optional[str] = None
    image_url_type: Optional[str] = None
    tags: Optional[List[TagBase]] = None
>>>>>>> Stashed changes

class TaskDisplay(BaseModel):
    title:str
    description:str
    task_status:str
    priority:str
    flag:bool
    date:date
    time:time
    folder_id:int 
<<<<<<< Updated upstream
=======
    image_url: Optional[str] = None
    image_url_type: Optional[str] = None
    tags: Optional[List[TagDisplay]] = None
>>>>>>> Stashed changes

    class Config:
      orm_mode = True
      json_encoders = {
            date: lambda v: v.strftime("%d.%m.%Y"),
            time: lambda v: v.strftime("%H:%M")
        }


class FolderDisplay(BaseModel):
    title:str

class UserBase(BaseModel):
  username: str='User'
  email: str='user@gmail.com'
  password: str

class UserDisplay(BaseModel):
  username: str
  email: str
  class Config():
    orm_mode = True

