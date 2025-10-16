
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    Email: str = Field(..., description="User email")
    Password: str = Field(..., description="User password")
    RememberMe: str = Field("false", description="Remember flag: true/false")
