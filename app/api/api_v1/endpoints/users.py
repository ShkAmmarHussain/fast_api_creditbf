from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"username": "User1"}, {"username": "User2"}]

@router.get("/name")
async def read_users():
    return [{"username": "User1"}, {"username": "User2"}]
