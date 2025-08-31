from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from app.models import Category
import re

if TYPE_CHECKING:
    from app.models import Category

class CategoryRepository():
    def __init__(self, session: Session):
        self.session = session

    def generate_slug(self, name: str) -> str:
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

    def create(self, name: str, description: str = None) -> Category:
        category = Category(
            name=name,
            slug=self.generate_slug(name),
            description=description
        )
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.session.query(Category).filter(Category.id == category_id).first()

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.session.query(Category).filter(Category.slug == slug).first()

    def get_all(self) -> List[Category]:
        return self.session.query(Category).all()

    def get_with_books(self, category_id: int) -> Optional[Category]:
        return self.session.query(Category).filter(
            Category.id == category_id
        ).first()

    def update(self, category_id: int, **kwargs) -> Optional[Category]:
        category = self.get_by_id(category_id)
        if category:
            for key, value in kwargs.items():
                if hasattr(category, key):
                    setattr(category, key, value)
            self.session.commit()
            self.session.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if category:
            self.session.delete(category)
            self.session.commit()
            return True
        return False
