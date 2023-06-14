import enum 

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column, Text, Integer, 
    ForeignKey, BigInteger, String, 
    Boolean, DECIMAL, func, DateTime, Enum
    )


Base = declarative_base()

class StatusChoices(enum.Enum):
    active = "active"
    ordering = "ordering"
    completed = "completed"
    rejected = "rejected"





class User(Base):
    __tablename__='cafe_user'
    tg_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    name = Column(String(50))
    is_active = Column(Boolean, default=True)


class CafeOrder(Base):
    __tablename__ = "cafe_order"
    id = Column(Integer, primary_key=True)
    cafe_url = Column(String(4048),nullable=False)
    notice = Column(Text)
    total_sum = Column(DECIMAL(10,2))
    created = Column(DateTime, default=func.now())
    status = Column(Enum(StatusChoices), nullable=False, default=StatusChoices.active)


class UserOrder(Base):
    __tablename__ = "user_order"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.tg_id'), nullable=False)
    order = Column(Integer, ForeignKey('cafe_order.id'), nullable=False)
    text = Column(Text, nullable=False)
    is_paid = Column(Boolean, default=False)
    created = Column(DateTime, default=func.now())
