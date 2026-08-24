from pydantic import BaseModel, EmailStr


class BaseCredentialsSchema(BaseModel):
    email: EmailStr
    password: str
