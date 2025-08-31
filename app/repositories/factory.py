from sqlalchemy.orm import Session
from .book import BookRepository
from .author import AuthorRepository
from .category import CategoryRepository
from .user import UserRepository
from .loan import LoanRepository
from .book_copy import BookCopyRepository

class RepositoryFactory:
    def __init__(self, session: Session):
        self.session = session

    @property
    def categories(self) -> CategoryRepository:
        return CategoryRepository(self.session)

    @property
    def books(self) -> BookRepository:
        return BookRepository(self.session)

    @property
    def authors(self) -> AuthorRepository:
        return AuthorRepository(self.session)

    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)

    @property
    def loans(self) -> LoanRepository:
        return LoanRepository(self.session)

    @property
    def book_copies(self) -> BookCopyRepository:
        return BookCopyRepository(self.session)
