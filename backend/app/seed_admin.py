from sqlalchemy.exc import IntegrityError
from app.core.config import ADMIN_EMAIL, ADMIN_FULL_NAME, ADMIN_PASSWORD
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


def seed_admin() -> None:
    if not ADMIN_PASSWORD or ADMIN_PASSWORD == 'change_me':
        raise RuntimeError('ADMIN_PASSWORD chưa được cấu hình an toàn trong backend/.env')
    repository = UserRepository()
    with SessionLocal() as db:
        existing = repository.get_by_email(db, ADMIN_EMAIL)
        if existing:
            print(f'Admin đã tồn tại: {existing.email}. Không thay đổi mật khẩu hoặc dữ liệu hiện có.')
            return
        admin = User(
            full_name=ADMIN_FULL_NAME or 'TaloFood Admin',
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            role='ADMIN',
            is_active=True,
        )
        try:
            repository.create(db, admin)
        except IntegrityError:
            db.rollback()
            print(f'Admin đã tồn tại: {ADMIN_EMAIL}')
            return
        print(f'Đã tạo admin: {ADMIN_EMAIL}')


if __name__ == '__main__':
    seed_admin()
