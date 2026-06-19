from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from car_api.models.cars import FuelType, Transmission
from car_api.schemas.brands import BrandPublicSchema
from car_api.schemas.users import UserPublicSchema


class CarSchema(BaseModel):
    model: str
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: FuelType
    transmission: Transmission
    price: Decimal
    description: Optional[str] = None
    is_available: bool = True
    brand_id: int
    owner_id: int

    @field_validator('model')
    def model_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError(
                'O modelo do carro deve ter no mínimo 2 caracteres'
            )
        return v.strip()

    @field_validator('color')
    def color_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('A cor do carro deve ter no mínimo 2 caracteres')
        return v.strip()

    @field_validator('plate')
    def plate_format(cls, v):
        plate = v.strip().upper()
        if len(plate) < 7 or len(plate) > 10:
            raise ValueError(
                'A placa do carro deve ter entre 7 e 10 caracteres'
            )
        return plate

    @field_validator('factory_year', 'model_year')
    def year_validation(cls, v):
        if v < 1886 or v > datetime.now().year:
            raise ValueError('O ano do carro deve ser válido')
        return v

    @field_validator('price')
    def price_validation(cls, v):
        if v is None or v <= 0:
            raise ValueError(
                'O preço do carro é obrigatório e deve ser maior que zero'
            )
        return v


class CarUpdateSchema(BaseModel):
    model: Optional[str] = None
    factory_year: Optional[int] = None
    model_year: Optional[int] = None
    color: Optional[str] = None
    plate: Optional[str] = None
    fuel_type: Optional[FuelType] = None
    transmission: Optional[Transmission] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    is_available: Optional[bool] = True
    brand_id: Optional[int] = None
    owner_id: Optional[int] = None

    @field_validator('model')
    def model_min_length(cls, v):
        if v is None:
            return v
        if len(v.strip()) < 2:
            raise ValueError(
                'O modelo do carro deve ter no mínimo 2 caracteres'
            )
        return v.strip()

    @field_validator('color')
    def color_min_length(cls, v):
        if v is None:
            return v
        if len(v.strip()) < 2:
            raise ValueError('A cor do carro deve ter no mínimo 2 caracteres')
        return v.strip()

    @field_validator('plate')
    def plate_format(cls, v):
        if v is None:
            return v
        plate = v.strip().upper()
        if len(plate) < 7 or len(plate) > 10:
            raise ValueError(
                'A placa do carro deve ter entre 7 e 10 caracteres'
            )
        return plate

    @field_validator('factory_year', 'model_year')
    def year_validation(cls, v):
        if v is None:
            return v
        if v < 1886 or v > datetime.now().year:
            raise ValueError('O ano do carro deve ser válido')
        return v

    @field_validator('price')
    def price_validation(cls, v):
        if v is None:
            return v
        if v <= 0:
            raise ValueError('O preço do carro deve ser maior que zero')
        return v


class CarPublicSchema(CarSchema):
    # Perimitir que os campos sejam populados a partir de atributos do
    # modelo ORM
    model_config = ConfigDict(from_attributes=True)
    id: int
    model: str
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: FuelType
    transmission: Transmission
    price: Decimal
    description: Optional[str] = None
    is_available: bool = True
    brand_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    brand: BrandPublicSchema
    owner: UserPublicSchema


class CarListPublicSchema(BaseModel):
    cars: List[CarPublicSchema]
    offset: int
    limit: int
