from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slogan = Column(String(300), nullable=True)
    logo_path = Column(String(500), nullable=True)
    address = Column(String(300), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    website = Column(String(200), nullable=True)
    ruc = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
