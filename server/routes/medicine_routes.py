from fastapi import APIRouter, HTTPException, Query
from services.medicine_service import get_all_medicines, get_medicine_by_id

router = APIRouter()

@router.get("/medicines")
def all_medicines(name: str = None, category: str = None, limit: int = Query(20, ge=1, le=100),skip: int = Query(0, ge=0) ):
    return get_all_medicines(name=name, category=category, limit=limit, skip=skip)

@router.get("/medicine")
def medicine_by_id(id: str):
    medicine = get_medicine_by_id(id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine
