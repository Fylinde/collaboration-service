from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils.collaboration_utils import calculate_proximity
from app.schemas.collaboration_schemas import LocationRequest
from fastapi.middleware.cors import CORSMiddleware
from app.routes import collaboration, category  # Assuming you have separate route files

# Initialize FastAPI application with Swagger UI metadata
app = FastAPI(
    title="Collaboration Service API",
    description="API for managing seller collaborations, partnerships, and inventory sharing",
    version="1.0.0",
    docs_url="/docs",  # Default URL for Swagger UI
    redoc_url="/redoc",  # Optional: ReDoc UI for alternative documentation interface
)


# Set up CORS
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your collaboration routes

app.include_router(collaboration.router, prefix="/collaboration", tags=["collaboration"])
app.include_router(category.router, prefix="/categories", tags=["categories"])  # Add this line

@app.post("/calculate-proximity/")
def calculate_proximity_endpoint(locations: LocationRequest):
    try:
        distance = calculate_proximity(locations.location1, locations.location2)
        return {"distance": distance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Collaboration Service is running"}
