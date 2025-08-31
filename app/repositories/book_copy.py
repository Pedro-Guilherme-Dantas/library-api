from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, date

if TYPE_CHECKING:
    from app.models import BookCopy, CopyStatus

class BookCopyRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, book_id: int, condition_notes: str = None, 
               status: CopyStatus = CopyStatus.AVAILABLE) -> BookCopy:
        book_copy = BookCopy(
            book_id=book_id,
            condition_notes=condition_notes,
            status=status
        )
        self.session.add(book_copy)
        self.session.commit()
        self.session.refresh(book_copy)
        return book_copy

    def get_by_id(self, copy_id: int) -> Optional[BookCopy]:
        return self.session.query(BookCopy).filter(BookCopy.id == copy_id).first()

    def get_all(self) -> List[BookCopy]:
        return self.session.query(BookCopy).all()

    def get_by_book(self, book_id: int) -> List[BookCopy]:
        return self.session.query(BookCopy).filter(
            BookCopy.book_id == book_id
        ).all()

    def get_available_copies(self, book_id: int) -> List[BookCopy]:
        return self.session.query(BookCopy).filter(
            and_(
                BookCopy.book_id == book_id,
                BookCopy.status == CopyStatus.AVAILABLE
            )
        ).all()

    def get_all_available(self) -> List[BookCopy]:
        return self.session.query(BookCopy).filter(
            BookCopy.status == CopyStatus.AVAILABLE
        ).all()

    def get_loaned_copies(self) -> List[BookCopy]:
        return self.session.query(BookCopy).filter(
            BookCopy.status == CopyStatus.LOANED
        ).all()

    def update_status(self, copy_id: int, status: CopyStatus) -> Optional[BookCopy]:
        copy = self.get_by_id(copy_id)
        if copy:
            copy.status = status
            self.session.commit()
            self.session.refresh(copy)
        return copy

    def update(self, copy_id: int, **kwargs) -> Optional[BookCopy]:
        copy = self.get_by_id(copy_id)
        if copy:
            for key, value in kwargs.items():
                if hasattr(copy, key):
                    setattr(copy, key, value)
            self.session.commit()
            self.session.refresh(copy)
        return copy

    def delete(self, copy_id: int) -> bool:
        copy = self.get_by_id(copy_id)
        if copy:
            self.session.delete(copy)
            self.session.commit()
            return True
        return False
