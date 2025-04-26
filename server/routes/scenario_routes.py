from fastapi import APIRouter, HTTPException
from services.scenario_service import get_all_scenarios, get_scenario_by_id

router = APIRouter()

@router.get("/scenarios")
def fetch_scenarios():
    return get_all_scenarios()

@router.get("/scenario")
def fetch_single_scenario(id: str):
    scenario = get_scenario_by_id(id)
    if scenario:
        return scenario
    raise HTTPException(status_code=404, detail="Scenario not found")
