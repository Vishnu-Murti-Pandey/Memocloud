from pydantic import BaseModel

class UserProfileResponse(BaseModel):
    user_id: str
    name: str
    email: str