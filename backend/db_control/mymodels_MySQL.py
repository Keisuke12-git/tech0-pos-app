from datetime import datetime, date
from sqlalchemy import String, Integer, BigInteger, DateTime, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = 'products'
    product_code: Mapped[str] = mapped_column(String(13), primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100))
    price_excl_tax: Mapped[int] = mapped_column(Integer)


class Staffs(Base):
    __tablename__ = 'staffs'
    staff_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    staff_name: Mapped[str] = mapped_column(String(100))
    staff_password: Mapped[str] = mapped_column(String(16))


class Transactions(Base):
    __tablename__ = 'transactions'
    transaction_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    transaction_datetime: Mapped[datetime] = mapped_column(DateTime)
    staff_id: Mapped[str] = mapped_column(String(10), ForeignKey("staffs.staff_id"))
    member_id: Mapped[str] = mapped_column(String(8), nullable=True) #会員マスタ未実装のためForeignKeyは未設定
    tax_rate: Mapped[float] = mapped_column(DECIMAL(3, 2))
    total_excl_tax: Mapped[int] = mapped_column(Integer)
    tax_amount: Mapped[int] = mapped_column(Integer)
    total_incl_tax: Mapped[int] = mapped_column(Integer)


class TransactionDetails(Base):
    __tablename__ = 'transaction_details'
    transaction_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("transactions.transaction_id"), primary_key=True)
    line_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_code: Mapped[str] = mapped_column(String(13), ForeignKey("products.product_code"))
    product_name: Mapped[str] = mapped_column(String(100))
    price_excl_tax: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    subtotal_excl_tax: Mapped[int] = mapped_column(Integer)

class TaxRates(Base):
    __tablename__ = 'tax_rates'
    effective_date: Mapped[date] = mapped_column(Date, primary_key=True)
    tax_rate: Mapped[float] = mapped_column(DECIMAL(3, 2))