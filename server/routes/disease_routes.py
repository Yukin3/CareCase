from fastapi import APIRouter, HTTPException
from services.disease_service import get_unique_diseases, get_random_profile_for_disease

router = APIRouter()

@router.get("/diseases")
def fetch_diseases():
    return get_unique_diseases()

@router.get("/disease/profile")
def fetch_random_profile(disease: str):
    profile = get_random_profile_for_disease(disease)
    if not profile:
        raise HTTPException(status_code=404, detail="Disease profile not found")
    
    profile["_id"] = str(profile["_id"])  # sanitize Mongo _id
    return profile
