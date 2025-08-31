from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

if TYPE_CHECKING:
    from app.models import Loan, LoanStatus
    from app.models import BookCopy, CopyStatus

class LoanRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, book_copy_id: int, due_date: datetime) -> Loan:
        loan = Loan(
            user_id=user_id,
            book_copy_id=book_copy_id,
            due_date=due_date,
            status=LoanStatus.ACTIVE
        )
        self.session.add(loan)

        book_copy = self.session.query(BookCopy).filter(
            BookCopy.id == book_copy_id
        ).first()
        if book_copy:
            book_copy.status = CopyStatus.LOANED

        self.session.commit()
        self.session.refresh(loan)
        return loan

    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        return self.session.query(Loan).filter(Loan.id == loan_id).first()

    def get_all(self) -> List[Loan]:
        return self.session.query(Loan).all()

    def get_active_loans(self) -> List[Loan]:
        return self.session.query(Loan).filter(
            Loan.status == LoanStatus.ACTIVE
        ).all()

    def get_overdue_loans(self) -> List[Loan]:
        return self.session.query(Loan).filter(
            and_(
                Loan.status == LoanStatus.ACTIVE,
                Loan.due_date < datetime.now()
            )
        ).all()

    def get_user_loans(self, user_id: int) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.user_id == user_id).all()

    def get_user_active_loans(self, user_id: int) -> List[Loan]:
        return self.session.query(Loan).filter(
            and_(
                Loan.user_id == user_id,
                Loan.status == LoanStatus.ACTIVE
            )
        ).all()

    def return_loan(self, loan_id: int, return_date: datetime = None) -> Optional[Loan]:
        loan = self.get_by_id(loan_id)
        if loan and loan.status == LoanStatus.ACTIVE:
            loan.return_date = return_date or datetime.now()
            loan.status = LoanStatus.RETURNED

            book_copy = loan.book_copy
            if book_copy:
                book_copy.status = CopyStatus.AVAILABLE

            self.session.commit()
            self.session.refresh(loan)
        return loan

    def update(self, loan_id: int, **kwargs) -> Optional[Loan]:
        loan = self.get_by_id(loan_id)
        if loan:
            for key, value in kwargs.items():
                if hasattr(loan, key):
                    setattr(loan, key, value)
            self.session.commit()
            self.session.refresh(loan)
        return loan

    def delete(self, loan_id: int) -> bool:
        loan = self.get_by_id(loan_id)
        if loan:
            self.session.delete(loan)
            self.session.commit()
            return True
        return False
