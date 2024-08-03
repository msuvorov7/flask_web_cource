import uuid
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String(40), unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String(100))
    hashed_password = sqlalchemy.Column(sqlalchemy.String())
    is_active = sqlalchemy.Column(sqlalchemy.Boolean(), default=True, nullable=False)


class TokensTable(Base):
    __tablename__ = "tokens"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    token = sqlalchemy.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    expires = sqlalchemy.Column(sqlalchemy.DateTime())
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey("users.id"))
