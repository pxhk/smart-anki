from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base

class CardType(str, enum.Enum):
    TYPE_IN = "type_in"
    REVERSE = "reverse"
    CLOZE = "cloze"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    categories = relationship("Category", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    is_enabled = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    owner = relationship("User", back_populates="categories")
    subcategories = relationship("Category", backref=ForeignKey("parent"))
    cards = relationship("Card", back_populates="category")

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    type = Column(Enum(CardType))
    front_content = Column(Text)
    back_content = Column(Text)
    metadata = Column(JSON)  # For additional card-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    next_review = Column(DateTime(timezone=True))
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0)
    
    category = relationship("Category", back_populates="cards")
    reviews = relationship("Review", back_populates="card")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    quality = Column(Integer)  # 0-5 rating of recall quality
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    card = relationship("Card", back_populates="reviews")
    user = relationship("User")
