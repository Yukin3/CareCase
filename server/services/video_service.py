from config.database import videos_collection  

def get_all_videos():
    return list(videos_collection.find({}, {"_id": 0}))

def get_video_by_id(video_id: str):
    return videos_collection.find_one({"id": video_id}, {"_id": 0})

def get_videos_for_scenario(scenario_id: str):
    return list(videos_collection.find({"scenario_id": scenario_id}, {"_id": 0}))
