from sqlalchemy import Column, Integer, String,DateTime, ForeignKey
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship

class Category  (Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    description = Column(String(256))
    status = Column(Integer, default=1)
    createdAt = Column(DateTime, default=datetime.now)
    
    # Define the relationship to Post
    posts = relationship("Post", back_populates="category")

class Post  (Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(256),nullable=False)
    content = Column(String(256),nullable=False)
    categoryId = Column(Integer, ForeignKey('categories.id'), nullable=False) 
    image = Column(String(256),nullable=False) 
    status = Column(Integer, default=1)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now) 

    category = relationship("Category", back_populates = "posts")