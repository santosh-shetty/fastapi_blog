from pydantic import BaseModel

# Start Post 
class PostCreate(BaseModel):
    title: str
    content: str
    categoryId: int
    status:int = 1
    image: str

    class Config:
        orm_mode = True

class Post(PostCreate):
    id: int
# End Post

# Start Category 
class CategoryCreate(BaseModel):
    title: str
    description: str
    status:int = 1

    class Config:
        orm_mode = True

class Category(CategoryCreate):
    id: int
# End Post