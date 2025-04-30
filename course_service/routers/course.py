from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_courses():
    return {"courses": ["Math", "Science"]}
