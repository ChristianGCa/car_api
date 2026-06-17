from typing import Optional, List

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def username_min_length(cls, v):  # Recebe a classe e o valor
        if len(v) < 3:
            raise ValueError('Username deve ter no mínimo 3 caracteres')
        return v

    @field_validator('password')
    def password_min_length(cls, v):  # Recebe a classe e o valor
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        return v



class UserUpdateSchema(BaseModel):
    # Para permitir enviar apenas um ou mais campos para atualizar, deixamos opcionais
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('username')
    def username_min_length(cls, v):  # Recebe a classe e o valor
        if len(v) < 3:
            raise ValueError('Username deve ter no mínimo 3 caracteres')
        return v

    @field_validator('password')
    def password_min_length(cls, v):  # Recebe a classe e o valor
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        return v


# Este Schema mostra apenas os campos públicos do usuário, sem a senha
class UserPublicSchema(BaseModel):
    # Permite criar o schema a partir do modelo SQLAlchemy, ou seja, do User
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int