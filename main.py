import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
from chatbot import run_pcos_chatbot

with open('catboost_pcos_model.pkl', 'rb') as f:
    model = pickle.load(f)



app = FastAPI()

# Blood group mapping
bg_map = {
    "A+": 11, "A-": 12, "B+": 13, "B-": 14,
    "O+": 15, "O-": 16, "AB+": 17, "AB-": 18
}

class UserInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    # Define fields once. Use 'alias' so FastAPI accepts the CSV-style names.
    age: Annotated[int, Field(alias='Age (yrs)')]
    weight: Annotated[float, Field(alias='Weight (Kg)')]
    height: Annotated[float, Field(alias='Height(Cm)')]
    bmi: Annotated[float, Field(alias='BMI')]
    blood_group: Annotated[str, Field(alias='Blood Group')]
    pulse_rate: Annotated[float, Field(alias='Pulse rate(bpm)')]
    rr: Annotated[float, Field(alias='RR (breaths/min)')]
    hb: Annotated[float, Field(alias='Hb(g/dl)')]
    cycle_ri: Annotated[int, Field(alias='Cycle(R/I)')]
    cycle_length: Annotated[int, Field(alias='Cycle length(days)')]
    marriage_status: Annotated[float, Field(alias='Marraige Status (Yrs)')]
    pregnant: Annotated[Literal["Yes", "No"], Field(alias='Pregnant(Y/N)')]
    abortions: Annotated[int, Field(alias='No. of aborptions')]
    beta_hcg_i: float = Field(alias='I beta-HCG(mIU/mL)')
    beta_hcg_ii: float = Field(alias='II beta-HCG(mIU/mL)')
    fsh: float = Field(alias='FSH(mIU/mL)')
    lh: float = Field(alias='LH(mIU/mL)')
    fsh_lh: float = Field(alias='FSH/LH')
    hip: float = Field(alias='Hip(inch)')
    waist: float = Field(alias='Waist(inch)')
    waist_hip_ratio: float = Field(alias='Waist:Hip Ratio')
    tsh: float = Field(alias='TSH (mIU/L)')
    amh: float = Field(alias='AMH(ng/mL)')
    prl: float = Field(alias='PRL(ng/mL)')
    vit_d3: float = Field(alias='Vit D3 (ng/mL)')
    prg: float = Field(alias='PRG(ng/mL)')
    rbs: float = Field(alias='RBS(mg/dl)')
    weight_gain: Literal["Yes", "No"] = Field(alias='Weight gain(Y/N)')
    hair_growth: Literal["Yes", "No"] = Field(alias='hair growth(Y/N)')
    skin_darkening: Literal["Yes", "No"] = Field(alias='Skin darkening (Y/N)')
    hair_loss: Literal["Yes", "No"] = Field(alias='Hair loss(Y/N)')
    pimples: Literal["Yes", "No"] = Field(alias='Pimples(Y/N)')
    fast_food: Literal["Yes", "No"] = Field(alias='Fast food (Y/N)')
    reg_exercise: Literal["Yes", "No"] = Field(alias='Reg.Exercise(Y/N)')
    bp_systolic: int = Field(alias='BP _Systolic (mmHg)')
    bp_diastolic: int = Field(alias='BP _Diastolic (mmHg)')
    follicle_no_l: int = Field(alias='Follicle No. (L)')
    follicle_no_r: int = Field(alias='Follicle No. (R)')
    avg_f_size_l: float = Field(alias='Avg. F size (L) (mm)')
    avg_f_size_r: float = Field(alias='Avg. F size (R) (mm)')
    endometrium: float = Field(alias='Endometrium (mm)')

@app.get("/")
async def root():
    return {"message": "PCOS Prediction API is active"}

@app.post("/predict")
async def predict(data: UserInput):
    binary_map = {'Yes': 1, 'No': 0}
    
    # We build the dictionary using the EXACT column names from your dataset
    input_dict = {
        'Age (yrs)': data.age,
        'Weight (Kg)': data.weight,
        'Height(Cm)': data.height,
        'BMI': data.bmi,
        'Blood Group': bg_map.get(data.blood_group, 15), # Defaults to O+ if not found
        'Pulse rate(bpm)': data.pulse_rate,
        'RR (breaths/min)': data.rr,
        'Hb(g/dl)': data.hb,
        'Cycle(R/I)': data.cycle_ri,
        'Cycle length(days)': data.cycle_length,
        'Marraige Status (Yrs)': data.marriage_status,
        'Pregnant(Y/N)': binary_map[data.pregnant],
        'No. of aborptions': data.abortions,
        'I beta-HCG(mIU/mL)': data.beta_hcg_i,
        'II beta-HCG(mIU/mL)': data.beta_hcg_ii,
        'FSH(mIU/mL)': data.fsh,
        'LH(mIU/mL)': data.lh,
        'FSH/LH': data.fsh_lh,
        'Hip(inch)': data.hip,
        'Waist(inch)': data.waist,
        'Waist:Hip Ratio': data.waist_hip_ratio,
        'TSH (mIU/L)': data.tsh,
        'AMH(ng/mL)': data.amh,
        'PRL(ng/mL)': data.prl,
        'Vit D3 (ng/mL)': data.vit_d3,
        'PRG(ng/mL)': data.prg,
        'RBS(mg/dl)': data.rbs,
        'Weight gain(Y/N)': binary_map[data.weight_gain],
        'hair growth(Y/N)': binary_map[data.hair_growth],
        'Skin darkening (Y/N)': binary_map[data.skin_darkening],
        'Hair loss(Y/N)': binary_map[data.hair_loss],
        'Pimples(Y/N)': binary_map[data.pimples],
        'Fast food (Y/N)': binary_map[data.fast_food],
        'Reg.Exercise(Y/N)': binary_map[data.reg_exercise],
        'BP _Systolic (mmHg)': data.bp_systolic,
        'BP _Diastolic (mmHg)': data.bp_diastolic,
        'Follicle No. (L)': data.follicle_no_l,
        'Follicle No. (R)': data.follicle_no_r,
        'Avg. F size (L) (mm)': data.avg_f_size_l,
        'Avg. F size (R) (mm)': data.avg_f_size_r,
        'Endometrium (mm)': data.endometrium
    }
    
    df = pd.DataFrame([input_dict])
    prediction = model.predict(df)
    result = "PCOS Positive" if prediction[0] == 1 else "PCOS Negative"

    return JSONResponse(status_code=200, content={"prediction": result})