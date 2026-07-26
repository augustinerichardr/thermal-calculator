from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Thermal Expansion AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AssemblyInput(BaseModel):
    L1: float
    A1: float
    E1: float
    alpha1: float
    L2: float
    A2: float
    E2: float
    alpha2: float
    delta_T: float

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            return f.read()
    return "<h1>Thermal API Engine Active</h1>"

@app.post("/predict_assembly_stress")
def predict_assembly_stress(data: AssemblyInput):
    free_expansion = (data.alpha1 * data.L1 + data.alpha2 * data.L2) * data.delta_T
    compliance = (data.L1 / (data.A1 * data.E1)) + (data.L2 / (data.A2 * data.E2))
    
    internal_force = free_expansion / compliance
    stress1_MPa = (internal_force / data.A1) / 1e6
    stress2_MPa = (internal_force / data.A2) / 1e6
    
    return {
        "internal_force_kN": round(internal_force / 1000, 2),
        "material_1_stress_MPa": round(stress1_MPa, 2),
        "material_2_stress_MPa": round(stress2_MPa, 2),
    }
