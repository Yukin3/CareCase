from fastapi import APIRouter, HTTPException
from services.video_service import get_all_videos, get_video_by_id, get_videos_for_scenario

router = APIRouter()

@router.get("/videos")
def all_videos(scenario: str = None):
    if scenario:
        return get_videos_for_scenario(scenario)
    return get_all_videos()

@router.get("/videos/scenario")
def videos_for_scenario(scenario_id: str):
    return get_videos_for_scenario(scenario_id)

@router.get("/video")
def video_by_id(id: str):
    video = get_video_by_id(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
