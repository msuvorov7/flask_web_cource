import sqlalchemy
from sqlalchemy.orm import declarative_base
from app.models.users import UserTable

Base = declarative_base()


class PostsTable(Base):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey(UserTable.id))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    title = sqlalchemy.Column(sqlalchemy.String(100))
    content = sqlalchemy.Column(sqlalchemy.Text())
