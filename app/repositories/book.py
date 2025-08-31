from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from app.models import Book
    from app.models import BookCopy, CopyStatus

class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, isbn: str, year: int, category_id: int, 
               author_id: int, description: str = None) -> Book:
        book = Book(
            title=title,
            isbn=isbn,
            description=description,
            year=year,
            category_id=category_id,
            author_id=author_id
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.session.query(Book).filter(Book.id == book_id).first()

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.session.query(Book).filter(Book.isbn == isbn).first()

    def get_all(self) -> List[Book]:
        return self.session.query(Book).all()

    def get_by_category(self, category_id: int) -> List[Book]:
        return self.session.query(Book).filter(Book.category_id == category_id).all()

    def get_by_author(self, author_id: int) -> List[Book]:
        return self.session.query(Book).filter(Book.author_id == author_id).all()

    def search_by_title(self, title: str) -> List[Book]:
        return self.session.query(Book).filter(
            Book.title.ilike(f"%{title}%")
        ).all()

    def get_available_books(self) -> List[Book]:
        return self.session.query(Book).join(BookCopy).filter(
            BookCopy.status == CopyStatus.AVAILABLE
        ).distinct().all()

    def update(self, book_id: int, **kwargs) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if book:
            for key, value in kwargs.items():
                if hasattr(book, key):
                    setattr(book, key, value)
            self.session.commit()
            self.session.refresh(book)
        return book

    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book:
            self.session.delete(book)
            self.session.commit()
            return True
        return False
