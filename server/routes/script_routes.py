from fastapi import APIRouter, HTTPException
from services.script_service import get_all_scripts, get_script_by_id, get_scripts_for_scenario

router = APIRouter()

@router.get("/scripts")
def all_scripts(scenario: str = None):
    if scenario:
        return get_scripts_for_scenario(scenario) #All for scenario
    return get_all_scripts() #ALL

@router.get("/scripts/scenario") #Scenario scripts
def scripts_for_scenario(scenario_id: str):
    scripts = get_scripts_for_scenario(scenario_id)
    return scripts

@router.get("/script") #Specifc script
def script_by_id(id: str):
    script = get_script_by_id(id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script

