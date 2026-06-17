from pydantic import BaseModel, EmailStr, field_validator


# Isso será a resposta do endpoint de login para o cliente
class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr 
    password: str

    @field_validator('password')
    def password_not_empty(cls, value):
        if not value:
            raise ValueError('Password must not be empty')
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return value