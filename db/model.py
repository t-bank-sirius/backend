from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text
)

class Model(DeclarativeBase):
    ...


class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chosen_character = mapped_column(ForeignKey('characters.id', ondelete='CASCADE'), nullable=True)
    
    chosen = relationship('Character', foreign_keys=[chosen_character], lazy='selectin')
    characters = relationship('Character', back_populates='user', foreign_keys='Character.user_id', lazy='selectin')


class Character(Model):
    __tablename__ = 'characters'
    
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user = relationship('User', back_populates='characters', foreign_keys=[user_id])

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    is_generated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    avatar_img_url: Mapped[str] = mapped_column(String(220), nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    init_message: Mapped[str] = mapped_column(Text, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(120), nullable=True)