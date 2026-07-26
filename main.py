from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
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

@app.get("/manifest.json")
def get_manifest():
    if os.path.exists("manifest.json"):
        return FileResponse("manifest.json")
    return {"error": "manifest.json not found"}

@app.get("/icon-192.png")
def get_icon_192():
    return FileResponse("icon-192.png", media_type="image/png")

@app.get("/icon-512.png")
def get_icon_512():
    return FileResponse("icon-512.png", media_type="image/png")

@app.post("/predict_assembly_stress")
def predict_assembly_stress(data: AssemblyInput):
    P = (data.alpha1 * data.L1 + data.alpha2 * data.L2) * data.delta_T / ((data.L1 / (data.A1 * data.E1)) + (data.L2 / (data.A2 * data.E2)))
    sigma1 = P / data.A1
    sigma2 = P / data.A2
    return {
        "internal_force_kN": round(P / 1000, 2),
        "material_1_stress_MPa": round(sigma1 / 1e6, 2),
        "material_2_stress_MPa": round(sigma2 / 1e6, 2)
    }
