from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_api.models import Base

if TYPE_CHECKING:
    from car_api.models import User


class Brand(Base):
    __tablename__ = 'brands'

    id: Mapped[int] = mapped_column(primary_key=True)
    # String(50) seria como um varchar(50)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),  # Define o valor padrão quando o
        # registro é criado
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    # Isso serve para criar um relacionamento entre a tabela de marcas
    # e a tabela de carros, permitindo acessar os carros de uma marca
    # diretamente a partir do objeto Brand, e também acessar a marca de
    # um carro a partir do objeto Car
    cars: Mapped[List['Car']] = relationship('Car', back_populates='brand')


class Transmission(str, Enum):
    MANUAL = 'manual'
    AUTOMATIC = 'automatic'
    SEMI_AUTOMATIC = 'semi_automatic'
    CVT = 'cvt'


class FuelType(str, Enum):
    GASOLINE = 'gasoline'
    DIESEL = 'diesel'
    FLEX = 'flex'
    ETHANOL = 'ethanol'
    ELECTRIC = 'electric'
    HYBRID = 'hybrid'


class Car(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(primary_key=True)

    model: Mapped[str] = mapped_column(String(100))
    factory_year: Mapped[int] = mapped_column(Integer)
    model_year: Mapped[int] = mapped_column(Integer)
    color: Mapped[str] = mapped_column(String(30))
    # index é para melhorar a performance nas consultas, já que a
    # placa é um campo que provavelmente será consultado
    plate: Mapped[str] = mapped_column(String(10), unique=True, index=True)

    fuel_type: Mapped[FuelType] = mapped_column(String(20))
    transmission: Mapped[Transmission] = mapped_column(String(20))

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    is_available: Mapped[bool] = mapped_column(default=True)

    brand_id: Mapped[int] = mapped_column(
        ForeignKey('brands.id'),
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )

    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        server_default=func.now(),  # Define o valor padrão quando o registro
        # é criado
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    # Isso será uma propriedade que permitirá acessar a marca do carro
    # diretamente a partir do objeto Car, e também permitirá acessar os
    # carros de uma marca a partir do objeto Brand
    brand: Mapped['Brand'] = relationship('Brand', back_populates='cars')

    owner: Mapped['User'] = relationship('User', back_populates='cars')
