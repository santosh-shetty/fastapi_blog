# crud/main.py
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends, File, UploadFile, Form
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import os
import uuid
from sqlalchemy.exc import IntegrityError

# Initialize the application
app = FastAPI()

# Create the database tables
Base.metadata.create_all(engine)

# Directory for saving uploaded images
UPLOAD_DIRECTORY = "upload/images"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Helper function to get the database db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Start Post
@app.get("/post", status_code=status.HTTP_200_OK)
def read_post_list(db: Session = Depends(get_db)):
    post_list = db.query(models.Post).all() 

    return {
        "status": "success",
        "message": "Posts Found Successfully",
        "posts": post_list
    }

@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    categoryId: int = Form(...),
    status: int = Form(1),  
    image: UploadFile = File(...),  
    db: Session = Depends(get_db)
):
    # Save the uploaded image
    _, file_extension = os.path.splitext(image.filename)
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # Create the post record with the image path
    post_db = models.Post(
        title=title,
        content=content,
        categoryId=categoryId,
        status=status,
        image=image_path
    )
    
    try:
        db.add(post_db)
        db.commit()
        db.refresh(post_db)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Database error"
            }
        )

    return {
        "status": "success",
        "message": "Post Created Successfully"
    }
    


@app.get("/post/{id}", status_code=status.HTTP_200_OK)
def read_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id) 
    if not post:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Post with id {id} not found"
            }
        )

    return {
        "status": "success",
        "message": "Post Found Successfully",
        "post": post
    }


@app.put("/post/{id}", status_code=status.HTTP_200_OK)
async def update_post(
    id: int, 
    title: str = Form(...),
    content: str = Form(...),
    categoryId: int = Form(...),
    status: int = Form(1),  
    image: UploadFile = File(None),  
    db: Session = Depends(get_db)):
    
    post_db = db.query(models.Post).get(id)
    if not post_db:
       raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Post with id {id} not found"
            }
        )

    # Update the post attributes
    post_db.title = title
    post_db.content = content
    post_db.categoryId = categoryId
    post_db.status = status

    # If a new image is uploaded, save it and update the image path
    if image:
        _, file_extension = os.path.splitext(image.filename)
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())
        post_db.image = image_path  

    db.commit()
    db.refresh(post_db)
    
    return {
        "status": "success",
        "message": "Post Updated Successfully",
        "post": post_db
    }

@app.delete("/post/delete/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_db = db.query(models.Post).get(id)

    if post_db:
        image_path = os.path.join(UPLOAD_DIRECTORY, post_db.image)
         # Delete the image file if it exists
        if os.path.isfile(image_path):
            os.remove(image_path)
            
        db.delete(post_db)
        db.commit()
        
    else:
       raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Post with id {id} not found"
            }
        )

    return {
        "status": "success",
        "message": "Post Deleted Successfully",
    }

# End Post


# Start Category
@app.get("/category", status_code=status.HTTP_200_OK)
def read_category_list(db: Session = Depends(get_db)):
    category_list = db.query(models.Category).all()  
    return {
        "status": "success",
        "message": "Categories Found Successfully",
        "categories": category_list
    }

@app.post("/category", status_code=status.HTTP_201_CREATED)
async def create_category(
    title: str = Form(...),
    description: str = Form(...),
    status: int = Form(1),  
    db: Session = Depends(get_db)
):
    # Create the category record with the image path
    category_db = models.Category(
        title=title,
        description=description,
        status=status
    )
    
    try:
        db.add(category_db)
        db.commit()
        db.refresh(category_db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "status": "success",
        "message": "Category Created Successfully",
        "category":category_db
    }

    


@app.get("/category/{id}", status_code=status.HTTP_200_OK)
def read_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(id) 
    if not category:
         raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Category with id {id} not found"
            }
        )

    return {
        "status": "success",
        "message": "Post Found Successfully",
        "category":category
    }

@app.put("/category/{id}", status_code=status.HTTP_200_OK)
async def update_category(
    id: int, 
    title: str = Form(...),
    description: str = Form(...),
    status: int = Form(1),  
    db: Session = Depends(get_db)):
    
    category_db = db.query(models.Category).get(id)
    if not category_db:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Category with id {id} not found"
            }
        )

    # Update the category attributes
    category_db.title = title
    category_db.description = description
    category_db.status = status

    db.commit()
    db.refresh(category_db)

    return {
        "status": "success",
        "category": category_db,
        "message": "Category updated successfully"
    }

@app.delete("/category/delete/{id}", status_code=status.HTTP_200_OK)
def delete_category(id: int, db: Session = Depends(get_db)):
    category_db = db.query(models.Category).get(id)

    # Check if category exists
    if not category_db:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Category with id {id} not found"
            }
        )

    try:
        db.delete(category_db)
        db.commit()
    except IntegrityError:
        db.rollback() 
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"Category with id {id} cannot be deleted because it is associated with existing posts or other data."
            }
        )
    return {
        "status": "success",
        "message": "Category deleted successfully"
    }

# End Category

