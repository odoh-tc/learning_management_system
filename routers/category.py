from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schema.category import CategoryCreate, CategoryResponse
from services.category import create_category, get_category, get_categories, update_category, delete_category
from services.auth import get_current_user  # Assuming this function exists and provides current user details

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
def create_new_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admins can create categories")
    return create_category(db=db, category=category)

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(
    category_id: int, 
    category: CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admins can update categories")
    updated_category = update_category(db=db, category_id=category_id, category=category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_existing_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admins can delete categories")
    deleted_category = delete_category(db=db, category_id=category_id)
    if deleted_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted_category
