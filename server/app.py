from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.scenario_routes import router as scenario_router
from routes.script_routes import router as script_router
from routes.video_routes import router as video_router
from routes.log_routes import router as log_router
from routes.preceptor_routes import router as preceptor_router
from routes.medicine_routes import router as medicine_router
from routes.disease_routes import router as disease_router


app = FastAPI()

app.include_router(scenario_router)
app.include_router(script_router)
app.include_router(video_router)
app.include_router(log_router)
app.include_router(preceptor_router)
app.include_router(medicine_router)
app.include_router(disease_router)
app.mount("/images", StaticFiles(directory="images"), name="images")

# Optional root
@app.get("/")
def root():
    return {"message": "CareCase API"}
