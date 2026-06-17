from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class BrandSchema(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

    @field_validator('name')
    def name_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('O nome da marca deve ter no mínimo 2 caracteres')
        return v.strip()


class BrandUpdateSchema(BaseModel):
    # Não é obrigado a enviar todos os campos para atualizar, por isso são opcionais
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

    @field_validator('name')
    def name_min_length(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('O nome da marca deve ter no mínimo 2 caracteres')
        return v.strip()


class BrandPublicSchema(BaseModel):
    # Para criar um PublicSchema atraves do modelo SQLAlchemy, ou seja, da Brand
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class BrandListPublicSchema(BaseModel):
    brands: List[BrandPublicSchema]
    offset: int
    limit: int
