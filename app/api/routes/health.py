from fastapi import APIRouter

#########################  DAY 1 ################################
router = APIRouter()

@router.get("/health")
def health():
    return {"status":"ok"}

