from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from datetime import datetime
import joblib
import pandas as pd

_version_ = 1
app = FastAPI(version=str(_version_))

class SprintRequest(BaseModel):
    team_seniority_ratio: float = Field(..., ge=0.0, le=1.0, description="Ratio of senior devs (0.0 to 1.0)")
    code_churn_lines: int = Field(..., ge=0, description="Expected lines of code changed")
    project_type: str = Field(..., description="e.g., Backend, Frontend, DevOps")
    sprint_description: str = Field(..., description="Details of the sprint tasks")
    
class SprintResponse(BaseModel):
    risk_probability:float
    risk_flag:float
    primary_risk_factor:list[str]

origins = [
    "http://localhost:8070",
    "http:/127.0.0.1:8070"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],             
    allow_headers=["*"],            
)

try:
    model = joblib.load(f"models/trained_model/trained_model_v{_version_}_{datetime.now().strftime('%Y-%m-%d')}.pkl")
except Exception as e:
    print(f"Warning: Model not found at model_path. Please train the model first!")
    model = None

@app.post("/predict",response_model=SprintResponse)
def predict(info:SprintRequest):
    
    if not model:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server.")
    
    input_df = pd.DataFrame([info.model_dump()]) 
    probability = float(model.predict_proba(input_df)[0][1])
   
    
    is_risky = probability > 0.50
    risk_factors = []
    if is_risky:
        if info.code_churn_lines > 4000:
            risk_factors.append("Exceptionally high code churn predicted.")
        if info.team_seniority_ratio < 0.40:
            risk_factors.append("Low team seniority assigned to this workload.")
        if "legacy" in info.sprint_description.lower():
            risk_factors.append("Sprint involves legacy systems, which historically carry high risk.")
    
    
    return SprintResponse(
        risk_probability=round(probability,4),
        risk_flag=is_risky,
        primary_risk_factor=risk_factors
    )