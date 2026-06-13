# metadata.py

from app.database.base import Base

from app.models.user import User

print(User.__tablename__)

print(Base.metadata.tables.keys())