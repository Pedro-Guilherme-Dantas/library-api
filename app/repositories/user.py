from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from app.models import User
    from app.models import Loan, LoanStatus

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, email: str, username: str, full_name: str, 
               hashed_password: str, is_admin: bool = False) -> User:
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def get_admins(self) -> List[User]:
        return self.session.query(User).filter(User.is_admin == True).all()

    def get_users_with_active_loans(self) -> List[User]:
        return self.session.query(User).join(Loan).filter(
            Loan.status == LoanStatus.ACTIVE
        ).distinct().all()

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.commit()
            self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
