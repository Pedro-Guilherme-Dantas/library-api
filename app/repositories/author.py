from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from datetime import date

if TYPE_CHECKING:
    from app.models import Author

class AuthorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, slug: str, date_of_birth: date, 
               biography: str = None, date_of_death: date = None) -> Author:
        author = Author(
            name=name,
            slug=slug,
            date_of_birth=date_of_birth,
            date_of_death=date_of_death,
            biography=biography
        )
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return self.session.query(Author).filter(Author.id == author_id).first()

    def get_by_slug(self, slug: str) -> Optional[Author]:
        return self.session.query(Author).filter(Author.slug == slug).first()

    def get_all(self) -> List[Author]:
        return self.session.query(Author).all()

    def search_by_name(self, name: str) -> List[Author]:
        return self.session.query(Author).filter(
            Author.name.ilike(f"%{name}%")
        ).all()

    def get_living_authors(self) -> List[Author]:
        return self.session.query(Author).filter(
            Author.date_of_death.is_(None)
        ).all()

    def update(self, author_id: int, **kwargs) -> Optional[Author]:
        author = self.get_by_id(author_id)
        if author:
            for key, value in kwargs.items():
                if hasattr(author, key):
                    setattr(author, key, value)
            self.session.commit()
            self.session.refresh(author)
        return author

    def delete(self, author_id: int) -> bool:
        author = self.get_by_id(author_id)
        if author:
            self.session.delete(author)
            self.session.commit()
            return True
        return False
