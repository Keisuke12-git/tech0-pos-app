from sqlalchemy import String, Integer #ForeignKey は別テーブルと同じ列を作るときに使う
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = 'products'
    product_code: Mapped[str] = mapped_column(String(13), primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100))
    price_excl_tax: Mapped[int] = mapped_column(Integer)