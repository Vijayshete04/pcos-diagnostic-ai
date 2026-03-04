import streamlit as st
import requests
import time
from chatbot import run_pcos_chatbot
# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PCOS Diagnosis AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PERSONAL DATA ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864345.png", width=100)
    st.title("Patient Profile")
    st.subheader("Personal Details")
    age = st.slider("Age (yrs)", 15, 50, 25)
    weight = st.number_input("Weight (Kg)", 30.0, 150.0, 60.0)
    height = st.number_input("Height (Cm)", 120.0, 220.0, 160.0)
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    marriage = st.number_input("Years of Marriage", 0.0, 40.0, 2.0)
    
    st.divider()
    st.caption("AI Diagnostic Tool v2.0")



# --- MAIN PANEL ---
st.title("🩺 PCOS Advanced Diagnostic System")
st.info("Fill in your symptoms below. Our AI will analyze clinical markers and lifestyle factors.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🩸 Menstrual Cycle")
    cycle_ri = st.radio("Cycle Regularity", ["Regular", "Irregular"], horizontal=True)
    cycle_len = st.number_input("Average Cycle length (days)", 2, 60, 28)
    pregnant = st.selectbox("Current Pregnancy Status", ["No", "Yes"])
    abortions = st.number_input("Number of previous abortions", 0, 10, 0)

with col2:
    st.subheader("✨ Physical Symptoms")
    # Use multi-column for small toggles to save space
    c2a, c2b = st.columns(2)
    weight_gain = c2a.checkbox("Sudden Weight Gain")
    hair_loss = c2b.checkbox("Hair Thinning/Loss")
    skin_dark = c2a.checkbox("Skin Darkening")
    hair_growth = c2b.checkbox("Excess Body Hair")
    pimples = c2a.checkbox("Persistent Acne")
    fast_food = c2b.checkbox("Frequent Fast Food")
    exercise = st.toggle("Exercise Regularly", value=True)

with st.expander("🔬 Clinical/Lab Metrics (Advanced)"):
    st.write("These values help increase prediction accuracy.")
    lc1, lc2, lc3 = st.columns(3)
    pulse = lc1.number_input("Pulse (bpm)", value=72.0)
    lh = lc2.number_input("LH (mIU/mL)", value=4.5)
    fsh = lc3.number_input("FSH (mIU/mL)", value=5.5)
    f_l = lc1.number_input("Follicle No. (Left)", value=5)
    f_r = lc2.number_input("Follicle No. (Right)", value=6)

# --- PREDICTION LOGIC ---
st.divider()
if st.button("🚀 Analyze My Health Data"):
    
    # Simple interaction: Progress bar
    with st.status("Analyzing biomarkers...", expanded=True) as status:
        st.write("Calculating BMI...")
        bmi = float(weight / ((height/100)**2))
        time.sleep(0.5)
        st.write("Checking hormonal balance...")
        time.sleep(0.5)
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # Prepare payload (Mapping UI to Model keys)
    def yn(val): return "Yes" if val else "No"
    
    payload = {
        "Age (yrs)": int(age),
        "Weight (Kg)": float(weight),
        "Height(Cm)": float(height),
        "BMI": float(bmi),
        "Blood Group": blood_group,
        "Cycle(R/I)": 2 if cycle_ri == "Regular" else 4,
        "Cycle length(days)": int(cycle_len),
        "Marraige Status (Yrs)": float(marriage),
        "Pregnant(Y/N)": pregnant,
        "No. of aborptions": int(abortions),
        "Weight gain(Y/N)": yn(weight_gain),
        "hair growth(Y/N)": yn(hair_growth),
        "Skin darkening (Y/N)": yn(skin_dark),
        "Hair loss(Y/N)": yn(hair_loss),
        "Pimples(Y/N)": yn(pimples),
        "Fast food (Y/N)": yn(fast_food),
        "Reg.Exercise(Y/N)": yn(exercise),
        # Hidden/Expanded values
        "Pulse rate(bpm)": pulse,
        "FSH(mIU/mL)": fsh,
        "LH(mIU/mL)": lh,
        "Follicle No. (L)": f_l,
        "Follicle No. (R)": f_r,
        # Default fillers for remaining 41 features
        "RR (breaths/min)": 18.0, "Hb(g/dl)": 12.0, "I beta-HCG(mIU/mL)": 1.9,
        "II beta-HCG(mIU/mL)": 1.9, "FSH/LH": fsh/lh if lh != 0 else 1.0,
        "Hip(inch)": 38.0, "Waist(inch)": 32.0, "Waist:Hip Ratio": 0.84,
        "TSH (mIU/L)": 2.1, "AMH(ng/mL)": 2.5, "PRL(ng/mL)": 18.0,
        "Vit D3 (ng/mL)": 25.0, "PRG(ng/mL)": 0.4, "RBS(mg/dl)": 100.0,
        "BP _Systolic (mmHg)": 110, "BP _Diastolic (mmHg)": 80,
        "Avg. F size (L) (mm)": 15.0, "Avg. F size (R) (mm)": 16.0, "Endometrium (mm)": 8.0
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json().get("prediction")
            # Inside your 'Analyze' button logic, after getting the 200 response:
            result = response.json().get("prediction")
            st.session_state['diagnosis_result'] = result
            st.session_state['show_chat'] = True
            
            # --- INTERACTIVE RESULTS ---
            st.subheader("📊 Diagnostic Summary")
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.metric(label="Calculated BMI", value=f"{bmi:.1f}")
            
            with res_col2:
                if "Positive" in result:
                    st.error(f"### Result: {result}")
                    st.warning("⚠️ High Correlation Detected. It is recommended to schedule an appointment with a gynecologist for an ultrasound.")
                else:
                    st.success(f"### Result: {result}")
                    st.balloons()
                    st.info("✅ Your indicators appear within the normal range. Continue maintaining a healthy lifestyle!")
            
            # Advice section
            with st.expander("See Recommendations"):
                st.write("""
                * **Diet:** Increase fiber and reduce processed sugars.
                * **Activity:** Aim for 30 mins of moderate activity 5x a week.
                * **Monitor:** Keep a log of your menstrual cycle variations.
                """)
        else:
            st.error(f"Server Error: {response.text}")
    except Exception as e:
        st.error("🔌 Backend Connection Failed. Is the FastAPI server running?")

st.write("")
st.caption("Disclaimer: This tool is for educational purposes only and does not replace professional medical diagnosis.")

# --- CHATBOT SECTION ---
# This must be outside the 'if st.button' block so it persists
if st.session_state.get('show_chat'):
    # Prepare the stats to give context to the AI
    patient_info = {
        "age": age,
        "bmi": float(weight / ((height/100)**2))
    }
    
    # This calls the function from your chatbot.py file
    run_pcos_chatbot(st.session_state['diagnosis_result'], patient_info)