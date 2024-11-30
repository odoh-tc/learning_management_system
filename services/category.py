from sqlalchemy.orm import Session
from schema.category import CategoryCreate
from models import Category
from typing import List, Optional

def create_category(db: Session, category: CategoryCreate) -> Category:
    """
    Create a new category in the database.
    """
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int) -> Optional[Category]:
    """
    Retrieve a category by its ID.
    """
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10) -> List[Category]:
    """
    Retrieve a list of categories with pagination.
    """
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category: CategoryCreate) -> Optional[Category]:
    """
    Update an existing category by ID.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> Optional[Category]:
    """
    Delete a category by ID.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category
