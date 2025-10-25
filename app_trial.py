import streamlit as st
import json
from itertools import combinations
import math
from datetime import date, timedelta

# ------------------ APP CONFIG ------------------
st.set_page_config(page_title="Crux Med", layout="wide")

# Load favicon & manifest
st.markdown("""
<link rel="icon" href="static/favicon.ico" type="image/x-icon">
<link rel="manifest" href="manifest.json">
""", unsafe_allow_html=True)

# Inject install button
with open("pwa-install.html", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)


# ------------------- Hide Hamburger Menu -------------------
hide_hamburger_css = """
<style>
/* Hide the top-right hamburger menu */
#MainMenu {visibility: hidden;}
</style>
"""
st.markdown(hide_hamburger_css, unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
# Load NLEM 2022 drugs
with open("nlem_2022.json", "r") as f:
    nlem_drugs = json.load(f)

# Load filtered DDI interactions
with open("filtered_ddi.json", "r") as f:
    ddi_data = json.load(f)

# ------------------ SIDEBAR NAVIGATION ------------------
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "Calculator", "Drug Assistant", "Normal Values", "Indian Protocols"])



# ------------------ HOME PAGE ------------------
if app_mode == "Home":
    st.title("🏥 Welcome to the complete Medical Suite")
    st.markdown("""
    This app is designed for doctors, medical students, and healthcare professionals.  
                
    <span style="color:red; font-weight:bold;">USE THE SIDEBAR ( > icon at top left) TO NAVIGATE TO:</span>
    - **Calculator:** Access medical calculators by specialty.
    - **Drug Assistant:** Search drug interactions.
    - **Normal Values:** Essential normal values sorted by system.
    - **Indian Protocols:** Coming Soon.
    
    ---
    🔬 *All tools are built for educational and professional support only.*
        
        Designed by K.S.Srinath.
    """, unsafe_allow_html=True
    )
    st.markdown("""
    Want to know more about me? <a href="https://ksnath.com" target="_blank" rel="noopener noreferrer">Visit ksnath.com</a>
    """, unsafe_allow_html=True)


# ------------------ CALCULATORS ------------------
elif app_mode == "Calculator":
    st.title("📟 Medical Calculators")
    #sri
    # Define calculator categories
    calculators_by_category = {
    "General": ["BMI", "BSA", "Ideal Body Weight", "Body Fat %", "Creatinine Clearance", "MAP"],
    "Cardiology": ["CHA2DS2-VASc", "HAS-BLED", "Heart Rate", "Framingham Risk", "TIMI Risk", "GRACE Score", "eGFR"],
    "Pulmonology": ["Wells Score PE", "CURB-65", "PaO2/FiO2", "Predicted PFT"],
    "Nephrology": ["eGFR", "Creatinine Clearance", "Urine Output", "FeNa"],
    "Endocrinology": ["HbA1c to Avg Glucose", "HOMA-IR", "Total Daily Insulin Requirement", "Corrected Calcium", "Corrected Sodium", "Calcium-Phosphate Product", "FRAX", "Serum Osmolality", "Water Deficit", "Anion Gap"],
    "Mental Health": ["GAD-7", "PHQ-9", "MMSE"],
    "Hematology": ["INR", "NLR", "PLR", "APTT Ratio", "PT Ratio"],
    "Gastroenterology": ["Child-Pugh", "MELD", "APRI"],
    "Critical Care": ["SOFA", "APACHE II", "SIRS"],
    "Obstetrics": ["Gestational Age", "EDC Calculator", "EDC to GA", "Bishop Score", "BMI in Pregnancy"],
    "Surgery" : ["ABPI"]
}

    # Sidebar selection
    # --- Sidebar search bar ---
    search_query = st.sidebar.text_input("🔍 Search Calculator", "")

    if search_query:
        # Flatten all calculators into a single list
        all_calcs = [calc for sublist in calculators_by_category.values() for calc in sublist]
        matching_calcs = [calc for calc in all_calcs if search_query.lower() in calc.lower()]

        if matching_calcs:
            selected_calculator = st.sidebar.selectbox("Matching Calculators", matching_calcs)
        else:
            st.sidebar.info("No matching calculators found.")
            selected_calculator = None
    else:
        # Normal navigation if no search
        category = st.sidebar.selectbox("Category", ["All"] + list(calculators_by_category.keys()))
        if category == "All":
            all_calcs = [calc for sublist in calculators_by_category.values() for calc in sublist]
            selected_calculator = st.sidebar.selectbox("Select Calculator", all_calcs)
        else:
            selected_calculator = st.sidebar.selectbox("Select Calculator", calculators_by_category[category])


    # ------------------ CALCULATOR LOGIC ------------------
    # ---------- GENERAL ----------
    if selected_calculator == "BMI":
        # Inputs as text for empty fields
        weight_input = st.text_input("Weight (kg)", "")
        height_input = st.text_input("Height (cm)", "")

        if weight_input and height_input:
            try:
                weight = float(weight_input)
                height = float(height_input)
                bmi = weight / (height/100)**2
                
                # Show formula
                st.latex(r"\text{BMI} = \frac{\text{Weight (kg)}}{\text{Height (m)}^2}")
                
                # Show result
                st.success(f"BMI: {bmi:.2f} kg/m²")
                
                # Interpretation
                if bmi < 18.5:
                    st.info("Underweight")
                elif bmi < 25:
                    st.success("Normal weight")
                elif bmi < 30:
                    st.warning("Overweight")
                else:
                    st.error("Obese")
            except ValueError:
                st.error("Please enter valid numeric values!")

    elif selected_calculator == "BSA":
        weight_input = st.text_input("Weight (kg)", "", key="bsa_weight")
        height_input = st.text_input("Height (cm)", "", key="bsa_height")
        if weight_input and height_input:
            try:
                weight = float(weight_input)
                height = float(height_input)
                
                # Mosteller formula
                bsa = math.sqrt((height * weight)/3600)
                
                # Show formula
                st.latex(r"\text{BSA} = \sqrt{\dfrac{\text{Height (cm)} \times \text{Weight (kg)}}{3600}}")
                
                # Show result
                st.success(f"BSA: {bsa:.2f} m²")
                
                # Interpretation based on average adult values
                if bsa < 1.0:
                    st.info("BSA is low (typical for children).")
                elif 1.0 <= bsa < 1.6:
                    st.info("BSA is within the expected range for adolescents or small adults.")
                elif 1.6 <= bsa < 2.2:
                    st.success("BSA is within the normal adult range.")
                else:
                    st.warning("BSA is higher than typical adult average (may be due to larger body size).")
            except ValueError:
                st.error("Please enter valid numeric values!")
    # elif selected_calculator == "BSA":
    #     weight = st.number_input("Weight (kg)", min_value=0.0, key="bsa_w")
    #     height = st.number_input("Height (cm)", min_value=0.0, key="bsa_h")
    #     if weight > 0 and height > 0:
    #         bsa = math.sqrt((height * weight)/3600)  # Mosteller formula
    #         st.success(f"BSA: {bsa:.2f} m²")

    #         #Interpretation 
    #         if bsa < 1.0:
    #             st.info("BSA is low (typical for children).")
    #         elif 1.0 <= bsa < 1.6:
    #             st.info("BSA is within the expected range for adolescents or small adults.")
    #         elif 1.6 <= bsa < 2.2:
    #             st.success("BSA is within the normal adult range.")
    #         else:
    #             st.warning("BSA is higher than typical adult average (may be due to larger body size).")

    #         #Show BSA formula in LaTeX
    #         st.latex(r"\text{BSA} = \sqrt{\dfrac{\text{Height (cm)} \times \text{Weight (kg)}}{3600}}")


    elif selected_calculator == "Ideal Body Weight":
        height = st.number_input("Height (cm)", min_value=0.0, key="ibw_h")
        gender = st.selectbox("Gender", ["Male", "Female"])
        if height > 0:
            if gender=="Male":
                ibw = 50 + 0.9 * (height-152)
            else:
                ibw = 45.5 + 0.9 * (height-152)
            st.success(f"Ideal Body Weight: {ibw:.2f} kg")

    elif selected_calculator == "Body Fat %":
        # Simple US Navy formula example
        gender = st.selectbox("Gender", ["Male", "Female"], key="bf_gender")
        waist = st.number_input("Waist circumference (cm)", min_value=0.0)
        neck = st.number_input("Neck circumference (cm)", min_value=0.0)
        height = st.number_input("Height (cm)", min_value=0.0, key="bf_h")
        if gender=="Male" and waist>0 and neck>0 and height>0:
            bf = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
            st.success(f"Body Fat %: {bf:.2f}%")
        elif gender=="Female":
            hip = st.number_input("Hip circumference (cm)", min_value=0.0)
            if waist>0 and neck>0 and hip>0 and height>0:
                bf = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387
                st.success(f"Body Fat %: {bf:.2f}%")

    elif selected_calculator == "Creatinine Clearance":
        age = st.number_input("Age (years)", min_value=0)
        weight = st.number_input("Weight (kg)", min_value=0.0, key="crcl_w")
        serum_cr = st.number_input("Serum Creatinine (mg/dL)", min_value=0.0)
        gender = st.selectbox("Gender", ["Male", "Female"], key="crcl_gender")
        if age>0 and weight>0 and serum_cr>0:
            crcl = ((140-age)*weight)/(72*serum_cr)
            if gender=="Female": crcl *= 0.85
            st.success(f"Creatinine Clearance: {crcl:.2f} mL/min")

    elif selected_calculator == "MAP":
        sbp = st.number_input("Systolic BP (mmHg)", min_value=0.0)
        dbp = st.number_input("Diastolic BP (mmHg)", min_value=0.0)
        if sbp>0 and dbp>0:
            map_val = (2*dbp + sbp)/3
            st.success(f"Mean Arterial Pressure (MAP): {map_val:.2f} mmHg")

    # ---------- Cardiology ----------
    elif selected_calculator == "CHA2DS2-VASc":
        # Inputs
        age = st.number_input("Age", min_value=0)
        hf = st.checkbox("Heart Failure")
        htn = st.checkbox("Hypertension")
        stroke = st.checkbox("Prior Stroke/TIA")
        vascular = st.checkbox("Vascular disease")
        female = st.checkbox("Female sex")
        diabetes = st.checkbox("Diabetes")
        # Score calculation
        score = 0
        score += 2 if age>=75 else 1 if age>=65 else 0
        score += 1 if hf else 0
        score += 1 if htn else 0
        score += 2 if stroke else 0
        score += 1 if vascular else 0
        score += 1 if diabetes else 0
        score += 1 if female else 0
        st.success(f"CHA2DS2-VASc Score: {score}")

    elif selected_calculator == "HAS-BLED":
        # Inputs
        htn = st.checkbox("Hypertension")
        abn_renal = st.checkbox("Abnormal renal/liver function")
        stroke = st.checkbox("Stroke")
        bleeding = st.checkbox("Bleeding history")
        labile_inr = st.checkbox("Labile INR")
        elderly = st.checkbox("Age >65")
        drugs_alcohol = st.checkbox("Drugs/alcohol use")
        # Score
        score = sum([htn, abn_renal, stroke, bleeding, labile_inr, elderly, drugs_alcohol])
        st.success(f"HAS-BLED Score: {score}")

    elif selected_calculator == "Heart Rate":
        # Resting and target HR example
        max_hr = st.number_input("Maximum HR (bpm)", min_value=0)
        resting_hr = st.number_input("Resting HR (bpm)", min_value=0)
        if max_hr>0 and resting_hr>0:
            target_hr = 0.7*(max_hr-resting_hr)+resting_hr
            st.success(f"Target HR (70% intensity): {target_hr:.0f} bpm")
    
    elif selected_calculator == "Framingham Risk":
        st.subheader("Framingham 10-year Cardiovascular Risk Score (Simplified)")

        age = st.text_input("Age (years)", "")
        total_chol = st.text_input("Total Cholesterol (mg/dL)", "")
        hdl = st.text_input("HDL Cholesterol (mg/dL)", "")
        sbp = st.text_input("Systolic BP (mmHg)", "")
        smoker = st.selectbox("Smoker?", ["No", "Yes"])
        diabetic = st.selectbox("Diabetic?", ["No", "Yes"])

        if age and total_chol and hdl and sbp:
            try:
                age = float(age)
                total_chol = float(total_chol)
                hdl = float(hdl)
                sbp = float(sbp)

                # Simplified risk factor points
                risk = 0
                if age >= 50: risk += 2
                if total_chol > 200: risk += 2
                if hdl < 40: risk += 2
                if sbp > 140: risk += 2
                if smoker == "Yes": risk += 2
                if diabetic == "Yes": risk += 2

                # Risk % estimation (very simplified, for demo)
                risk_percent = min(30, risk * 2.5)

                st.latex(r"\text{Risk} = \text{Sum of Risk Factors} \times 2.5\%")
                st.success(f"Estimated 10-year CHD Risk: {risk_percent:.1f}%")

                if risk_percent < 10:
                    st.info("Low Risk (<10%)")
                elif risk_percent < 20:
                    st.warning("Moderate Risk (10–20%)")
                else:
                    st.error("High Risk (>20%)")

            except ValueError:
                st.error("Please enter valid numeric values!")

    elif selected_calculator == "TIMI Risk":
        st.subheader("TIMI Risk Score for Unstable Angina / NSTEMI")

        age65 = st.checkbox("Age ≥ 65 years")
        risk_factors = st.number_input("≥3 Risk Factors for CAD", 0, 5, 0)
        known_cad = st.checkbox("Known CAD (stenosis ≥50%)")
        aspirin = st.checkbox("Aspirin use in past 7 days")
        recent_angina = st.checkbox("≥2 Angina episodes in last 24h")
        st_deviation = st.checkbox("ST deviation ≥0.5 mm")
        elevated_markers = st.checkbox("Elevated cardiac markers")

        score = 0
        if age65: score += 1
        if risk_factors >= 3: score += 1
        if known_cad: score += 1
        if aspirin: score += 1
        if recent_angina: score += 1
        if st_deviation: score += 1
        if elevated_markers: score += 1

        st.latex(r"\text{TIMI Score} = \text{Sum of Positive Predictors}")
        st.success(f"TIMI Score: {score}/7")

        if score <= 2:
            st.info("Low Risk (≤8% event rate)")
        elif score <= 4:
            st.warning("Intermediate Risk (~19%)")
        else:
            st.error("High Risk (~41%)")
    
    elif selected_calculator == "GRACE Score":
        st.subheader("Simplified GRACE Risk Score (ACS)")

        age = st.text_input("Age (years)", "")
        heart_rate = st.text_input("Heart Rate (bpm)", "")
        sbp = st.text_input("Systolic BP (mmHg)", "")
        creat = st.text_input("Serum Creatinine (mg/dL)", "")

        if age and heart_rate and sbp and creat:
            try:
                age = float(age)
                heart_rate = float(heart_rate)
                sbp = float(sbp)
                creat = float(creat)

                # simplified linear approximation
                grace = (0.04 * age) + (0.03 * heart_rate) - (0.05 * sbp) + (1.2 * creat)
                grace_score = round(grace * 10, 1)

                st.latex(r"\text{GRACE} = 0.04A + 0.03HR - 0.05SBP + 1.2Cr")
                st.success(f"GRACE (simplified): {grace_score:.1f}")

                if grace_score < 100:
                    st.info("Low risk")
                elif grace_score < 150:
                    st.warning("Moderate risk")
                else:
                    st.error("High risk")

            except ValueError:
                st.error("Please enter valid numeric values!")

    elif selected_calculator == "eGFR":
        st.subheader("Estimated Glomerular Filtration Rate (eGFR) — CKD-EPI")

        creat = st.text_input("Serum Creatinine (mg/dL)", "")
        age = st.text_input("Age (years)", "")
        sex = st.selectbox("Sex", ["Male", "Female"])

        if creat and age:
            try:
                creat = float(creat)
                age = float(age)

                if sex == "Female":
                    k, a = 0.7, -0.329
                    sex_factor = 1.018
                else:
                    k, a = 0.9, -0.411
                    sex_factor = 1.0

                egfr = 141 * min(creat / k, 1) ** a * max(creat / k, 1) ** -1.209 * (0.993 ** age) * sex_factor
                st.latex(r"\text{eGFR} = 141 \times \min\left(\frac{Scr}{k},1\right)^a \times \max\left(\frac{Scr}{k},1\right)^{-1.209} \times 0.993^{Age} \times S")
                st.success(f"eGFR: {egfr:.1f} mL/min/1.73m²")

                if egfr >= 90:
                    st.info("Normal or high (G1)")
                elif egfr >= 60:
                    st.success("Mildly decreased (G2)")
                elif egfr >= 45:
                    st.warning("Mild–moderate decrease (G3a)")
                elif egfr >= 30:
                    st.warning("Moderate–severe decrease (G3b)")
                elif egfr >= 15:
                    st.error("Severe decrease (G4)")
                else:
                    st.error("Kidney failure (G5)")

            except ValueError:
                st.error("Please enter valid numeric values!")

    # ---------- Mental Health ----------
    elif selected_calculator == "GAD-7":
        questions = [
            "Feeling nervous, anxious, or on edge",
            "Not being able to stop worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Restless that it is hard to sit still",
            "Becoming easily annoyed",
            "Feeling afraid something awful might happen"
        ]
        options = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]
        scores = [options.index(st.selectbox(q, options, key=q)) for q in questions]
        total = sum(scores)
        st.success(f"GAD-7 Score: {total}")

    elif selected_calculator == "PHQ-9":
        questions = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble sleeping or sleeping too much",
            "Feeling tired",
            "Poor appetite or overeating",
            "Feeling bad about yourself",
            "Trouble concentrating",
            "Moving slowly or fidgety",
            "Thoughts of self-harm"
        ]
        options = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]
        scores = [options.index(st.selectbox(q, options, key="phq"+q)) for q in questions]
        total = sum(scores)
        st.success(f"PHQ-9 Score: {total}")

    elif selected_calculator == "MMSE":
        st.subheader("Mini-Mental State Examination (MMSE)")

        st.markdown("""
        **Purpose:** Screening tool to assess cognitive function.  
        **Maximum score:** 30 points.  
        """)
        
        st.info("Enter the patient's score for each domain below:")

        orientation = st.number_input("Orientation (0–10)", min_value=0, max_value=10, step=1)
        registration = st.number_input("Registration (0–3)", min_value=0, max_value=3, step=1)
        attention = st.number_input("Attention & Calculation (0–5)", min_value=0, max_value=5, step=1)
        recall = st.number_input("Recall (0–3)", min_value=0, max_value=3, step=1)
        language = st.number_input("Language (0–9)", min_value=0, max_value=9, step=1)

        if st.button("Calculate MMSE"):
            total = orientation + registration + attention + recall + language
            
            st.latex(r"\text{MMSE Total} = \text{Orientation} + \text{Registration} + \text{Attention} + \text{Recall} + \text{Language}")
            st.success(f"Total MMSE Score: {total}/30")

            if total >= 25:
                st.info("Normal cognition (25–30)")
            elif total >= 21:
                st.warning("Mild cognitive impairment (21–24)")
            elif total >= 10:
                st.error("Moderate cognitive impairment (10–20)")
            else:
                st.error("Severe cognitive impairment (<10)")

            st.caption("Interpretation may vary slightly depending on age and education level.")


    # ---------- PULMONOLOGY ----------
    elif selected_calculator == "Wells Score PE":
        criteria = {
            "Clinical signs of DVT": 3,
            "PE is #1 diagnosis or equally likely": 3,
            "Heart rate >100 bpm": 1.5,
            "Immobilization ≥3 days / surgery in last 4 weeks": 1.5,
            "Previous DVT/PE": 1.5,
            "Hemoptysis": 1,
            "Malignancy": 1
        }
        score = sum([st.checkbox(k) * v for k, v in criteria.items()])
        st.success(f"Wells Score for PE: {score}")
        if score > 6: st.error("High probability")
        elif score >= 2: st.warning("Moderate probability")
        else: st.info("Low probability")

    elif selected_calculator == "CURB-65":
        age = st.number_input("Age ≥65?", min_value=0)
        confusion = st.checkbox("Confusion")
        bun = st.number_input("BUN > 19 mg/dL?", min_value=0)
        rr = st.number_input("Respiratory rate ≥30?", min_value=0)
        sbp = st.number_input("SBP <90 or DBP ≤60?", min_value=0)
        score = sum([age>=65, confusion, bun>19, rr>=30, sbp>0])
        st.success(f"CURB-65 Score: {score}")

    elif selected_calculator == "PaO2/FiO2":
        pao2 = st.number_input("PaO2 (mmHg)", min_value=0.0)
        fio2 = st.number_input("FiO2 (%)", min_value=0.0)
        if pao2>0 and fio2>0:
            ratio = pao2 / (fio2/100)
            st.success(f"PaO2/FiO2 Ratio: {ratio:.0f}")
            if ratio < 100: st.error("Severe ARDS")
            elif ratio < 200: st.warning("Moderate ARDS")
            else: st.info("Mild / Normal")

    elif selected_calculator == "Predicted PFT":
        st.subheader("Predicted Pulmonary Function Test Values (FEV₁, FVC)")

        age = st.text_input("Age (years)", "")
        height = st.text_input("Height (cm)", "")
        sex = st.selectbox("Sex", ["Male", "Female"])

        if age and height:
            try:
                age = float(age)
                height = float(height)

                if sex == "Male":
                    fev1 = (0.0414 * height) - (0.0244 * age) - 2.19
                    fvc = (0.0523 * height) - (0.0281 * age) - 3.59
                else:
                    fev1 = (0.0342 * height) - (0.0255 * age) - 1.578
                    fvc = (0.041 * height) - (0.0244 * age) - 2.190

                ratio = (fev1 / fvc) * 100
                st.latex(r"\text{FEV₁/FVC Ratio} = \frac{\text{FEV₁}}{\text{FVC}} \times 100")
                st.success(f"Predicted FEV₁: {fev1:.2f} L")
                st.success(f"Predicted FVC: {fvc:.2f} L")
                st.info(f"Predicted FEV₁/FVC Ratio: {ratio:.1f}%")

            except ValueError:
                st.error("Please enter valid numeric values!")

    # ---------- NEPHROLOGY ----------
    elif selected_calculator == "FeNa":
        na_serum = st.number_input("Serum Na (mmol/L)", min_value=0.0)
        na_urine = st.number_input("Urine Na (mmol/L)", min_value=0.0)
        cr_serum = st.number_input("Serum Creatinine (mg/dL)", min_value=0.0)
        cr_urine = st.number_input("Urine Creatinine (mg/dL)", min_value=0.0)
        if all([na_serum, na_urine, cr_serum, cr_urine]):
            fena = (na_urine * cr_serum)/(na_serum * cr_urine) * 100
            st.success(f"FeNa: {fena:.2f}%")

    elif selected_calculator == "Urine Output":
        weight = st.number_input("Weight (kg)", min_value=0.0)
        urine = st.number_input("Urine output (mL)", min_value=0.0)
        hours = st.number_input("Time (hours)", min_value=0.0)
        if weight>0 and urine>0 and hours>0:
            uo_rate = urine / weight / hours * 60  # mL/kg/hr
            st.success(f"Urine Output Rate: {uo_rate:.2f} mL/kg/hr")

    # ---------- ENDOCRINOLOGY ----------
    elif selected_calculator == "HbA1c to Avg Glucose":
        hba1c = st.text_input("HbA1c (%)")
        try:
            hba1c = float(hba1c)
            eag = 28.7 * hba1c - 46.7
            st.latex(r"eAG (mg/dL) = (28.7 \times HbA1c) - 46.7")
            st.write(f"**Estimated Average Glucose = {eag:.0f} mg/dL**")
        except:
            st.warning("Enter a valid number.")

    elif selected_calculator == "HOMA-IR":
        insulin = st.text_input("Fasting Insulin (µU/mL)")
        glucose = st.text_input("Fasting Glucose (mg/dL)")
        try:
            insulin = float(insulin)
            glucose = float(glucose)
            homa_ir = (insulin * glucose)/405
            st.latex(r"HOMA-IR = \frac{Fasting\ Insulin (\mu U/mL) \times Fasting\ Glucose (mg/dL)}{405}")
            st.write(f"**HOMA-IR = {homa_ir:.2f}**")
            if homa_ir > 2.5:
                st.warning("Suggestive of insulin resistance")
        except:
            st.warning("Enter valid numeric values.")

    elif selected_calculator == "Total Daily Insulin Requirement":
        weight = st.text_input("Weight (kg)")
        try:
            weight = float(weight)
            tdi = weight * 0.5
            st.latex(r"TDI = 0.5 \times Weight (kg)")
            st.write(f"**Approx. Total Daily Insulin = {tdi:.1f} units/day**")
            st.caption("50% basal, 50% bolus (approx.)")
        except:
            st.warning("Enter valid numeric value.")

    elif selected_calculator == "Corrected Calcium":
        calcium = st.text_input("Measured Calcium (mg/dL)")
        albumin = st.text_input("Albumin (g/dL)")
        try:
            calcium = float(calcium)
            albumin = float(albumin)
            corr_ca = calcium + 0.8*(4 - albumin)
            st.latex(r"Corrected\ Ca = Measured\ Ca + 0.8 \times (4 - Albumin)")
            st.write(f"**Corrected Calcium = {corr_ca:.2f} mg/dL**")
        except:
            st.warning("Enter valid numeric values.")
    
    elif selected_calculator == "Corrected Sodium":
        sodium = st.text_input("Measured Sodium (mEq/L)")
        glucose = st.text_input("Glucose (mg/dL)")
        try:
            sodium = float(sodium)
            glucose = float(glucose)
            corr_na = sodium + 1.6*((glucose-100)/100)
            st.latex(r"Corrected\ Na^+ = Measured\ Na^+ + 1.6 \times \frac{(Glucose-100)}{100}")
            st.write(f"**Corrected Sodium = {corr_na:.1f} mEq/L**")
        except:
            st.warning("Enter valid numeric values.")

    # --- Calcium-Phosphate Product ---
    elif selected_calculator == "Calcium-Phosphate Product":
        calcium = st.text_input("Calcium (mg/dL)")
        phosphate = st.text_input("Phosphate (mg/dL)")
        try:
            calcium = float(calcium)
            phosphate = float(phosphate)
            product = calcium * phosphate
            st.latex(r"Ca \times P = Serum\ Calcium \times Serum\ Phosphate")
            st.write(f"**Ca × P = {product:.1f}**")
            if product > 55:
                st.warning("High risk of vascular calcification (esp. in CKD)")
        except:
            st.warning("Enter valid numeric values.")
    
    # --- FRAX (simplified) ---
    elif selected_calculator == "FRAX":
        age = st.text_input("Age (years)")
        t_score = st.text_input("T-score")
        try:
            age = int(age)
            t_score = float(t_score)
            st.caption("Full FRAX requires age, sex, BMI, BMD & risk factors.")
            st.latex(r"FRAX = Risk\ Algorithm\ (Age, Sex, BMD, Clinical\ factors)")
            if age > 65 or t_score < -2.5:
                st.warning("High fracture risk")
            else:
                st.success("Lower fracture risk")
        except:
            st.warning("Enter valid numeric values.")
    
    
    # --- Serum Osmolality ---
    elif selected_calculator == "Serum Osmolality":
        sodium = st.text_input("Sodium (mEq/L)")
        glucose = st.text_input("Glucose (mg/dL)")
        bun = st.text_input("BUN (mg/dL)")
        try:
            sodium = float(sodium)
            glucose = float(glucose)
            bun = float(bun)
            osmo = 2*sodium + glucose/18 + bun/2.8
            st.latex(r"Serum\ Osmolality = 2 \times Na^+ + \frac{Glucose}{18} + \frac{BUN}{2.8}")
            st.write(f"**Serum Osmolality = {osmo:.1f} mOsm/kg**")
        except:
            st.warning("Enter valid numeric values.")

    # --- Water Deficit ---
    elif selected_calculator == "Water Deficit":
        weight = st.text_input("Weight (kg)")
        sodium = st.text_input("Serum Sodium (mEq/L)")
        sex = st.radio("Sex", ["Male", "Female"])
        try:
            weight = float(weight)
            sodium = float(sodium)
            tbw = 0.6*weight if sex=="Male" else 0.5*weight
            deficit = tbw*((sodium/140)-1)
            st.latex(r"Water\ Deficit = TBW \times \left(\frac{Na}{140} - 1\right)")
            st.write(f"**Water Deficit = {deficit:.1f} L**")
        except:
            st.warning("Enter valid numeric values.")

    elif selected_calculator == "Anion Gap":
        sodium = st.text_input("Sodium (mEq/L)")
        chloride = st.text_input("Chloride (mEq/L)")
        bicarbonate = st.text_input("Bicarbonate (HCO3-) (mEq/L)")
        try:
            sodium = float(sodium)
            chloride = float(chloride)
            bicarbonate = float(bicarbonate)
            anion_gap = sodium - (chloride + bicarbonate)
            st.latex(r"Anion\ Gap = Na^+ - (Cl^- + HCO_3^-)")
            st.write(f"**Anion Gap = {anion_gap:.1f} mEq/L**")
            if anion_gap < 8:
                st.info("Low Anion Gap (consider hypoalbuminemia or lab error)")
            elif 8 <= anion_gap <= 12:
                st.success("Normal Anion Gap")
            else:
                st.warning("High Anion Gap (consider metabolic acidosis, toxins, renal failure)")
        except:
            st.warning("Enter valid numeric values for Na⁺, Cl⁻, and HCO₃⁻.")


    # ---------- HEMATOLOGY ----------
    elif selected_calculator == "NLR":
        neutrophils = st.number_input("Neutrophils (cells/μL)", min_value=0.0)
        lymphocytes = st.number_input("Lymphocytes (cells/μL)", min_value=0.0)
        if neutrophils>0 and lymphocytes>0:
            nlr = neutrophils/lymphocytes
            st.success(f"NLR: {nlr:.2f}")

    elif selected_calculator == "PLR":
        platelets = st.number_input("Platelets (cells/μL)", min_value=0.0)
        lymphocytes = st.number_input("Lymphocytes (cells/μL)", min_value=0.0, key="plr")
        if platelets>0 and lymphocytes>0:
            plr = platelets/lymphocytes
            st.success(f"PLR: {plr:.2f}")

    elif selected_calculator == "INR":
            st.subheader("International Normalized Ratio (INR)")

            st.markdown("""
            **Purpose:** Standardizes Prothrombin Time (PT) to monitor warfarin therapy or liver function.
            """)

            # Proper LaTeX display
            st.latex(r"\text{INR} = \left( \frac{\text{Patient PT}}{\text{Control PT}} \right)^{\text{ISI}}")

            patient_pt = st.text_input("Patient PT (seconds)", "")
            control_pt = st.text_input("Control PT (seconds)", "")
            isi = st.text_input("ISI (International Sensitivity Index)", "1.0")

            if patient_pt and control_pt and isi:
                try:
                    patient_pt = float(patient_pt)
                    control_pt = float(control_pt)
                    isi = float(isi)

                    if control_pt <= 0:
                        st.error("Control PT must be greater than 0!")
                    else:
                        inr = (patient_pt / control_pt) ** isi
                        st.success(f"Calculated INR: {inr:.2f}")

                        # Interpretation
                        if inr < 0.8:
                            st.warning("Below normal range — may indicate increased clotting tendency.")
                        elif 0.8 <= inr <= 1.2:
                            st.info("Normal range (not on anticoagulation).")
                        elif 2.0 <= inr <= 3.0:
                            st.success("Therapeutic range for most indications (on warfarin).")
                        elif 2.5 <= inr <= 3.5:
                            st.success("Therapeutic range for mechanical valves or high-risk conditions.")
                        elif inr > 4.0:
                            st.error("High bleeding risk — consider dose adjustment or evaluation.")
                        else:
                            st.warning("Sub-therapeutic INR for anticoagulation.")

                except ValueError:
                    st.error("Please enter valid numeric values!")


    elif selected_calculator == "APTT Ratio":
        st.subheader("APTT (Activated Partial Thromboplastin Time) Calculator")

        st.latex(r"""
        \text{APTT Ratio} = 
        \frac{\text{Patient APTT}}{\text{Control APTT}}
        """)

        patient_aptt = st.number_input("Patient APTT (seconds)", min_value=0.0, step=0.1)
        control_aptt = st.number_input("Control APTT (seconds)", min_value=0.0, step=0.1)

        if control_aptt > 0:
            aptt_ratio = patient_aptt / control_aptt
            st.markdown(f"### 🧪 APTT Ratio = {aptt_ratio:.2f}")
        else:
            st.warning("Enter a valid Control APTT.")

        st.info("""
        **Interpretation:**
        - **Normal APTT Ratio:** 0.8 – 1.2  
        - **Prolonged (>1.5):** May indicate  
        - Heparin therapy  
        - Coagulation factor deficiency  
        - Liver disease  
        - DIC (Disseminated Intravascular Coagulation)
        """)


    elif selected_calculator == "PT Ratio":
        st.subheader("PT (Prothrombin Time) Calculator")

        st.latex(r"""
        \text{INR} = 
        \left( 
            \frac{\text{Patient PT}}{\text{Control PT}} 
        \right)^{\text{ISI}}
        """)

        patient_pt = st.number_input("Patient PT (seconds)", min_value=0.0, step=0.1)
        control_pt = st.number_input("Control PT (seconds)", min_value=0.0, step=0.1)
        isi = st.number_input("ISI (International Sensitivity Index)", min_value=0.0, step=0.1)

        if control_pt > 0:
            inr = (patient_pt / control_pt) ** isi
            st.markdown(f"### 🧬 INR = {inr:.2f}")
        else:
            st.warning("Enter a valid Control PT.")

        st.info("""
        **Interpretation:**
        - **Normal INR:** 0.8 – 1.2  
        - **Therapeutic (Warfarin):** 2.0 – 3.0  
        - **High INR →** Increased bleeding risk  
        - **Low INR →** Thrombosis risk  
        """)


    # ---------- GASTROENTEROLOGY ----------
    elif selected_calculator == "Child-Pugh":
        bilirubin = st.number_input("Bilirubin (mg/dL)", min_value=0.0)
        albumin = st.number_input("Albumin (g/dL)", min_value=0.0)
        inr = st.number_input("INR", min_value=0.0)
        ascites = st.selectbox("Ascites", ["None","Mild","Moderate-Severe"])
        encephalopathy = st.selectbox("Encephalopathy", ["None","Grade 1-2","Grade 3-4"])
        # Assign points
        score = 0
        score += 1 if bilirubin<2 else 2 if bilirubin<=3 else 3
        score += 1 if albumin>3.5 else 2 if albumin>=2.8 else 3
        score += 1 if inr<1.7 else 2 if inr<=2.3 else 3
        score += 1 if ascites=="None" else 2 if ascites=="Mild" else 3
        score += 1 if encephalopathy=="None" else 2 if encephalopathy=="Grade 1-2" else 3
        st.success(f"Child-Pugh Score: {score}")

    elif selected_calculator == "MELD":
        bilirubin = st.number_input("Bilirubin (mg/dL)", min_value=0.0, key="meld_bil")
        inr = st.number_input("INR", min_value=0.0, key="meld_inr")
        creatinine = st.number_input("Creatinine (mg/dL)", min_value=0.0, key="meld_cr")
        if bilirubin>0 and inr>0 and creatinine>0:
            meld = 3.78*math.log(bilirubin) + 11.2*math.log(inr) + 9.57*math.log(creatinine) + 6.43
            st.success(f"MELD Score: {meld:.0f}")

    # ---------- CRITICAL CARE ----------
    elif selected_calculator == "SOFA":
        st.info("Coming soon.")
        st.info("SOFA Score requires multiple organ parameters. Add inputs for PaO2/FiO2, Platelets, Bilirubin, MAP, GCS, Creatinine.")
        st.info("You can calculate total score by assigning 0-4 points per organ system.")

    elif selected_calculator == "APACHE II":
        st.info("Coming soon.")
        st.info("APACHE II requires age, vitals, lab values, and chronic health status.")
        st.info("You can sum points to get the APACHE II score.")

    elif selected_calculator == "SIRS":
        temp = st.number_input("Temperature (°C)", min_value=0.0)
        hr = st.number_input("Heart rate (bpm)", min_value=0)
        rr = st.number_input("Respiratory rate (/min)", min_value=0)
        wbc = st.number_input("WBC count (x10⁹/L)", min_value=0.0)
        criteria = 0
        criteria += 1 if temp<36 or temp>38 else 0
        criteria += 1 if hr>90 else 0
        criteria += 1 if rr>20 else 0
        criteria += 1 if wbc<4 or wbc>12 else 0
        st.success(f"SIRS Criteria Met: {criteria} (≥2 indicates SIRS)")

    # ---------- OBSTETRICS ----------
    elif selected_calculator == "Gestational Age":
        lmp = st.date_input("Last Menstrual Period (LMP)")
        from datetime import date, timedelta
        today = date.today()
        ga_days = (today - lmp).days
        weeks = ga_days // 7
        days = ga_days % 7
        st.success(f"Estimated Gestational Age: {weeks} weeks and {days} days")

    elif selected_calculator == "EDC Calculator":
        def days_to_weeks_days(days):
            weeks = days // 7
            days_rem = days % 7
            return weeks, days_rem

        def format_weeks_days(days):
            w, d = days_to_weeks_days(days)
            return f"{w} week{'s' if w != 1 else ''} {d} day{'s' if d != 1 else ''}"

        st.title("⚕️ EDC / EDD Calculator")
        st.caption("Estimate date of delivery and current gestational age. (Designed for clinical use — always confirm clinically.)")

        st.markdown("---")
        method = st.radio("Choose calculation method:", ["Last Menstrual Period (LMP) — Naegele's rule", 
                                                        "Conception date (if known)", 
                                                        "Ultrasound (CRL / Gestational Age)"])

        today = date.today()

        # Common inputs
        if method == "Last Menstrual Period (LMP) — Naegele's rule":
            st.write("**Using LMP + cycle length adjustment**")
            lmp = st.date_input("Date of Last Menstrual Period (LMP)", value=today - timedelta(weeks=12))
            cycle_len = st.number_input("Average menstrual cycle length (days)", min_value=21, max_value=45, value=28, step=1,
                                        help="If not 28, EDD is adjusted by (cycle_len - 28) days.")
            # Calculation: Naegele's rule baseline is LMP + 280 days (40 weeks). Adjust for cycle length.
            edd = lmp + timedelta(days=280 + (cycle_len - 28))
            # gestational age from LMP to today
            gest_days = (today - lmp).days
            gest_days = max(0, gest_days)
            gest_weeks_days = format_weeks_days(gest_days)
            st.markdown("### Result")
            st.success(f"Estimated Date of Delivery (EDD): **{edd.strftime('%d-%b-%Y')}**")
            st.info(f"Current gestational age (from LMP): **{gest_weeks_days}** ({gest_days} days)")
            st.markdown("**Explanation:** Naegele's rule: LMP + 280 days (40 weeks). Adjust by (cycle_len - 28) days if cycle differs from 28 days.")

        elif method == "Conception date (if known)":
            st.write("**Using conception date**")
            conc = st.date_input("Conception date", value=today - timedelta(weeks=10))
            # Typical interval conception -> EDD is ~266 days (38 weeks from conception)
            edd = conc + timedelta(days=266)
            gest_days = (today - conc).days + 14  # convention: gestational age counts from LMP ~2 weeks before conception
            # ensure non-negative
            if gest_days < 0:
                gest_days = 0
            gest_weeks_days = format_weeks_days(gest_days)
            st.markdown("### Result")
            st.success(f"Estimated Date of Delivery (EDD): **{edd.strftime('%d-%b-%Y')}**")
            st.info(f"Current gestational age (approx): **{gest_weeks_days}** ({gest_days} days)")
            st.markdown("**Explanation:** When conception date is known, EDD ≈ conception + 266 days (~38 weeks). Gestational age is conventionally ~2 weeks more than time since conception (i.e., from LMP).")

        else:  # Ultrasound method
            st.write("**Using an ultrasound estimate**")
            us_date = st.date_input("Ultrasound date", value=today - timedelta(weeks=12))
            ga_weeks = st.number_input("Gestational age on ultrasound — weeks", min_value=0, max_value=45, value=12, step=1)
            ga_days = st.number_input("Gestational age on ultrasound — extra days", min_value=0, max_value=6, value=0, step=1)
            # total gestational days at time of ultrasound
            ga_at_us_days = ga_weeks * 7 + ga_days
            # EDD = ultrasound_date + (280 - ga_at_us_days) days
            edd = us_date + timedelta(days=(280 - ga_at_us_days))
            # current GA = ga_at_us + (today - us_date)
            ga_today_days = ga_at_us_days + (today - us_date).days
            if ga_today_days < 0:
                ga_today_days = 0
            ga_today = format_weeks_days(ga_today_days)
            st.markdown("### Result")
            st.success(f"Estimated Date of Delivery (EDD): **{edd.strftime('%d-%b-%Y')}**")
            st.info(f"Gestational age today (based on ultrasound): **{ga_today}** ({ga_today_days} days)")
            st.markdown("**Explanation:** Ultrasound-based dating uses the GA measured on scan. EDD = scan date + (280 days − GA at scan). Ultrasound dating is preferred in the first trimester for accuracy.")

        st.markdown("---")
        # Additional helpful info block
        st.markdown("### Quick references")
        st.write(
            "- Naegele's rule (LMP): **LMP + 280 days (40 weeks)**. Adjust for cycle length.\n"
            "- Conception method: **conception + 266 days (~38 weeks from conception)**.\n"
            "- Ultrasound: preferred when LMP unknown or cycles irregular, especially 1st trimester."
        )

        # Optional: copy results text for pasting / clinic notes
        st.markdown("### Copyable summary")
        if method == "Last Menstrual Period (LMP) — Naegele's rule":
            if lmp:
                summary = (f"Method: LMP\nLMP: {lmp.strftime('%d-%b-%Y')}\n"
                        f"Cycle length: {cycle_len} days\nEDD: {edd.strftime('%d-%b-%Y')}\n"
                        f"Gestational age today: {gest_weeks_days} ({gest_days} days)")
                st.code(summary)
        elif method == "Conception date (if known)":
            summary = (f"Method: Conception date\nConception: {conc.strftime('%d-%b-%Y')}\n"
                    f"EDD: {edd.strftime('%d-%b-%Y')}\nGestational age today (approx): {gest_weeks_days} ({gest_days} days)")
            st.code(summary)
        else:
            summary = (f"Method: Ultrasound\nScan date: {us_date.strftime('%d-%b-%Y')}\n"
                    f"GA at scan: {ga_weeks} weeks + {ga_days} days\nEDD: {edd.strftime('%d-%b-%Y')}\n"
                    f"GA today (based on scan): {ga_today} ({ga_today_days} days)")
            st.code(summary)

        st.markdown("---")
        st.caption("Note: This tool provides estimates. Always corroborate with clinical judgement and local guidelines.")

    elif selected_calculator == "EDC to GA":
        def days_to_weeks_days(days: int):
            weeks = days // 7
            days_rem = days % 7
            return weeks, days_rem

        def format_weeks_days(days: int):
            w, d = days_to_weeks_days(days)
            return f"{w} week{'s' if w != 1 else ''} {d} day{'s' if d != 1 else ''}"

        def trimester_from_ga_days(ga_days: int):
            # Using conventional cutoffs:
            # 1st trimester: <14 weeks (0 - 13+6)
            # 2nd trimester: 14 - 27+6 weeks
            # 3rd trimester: >=28 weeks
            weeks = ga_days / 7
            if weeks < 14:
                return "1st trimester"
            elif weeks < 28:
                return "2nd trimester"
            else:
                return "3rd trimester"

        st.title("⚕️ EDC → Gestational Age (GA) Calculator")
        st.caption("Enter the estimated date of delivery (EDC/EDD) to compute current gestational age and related info.")

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            edd = st.date_input("Estimated Date of Delivery (EDC / EDD)", value=date.today() + timedelta(weeks=20))
            ref_date = st.date_input("Reference date (for GA calculation)", value=date.today(), help="Defaults to today. Change to calculate GA on another date.")
        with col2:
            show_progress = st.checkbox("Show GA progress bar (toward 40 weeks)", value=True)
            show_conception = st.checkbox("Show estimated conception date", value=True)
            show_summary = st.checkbox("Show copyable summary", value=True)

        # Constants
        TOTAL_GA_DAYS = 280  # 40 weeks from LMP (Naegele)
        CONCEPTION_OFFSET_DAYS = 266  # approx. from conception to EDD

        # calculations
        days_until_edd = (edd - ref_date).days  # positive -> days remaining; negative -> overdue by abs(...)
        ga_days = TOTAL_GA_DAYS - days_until_edd
        # allow negative (if reference date well before conception) but clamp for display
        if ga_days < 0:
            ga_days_display = 0
        else:
            ga_days_display = ga_days

        ga_weeks_days_text = format_weeks_days(ga_days_display)
        trimester = trimester_from_ga_days(ga_days)
        conception_date = edd - timedelta(days=CONCEPTION_OFFSET_DAYS)

        # Display results
        st.markdown("### Result")
        if days_until_edd > 0:
            st.success(f"EDD: **{edd.strftime('%d-%b-%Y')}** — {days_until_edd} day(s) remaining")
        elif days_until_edd == 0:
            st.warning(f"EDD is today: **{edd.strftime('%d-%b-%Y')}**")
        else:
            st.error(f"EDD passed {abs(days_until_edd)} day(s) ago (Overdue). EDD: **{edd.strftime('%d-%b-%Y')}**")

        # Gestational age
        if ga_days < 0:
            st.info(f"Estimated GA on {ref_date.strftime('%d-%b-%Y')}: **< 0 days** (before pregnancy dating).")
        else:
            st.info(f"Estimated Gestational Age on {ref_date.strftime('%d-%b-%Y')}: **{ga_weeks_days_text}** ({ga_days} days)")

        # Trimester & conception
        st.write(f"**Trimester:** {trimester}")
        if show_conception:
            st.write(f"**Estimated conception date:** {conception_date.strftime('%d-%b-%Y')} (≈ EDD − 266 days)")

        # Progress bar (toward 280 days / 40 weeks)
        if show_progress:
            progress_pct = (ga_days / TOTAL_GA_DAYS) if TOTAL_GA_DAYS else 0
            # cap progress for UI (allow >100 to show overdue)
            display_pct = max(0.0, min(progress_pct, 1.0))
            st.write(f"**Progress toward 40 weeks:** {round(progress_pct*100, 1)}%")
            st.progress(display_pct)

        # Warnings
        if ga_days >= 294:  # >=42 weeks (294 days)
            st.warning("⚠️ Post-term (≥42 weeks). Consider clinical assessment.")
        if ga_days > 280 and ga_days < 294:
            st.info("Note: Term (>40 weeks) — monitor for labour and follow local guidelines.")

        st.markdown("---")

        # Copyable summary
        if show_summary:
            summary_lines = [
                f"Method: EDC → GA calculator",
                f"Reference date: {ref_date.strftime('%d-%b-%Y')}",
                f"EDC (EDD): {edd.strftime('%d-%b-%Y')}",
            ]
            if ga_days >= 0:
                summary_lines.append(f"Gestational age: {ga_weeks_days_text} ({ga_days} days)")
            else:
                summary_lines.append(f"Gestational age: <0 days (reference date before pregnancy dating)")
            summary_lines.append(f"Trimester: {trimester}")
            summary_lines.append(f"Estimated conception date: {conception_date.strftime('%d-%b-%Y')}")
            summary_lines.append(f"Days until EDD: {days_until_edd} (positive = remaining; negative = overdue)")

            summary_text = "\n".join(summary_lines)
            st.code(summary_text)

        st.markdown("---")
        st.caption("Estimates only — always confirm with clinical judgement and local guidance (ultrasound dating preferred for accuracy).")
            
    elif selected_calculator == "Bishop Score":
        dilation = st.number_input("Cervical dilation (cm)", min_value=0)
        effacement = st.number_input("Effacement (%)", min_value=0, max_value=100)
        station = st.number_input("Fetal station (-3 to +3)", min_value=-3, max_value=3)
        consistency = st.selectbox("Cervical consistency", ["Firm","Medium","Soft"])
        position = st.selectbox("Cervical position", ["Posterior","Mid","Anterior"])
        score = dilation + (effacement//10) + (station+3)  # Simple approximation
        score += 0 if consistency=="Firm" else 1 if consistency=="Medium" else 2
        score += 0 if position=="Posterior" else 1 if position=="Mid" else 2
        st.success(f"Bishop Score: {score}")

    elif selected_calculator == "BMI in Pregnancy":
        weight = st.number_input("Weight (kg)", min_value=0.0, key="preg_bmi_w")
        height = st.number_input("Height (cm)", min_value=0.0, key="preg_bmi_h")
        if weight>0 and height>0:
            bmi = weight / (height/100)**2
            st.success(f"BMI: {bmi:.2f}")
            if bmi<18.5: st.info("Underweight")
            elif bmi<25: st.success("Normal weight")
            elif bmi<30: st.warning("Overweight")
            else: st.error("Obese")

# ------- SURGERY --------- #
    elif selected_calculator == "ABPI":
        st.title("Ankle-Brachial Pressure Index (ABPI) Calculator")

        st.markdown("""
        The **ABPI** is calculated by dividing the **highest ankle systolic pressure** 
        by the **highest brachial systolic pressure**.  
        It helps in screening for **Peripheral Arterial Disease (PAD)**.
        """)

        # -----------------------------
        # Inputs
        # -----------------------------
        st.subheader("Enter Systolic Blood Pressures (mmHg)")

        col1, col2 = st.columns(2)

        with col1:
            brachial_right = st.number_input("Right Brachial Pressure", min_value=0.0, step=1.0)
            brachial_left = st.number_input("Left Brachial Pressure", min_value=0.0, step=1.0)

        with col2:
            ankle_right = st.number_input("Right Ankle Pressure", min_value=0.0, step=1.0)
            ankle_left = st.number_input("Left Ankle Pressure", min_value=0.0, step=1.0)

        # -----------------------------
        # Calculation
        # -----------------------------
        if st.button("Calculate ABPI"):
            highest_brachial = max(brachial_right, brachial_left)

            if highest_brachial == 0:
                st.error("⚠️ Brachial pressure cannot be 0.")
            else:
                abpi_right = ankle_right / highest_brachial if ankle_right > 0 else None
                abpi_left = ankle_left / highest_brachial if ankle_left > 0 else None

                st.subheader("📊 Results")

                # Bailey & Love Interpretation
                def interpret_abpi(value):
                    if value is None:
                        return "Not calculated", "#d3d3d3"
                    elif value > 1.3:
                        return "Arterial calcification / non-compressible vessels", "#ff8000"
                    elif 0.91 <= value <= 1.3:
                        return "Normal", "#4CAF50"
                    elif 0.80 <= value < 0.91:
                        return "Mild PAD", "#FFD700"
                    elif 0.50 <= value < 0.80:
                        return "Moderate PAD", "#FF4500"
                    else:  # < 0.50
                        return "Severe PAD", "#FF0000"

                # Helper to render card
                def result_card(side, value):
                    interpretation, color = interpret_abpi(value)
                    if value is not None:
                        st.markdown(
                            f"""
                            <div style="padding:15px; border-radius:10px; margin-bottom:15px;
                                        background-color:{color}; color:white; font-size:18px;">
                                <b>{side} ABPI:</b> {value:.2f} <br>
                                <b>Interpretation:</b> {interpretation}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                result_card("Right Leg", abpi_right)
                result_card("Left Leg", abpi_left)

        # -----------------------------
        # Reference Table (Bailey & Love)
        # -----------------------------
        st.subheader("📖 ABPI Reference Table ")

        st.markdown("""
        | **ABPI Value**     | **Interpretation**                                |
        |---------------------|--------------------------------------------------|
        | > 1.3              | Arterial calcification / non-compressible vessels |
        | 0.91 – 1.30        | Normal                                           |
        | 0.80 – 0.90        | Mild PAD                                         |
        | 0.50 – 0.79        | Moderate PAD                                     |
        | < 0.50             | Severe PAD                                       |
        """)

    # ---------- Add more calculators as needed following same pattern ----------
    else:
        st.info("This calculator will be added soon.")


# ------------------ DRUG ASSISTANT ------------------
# elif app_mode == "Drug Assistant":
#     st.title("💊 Drug Assistant")
#     st.subheader("Drug Interaction Checker")

#     selected_drugs = st.multiselect("Select patient drugs:", nlem_drugs)

#     if len(selected_drugs) > 1:
#         st.subheader("Interactions Found:")
#         found = False
#         for d1, d2 in combinations(selected_drugs, 2):
#             interaction = ddi_data.get(d1, {}).get(d2) or ddi_data.get(d2, {}).get(d1)
#             if interaction:
#                 severity = interaction["severity"]
#                 desc = interaction["description"]

#                 if severity.lower() == "high":
#                     st.error(f"⚠️ {d1} + {d2} → {severity}: {desc}")
#                 elif severity.lower() == "moderate":
#                     st.warning(f"⚠️ {d1} + {d2} → {severity}: {desc}")
#                 else:
#                     st.info(f"{d1} + {d2} → {severity}: {desc}")

#                 found = True
#         if not found:
#             st.success("✅ No major interactions found.")

elif app_mode == "Drug Assistant":
    import json
    from itertools import combinations

    # -----------------------------
    # Load JSON
    # -----------------------------
    with open("filtered_ddi.json", "r") as f:
        ddi_data = json.load(f)

    # Normalize drug names
    def normalize(name):
        return name.strip().lower()

    # Build symmetric normalized interaction map
    normalized_ddi = {}
    for d1, interactions in ddi_data.items():
        d1_norm = normalize(d1)
        if d1_norm not in normalized_ddi:
            normalized_ddi[d1_norm] = {}

        for d2, interaction in interactions.items():
            d2_norm = normalize(d2)

            # Ensure both directions exist
            if d1_norm not in normalized_ddi:
                normalized_ddi[d1_norm] = {}
            if d2_norm not in normalized_ddi:
                normalized_ddi[d2_norm] = {}

            normalized_ddi[d1_norm][d2_norm] = interaction
            normalized_ddi[d2_norm][d1_norm] = interaction  # 🔄 reverse mapping

    # Build master drug list
    nlem_drugs = sorted(set(normalized_ddi.keys()))

    # Helper to get interaction
    def get_interaction(d1, d2):
        return normalized_ddi.get(normalize(d1), {}).get(normalize(d2))

    # -----------------------------
    # Streamlit App
    # -----------------------------
    st.title("💊 Drug Assistant")
    st.subheader("Drug Interaction Checker")

    # ---------------- Help / How to Use ----------------
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        1. **Search** for a drug using the search bar.  
        2. **Add** it to your list with ➕.  
        3. Repeat to add multiple drugs.  
        4. The app will **automatically check interactions** between all selected drugs.  
        5. Use 🧹 **Clear All Drugs** to start over.
        """)

    if "selected_drugs" not in st.session_state:
        st.session_state.selected_drugs = []

    # ---------------- Search ----------------
    search_query = st.text_input("🔍 Search Drug", "")

    if search_query:
        query_norm = normalize(search_query)
        matching_drugs = [drug for drug in nlem_drugs if query_norm in drug]
        if matching_drugs:
            selected_drug = st.selectbox("Matching Drugs", matching_drugs, key="drug_select")
            if st.button("➕ Add Drug"):
                if normalize(selected_drug) not in [normalize(d) for d in st.session_state.selected_drugs]:
                    st.session_state.selected_drugs.append(selected_drug)
        else:
            st.info("No matching drugs found.")

    # ---------------- Clear button ----------------
    if st.button("🧹 Clear All Drugs"):
        st.session_state.selected_drugs = []

    # ---------------- Show selected ----------------
    if st.session_state.selected_drugs:
        st.subheader("Selected Drugs")
        st.write(", ".join(st.session_state.selected_drugs))

    # ---------------- Check interactions ----------------
    if len(st.session_state.selected_drugs) > 1:
        st.subheader("Interactions Found")
        found = False
        for d1, d2 in combinations(st.session_state.selected_drugs, 2):
            interaction = get_interaction(d1, d2)
            if interaction:
                severity = interaction["severity"].lower()
                desc = interaction["description"]

                if severity == "no interaction":
                    st.success(f"✅ {d1} + {d2} → No Interaction: {desc}")
                elif severity == "monitor closely":
                    st.warning(f"🟠 {d1} + {d2} → Monitor Closely: {desc}")
                elif severity in ["serious - use alternative", "contraindicated"]:
                    st.error(f"❌ {d1} + {d2} → Serious / Contraindicated: {desc}")
                else:
                    st.info(f"{d1} + {d2} → {severity.capitalize()}: {desc}")
                found = True
            else:
                st.info(f"ℹ️ {d1} + {d2} → No interaction data available.")

        if not found:
            st.success("✅ No major interactions found.")

        
#filtered_ddi.json is being used.

# no interaction -> green colour 
# monitor closely -> orange colour
# serious-use alternative -> red colour 
# contraindicated -> red colour
# use these categories with same spelling and all in json too.

# -------------------------
# Normal Values Page
# -------------------------
elif app_mode == "Normal Values":
    st.title("📊 Normal Values")

    # Load JSON file
    with open("normal_values.json", "r", encoding="utf-8") as f:
        normal_values = json.load(f)

    # Search box
    search_query = st.text_input("🔍 Search Normal Value")

    if search_query:
        results = []
        for system, params in normal_values.items():
            for param, value in params.items():
                if search_query.lower() in param.lower():
                    results.append((system, param, value))
        if results:
            for system, param, value in results:
                st.subheader(f"{param} ({system})")
                st.success(f"Normal Range: {value}")
        else:
            st.warning("No matching parameter found.")
    else:
        # If no search, filter by system → parameter
        system = st.selectbox("Select Body System", list(normal_values.keys()))
        param = st.selectbox("Select Parameter", list(normal_values[system].keys()))
        st.subheader(f"{param} ({system})")
        st.info(f"Normal Range: {normal_values[system][param]}")


# ------------------ INDIAN PROTOCOLS ------------------
elif app_mode == "Indian Protocols":
    st.title("📋 Indian Protocols - Emergency Management")

    # Dropdown of protocols
    protocols = [
        "Snakebite",
        "OP Poisoning",
        "Rabies",
        "Anaphylaxis",
        "Seizure",
        "DKA",
        "Acute MI",
        "Status Asthmaticus"
    ]

    selected_protocol = st.selectbox("Select Protocol", protocols)

    if selected_protocol == "OP Poisoning":
        st.subheader("Organophosphorus (OP) Poisoning Management Protocol (AIIMS)")

        with st.expander("1️⃣ Initial Assessment"):
            st.markdown("""
            - Ensure **patient and rescuer safety**.
            - Assess **airway, breathing, circulation (ABCs)**.
            - Remove **contaminated clothing**.
            - Wash skin thoroughly with **soap and running water**.
            - **Do not induce vomiting** unless instructed in hospital.""")

        with st.expander("2️⃣ Clinical Features"):
            st.markdown("""
            OP poisoning leads to **cholinergic excess**. Look for:

            | Feature Type | Examples |
            |--------------|---------|
            | **Muscarinic** | Salivation, lacrimation, urination, diarrhea, GI cramps, miosis, bronchospasm |
            | **Nicotinic** | Muscle fasciculations, weakness, paralysis, hypertension, tachycardia |
            | **CNS** | Anxiety, confusion, seizures, coma |""")

        with st.expander("3️⃣ Investigations"):
            st.markdown("""
            - **Bedside:** 20-min Whole Blood Clotting Test (20WBCT) if snakebite suspected too.
            - **Lab:** CBC, RFT, LFT, Serum Cholinesterase (if available)
            - ABG, electrolytes, ECG (for cardiac monitoring)""")

        with st.expander("4️⃣ Decontamination & Supportive Care"):
            st.markdown("""
            - **Remove contaminated clothing** and wash exposed skin.
            - **Airway management**: Oxygen, suction if excessive secretions.
            - **IV fluids** to maintain perfusion.
            - Monitor vitals, urine output, and oxygen saturation.
            - Treat **seizures** with benzodiazepines (e.g., lorazepam, diazepam).""")

        with st.expander("5️⃣ Antidotes"):
            st.markdown("""
            **Atropine (Muscarinic Antagonist)**
            - Initial dose: 1–2 mg IV in adults (0.05 mg/kg in children)
            - Double dose every 5–10 min until signs of **atropinization**:
                - Drying of secretions
                - Pupils mid-dilated
                - Heart rate normalized
            - **Maintenance infusion**: 10–20% of total loading dose per hour

            **Pralidoxime (2-PAM, Oxime)**
            - Reverses nicotinic effects
            - Dose: 30 mg/kg IV over 15–30 min, may repeat q6–12h
            - Start **early** (within 24h of ingestion) for maximal benefit""")

        with st.expander("6️⃣ Monitoring"):
            st.markdown("""
            - Continuous cardiac monitoring
            - Reassess for atropinization signs and dose adjustments
            - Watch for **intermediate syndrome** (2–4 days post-ingestion):
                - Limb and neck weakness
                - Respiratory muscle involvement
                - Requires ventilatory support if needed""")

        with st.expander("7️⃣ Discharge & Follow-up"):
            st.markdown("""
            - Discharge when **stable, symptom-free, and cholinesterase improving**
            - Educate patient and caregivers on **safe storage of pesticides**
            - Consider **psychiatric evaluation** if intentional poisoning""")

        st.markdown("""
        **References:**
        - AIIMS Clinical Toxicology Protocols, 2023  
        - Indian Journal of Critical Care Medicine: OP Poisoning Guidelines  
        """)

    elif selected_protocol == "Snakebite":
        st.subheader("Snakebite Management Protocol (AIIMS)")

        with st.expander("1️⃣ Initial Assessment"):
            st.markdown("""
            - Ensure **rescuer and patient safety** (identify snake if possible).
            - **Do not cut, suck, or apply tight tourniquets**.
            - Immobilize the bitten limb **below heart level**.
            - Assess **airway, breathing, circulation (ABCs)**.
            - Transport patient **promptly** to the nearest hospital.""")

        with st.expander("2️⃣ Clinical Grading of Envenomation"):
            st.markdown("""
            | Grade | Clinical Features |
            |-------|-----------------|
            | I     | Local pain, swelling |
            | II    | Regional lymphadenopathy, mild systemic signs |
            | III   | Systemic manifestations: neurotoxicity, bleeding, shock |""")

        with st.expander("3️⃣ Investigations"):
            st.markdown("""
            - **Bedside:** 20-minute Whole Blood Clotting Test (20WBCT)  
            - **Lab:** CBC, PT/INR, APTT, RFT, LFT, electrolytes, ECG
            - Monitor **urine output** for early detection of renal involvement""")

        with st.expander("4️⃣ Antivenom Administration (ASV)"):
            st.markdown("""
            - **Polyvalent Anti-Snake Venom (ASV)**:
                - Initial dose: 10 vials IV over 1 hour (diluted in 200 mL NS)
                - Repeat **every 1 hour** until systemic signs improve
                - **Maximum total dose:** 30 vials
            - **Pre-medication:** Hydrocortisone/Antihistamine is optional, not routinely required
            - **Neurotoxic bites:** Monitor respiration, may require mechanical ventilation""")

        with st.expander("5️⃣ Supportive Care"):
            st.markdown("""
            - Oxygen supplementation if hypoxic
            - IV fluids to maintain hemodynamic stability
            - Analgesics for pain (avoid NSAIDs in coagulopathy)
            - Manage shock with crystalloids; vasopressors if needed
            - **Neostigmine + Atropine** for neurotoxic paralysis (as per protocol)
            - Monitor for **coagulopathy and bleeding**""")

        with st.expander("6️⃣ Observation & Follow-up"):
            st.markdown("""
            - Observe patient for **24 hours** after last ASV dose
            - Document:
                - Bite site
                - Snake species if identified
                - Dose of ASV administered
            - Discharge only when **clinically stable and coagulation normal**""")

        with st.expander("7️⃣ Patient Education"):
            st.markdown("""
            - Avoid traditional remedies (cutting, sucking, tying)
            - Educate on prevention: footwear, snake awareness
            - Follow-up for delayed neurological symptoms or wound care""")

        st.markdown("""
        **References:**
        - AIIMS Snakebite Management Protocol, 2023  
        - Ministry of Health & Family Welfare, India: Guidelines for Snakebite Management  
        """)

    elif selected_protocol == "Rabies":
        st.subheader("Rabies Post-Exposure Prophylaxis (PEP) Protocol (India)")

        with st.expander("1️⃣ Immediate First Aid (Wound Management)"):
            st.markdown("""
            - **Wash the wound immediately** with **soap and running water for ≥15 minutes**.
            - **Apply antiseptic**: 70% ethanol, povidone-iodine, or other recommended disinfectant.
            - **Do NOT suture** the wound unless necessary; if suturing is done, avoid injecting vaccine at that site.
            - Remove any contaminated clothing near the bite.""")

        with st.expander("2️⃣ Exposure Assessment"):
            st.markdown("""
            - Classify exposure using **WHO categories**:

            | Category | Description | Risk / PEP Requirement |
            |----------|------------|----------------------|
            | I        | Touching/feeding animals, licks on intact skin | None – PEP not required |
            | II       | Nibbling of uncovered skin, minor scratches/abrasions **without bleeding** | Moderate – PEP indicated |
            | III      | Transdermal bites, scratches, licks on broken skin, mucous membrane contamination | High – PEP indicated **with RIG** |

            - Identify the **animal species** if possible.""")

        with st.expander("3️⃣ Vaccination Schedule"):
            st.markdown("""
            **Essen 5-dose regimen (IM):** Day 0, 3, 7, 14, 28  
            **Intradermal 2-site regimen (Thai Red Cross):** Day 0, 3, 7, 28  
            - Use **Cell Culture Vaccine (CCV) or Purified Vero Cell Vaccine (PVRV)**  
            - **Nerve Tissue Vaccines** are not recommended""")

        with st.expander("4️⃣ Rabies Immunoglobulin (RIG)"):
            st.markdown("""
            - Indicated for **Category III exposures**  
            - **Human RIG (HRIG) / Equine RIG (ERIG)**: infiltrate **around the wound**  
            - Dose: HRIG 20 IU/kg, ERIG 40 IU/kg  
            - Remaining RIG (if any) can be given **IM at site distant from vaccine**""")

        with st.expander("5️⃣ Monitoring & Follow-up"):
            st.markdown("""
            - Complete all **vaccine doses**
            - Monitor wound for infection
            - Advise patient to report any **neurological symptoms**""")

        with st.expander("6️⃣ Special Considerations"):
            st.markdown("""
            - Pregnant or immunocompromised patients: **same PEP schedule**  
            - Previously vaccinated: 2 booster doses only (Day 0 and Day 3)  
            - RIG not required for previously fully vaccinated individuals""")

        st.markdown("""
        **References:**
        - NCDC Rabies Guidelines, India, 2023  
        - AIIMS Clinical Protocols for Rabies PEP  
        - WHO: Rabies Post-Exposure Prophylaxis, 2022
        """)

    elif selected_protocol == "Anaphylaxis":
        st.subheader("Anaphylaxis Management Protocol (India)")

        with st.expander("1️⃣ Immediate First Aid"):
            st.markdown("""
            - **Call for help / emergency services immediately**.
            - **Assess ABCs**:
                - **Airway:** Check for obstruction (laryngeal edema, tongue swelling)
                - **Breathing:** Look for wheezing, stridor, cyanosis
                - **Circulation:** Monitor pulse, blood pressure
            - **Position patient**:
                - Supine with legs elevated (if hypotensive)
                - Upright if severe respiratory distress
            - Remove **trigger** if known (insect sting, drug, food).""")

        with st.expander("2️⃣ First-Line Drug: Epinephrine"):
            st.markdown("""
            - **Dose:** 0.01 mg/kg IM (max 0.5 mg)  
            - Adults: 0.5 mg IM  
            - Children: 0.01 mg/kg IM  
            - **Site:** Mid-outer thigh  
            - Repeat every 5–15 min if symptoms persist""")

        with st.expander("3️⃣ Supportive Care"):
            st.markdown("""
            - **Oxygen:** High-flow via mask if hypoxic
            - **IV fluids:** 20 mL/kg crystalloid bolus for hypotension
            - **Airway support:** Prepare for intubation if airway compromise
            - **Monitor vitals:** BP, HR, SpO₂, urine output""")

        with st.expander("4️⃣ Adjunct Medications"): 
            st.markdown("""
            - **Antihistamines:** 
                - Diphenhydramine 25–50 mg IV/IM (adults)
                - Children: 1 mg/kg IV/IM
            - **Corticosteroids:** 
                - Hydrocortisone 4–8 mg/kg IV (max 300 mg)
                - Prevents biphasic reaction (not for immediate symptom relief)
            - **Bronchodilators:** Salbutamol nebulization if wheezing persists""")

        with st.expander("5️⃣ Observation & Follow-up"):
            st.markdown("""
            - **Monitor patient for at least 4–6 hours** after symptom resolution
            - **Admit if:**
                - Severe anaphylaxis
                - Comorbidities (asthma, cardiovascular disease)
                - Delayed or biphasic reaction risk
            - **Educate patient:**
                - Avoid triggers
                - Prescribe **epinephrine auto-injector** if available
                - Follow-up with allergist""")

        with st.expander("6️⃣ Special Considerations"):
            st.markdown("""
            - Pregnancy: Epinephrine **first-line**, same dose
            - Children: Dose adjustments as above
            - Elderly: Monitor cardiac function during epinephrine use""")
        
        st.markdown("""
        **References:**
        - AIIMS Guidelines on Emergency Medicine, 2023  
        - Indian Academy of Pediatrics (IAP) Anaphylaxis Protocol  
        - WHO & WAO Guidelines for Anaphylaxis Management
        """)

    elif selected_protocol == "Seizure":
        st.subheader("Seizure / Status Epilepticus Management Protocol (India)")

        with st.expander("1️⃣ First Aid During a Seizure"):
            st.markdown("""
            - **Ensure patient safety**: move objects away, protect head.
            - **Do NOT restrain the patient** or put objects in mouth.
            - **Time the seizure**; note duration and type.
            - **Place patient in lateral (recovery) position** once convulsions stop.
            - Maintain **airway and breathing**.""")

        with st.expander("2️⃣ Initial Assessment"):
            st.markdown("""
            - Check **ABCs** (Airway, Breathing, Circulation).
            - **Vitals:** BP, HR, SpO₂, temperature.
            - **Blood glucose**: treat hypoglycemia if present.""")

        with st.expander("3️⃣ Investigations"):
            st.markdown("""
            - Blood: CBC, electrolytes, glucose, calcium, magnesium, renal and liver function.
            - EEG: if available after stabilization.
            - Neuroimaging (CT/MRI) if new-onset seizure or focal deficits.
            - Toxicology screen if poisoning suspected.""")

        with st.expander("4️⃣ Acute Management (Status Epilepticus)"):
            st.markdown("""
            **First-line: Benzodiazepines**
            - **IV Lorazepam:** 0.1 mg/kg (max 4 mg) over 2–5 min  
            - **If IV unavailable:** Diazepam 0.2 mg/kg IV (max 10 mg) or Rectal Diazepam
            - Repeat dose after 10–15 min if seizure persists.

            **Second-line: Antiepileptics**
            - **Phenytoin:** 20 mg/kg IV (max 1 g), slow infusion ≤50 mg/min
            - **Fosphenytoin:** 20 mg PE/kg IV, faster and safer alternative
            - Alternatives: Valproate IV 20–40 mg/kg, Levetiracetam IV 60 mg/kg""")

        with st.expander("5️⃣ Supportive Care"):
            st.markdown("""
            - Oxygen supplementation as needed
            - Cardiac and respiratory monitoring
            - Correct **electrolyte disturbances**
            - Maintain **IV access**
            - Monitor urine output""")

        with st.expander("6️⃣ Refractory Status Epilepticus"):
            st.markdown("""
            - Continuous infusion of **midazolam, propofol, or thiopentone** in ICU
            - Intubation and mechanical ventilation if required
            - Identify and treat underlying cause""")

        with st.expander("7️⃣ Observation & Follow-up"):
            st.markdown("""
            - Admit patient for monitoring if:
                - Prolonged seizure >5 min
                - New-onset seizure
                - Focal neurological deficits
            - Post-seizure care:
                - Neuro assessment
                - Medication review
                - Patient and caregiver education""")
            
        st.markdown("""
        **References:**
        - AIIMS Clinical Protocols: Status Epilepticus, 2023  
        - Indian Epilepsy Society (IES) Guidelines  
        - ILAE Guidelines on Status Epilepticus
        """)

    elif selected_protocol == "DKA":
        st.subheader("Diabetic Ketoacidosis (DKA) Management Protocol (India)")

        with st.expander("1️⃣ Initial Assessment"):
            st.markdown("""
            - **Airway, Breathing, Circulation (ABCs)**
            - **Level of consciousness**: use GCS
            - **Vitals:** BP, HR, RR, SpO₂, temperature
            - **Severity classification:** mild, moderate, severe DKA based on pH, bicarbonate, mental status""")

        with st.expander("2️⃣ Immediate Investigations"):
            st.markdown("""
            - Blood glucose
            - Serum electrolytes: Na⁺, K⁺, Cl⁻, HCO₃⁻
            - Renal function: urea, creatinine
            - Serum ketones or urine ketones
            - Arterial blood gas (ABG)
            - CBC
            - ECG (especially if K⁺ abnormal)
            - Serum osmolality if hyperosmolar features suspected""")

        with st.expander("3️⃣ Initial Stabilization"):
            st.markdown("""
            - **IV fluids:** 
                - Start with 0.9% NaCl 15–20 mL/kg (1–1.5 L) in first hour
                - Adjust based on hemodynamics and hydration
            - **Monitor vitals** and urine output
            - **Correct potassium before insulin** if K⁺ < 3.3 mEq/L""")

        with st.expander("4️⃣ Electrolyte Management"):
            st.markdown("""
            - **Potassium replacement:**
                - K⁺ 3.3–5.5 mEq/L: add 20–30 mEq K⁺ per L IV fluid
                - K⁺ < 3.3 mEq/L: replace **before insulin**
                - K⁺ > 5.5 mEq/L: monitor without supplementation initially
            - **Other electrolytes:** correct phosphate and magnesium if needed""")

        with st.expander("5️⃣ Insulin Therapy"):
            st.markdown("""
            - **Regular insulin IV infusion:** 0.1 U/kg/h
            - **Target glucose reduction:** 50–100 mg/dL per hour
            - **Switch to subcutaneous insulin** once ketosis resolves and patient can eat""")

        with st.expander("6️⃣ Monitor & Adjust"):
            st.markdown("""
            - **Blood glucose:** hourly
            - **Electrolytes:** every 2–4 hours
            - **Fluid status**: input/output, hemodynamics
            - **Acid-base status:** ABG every 4–6 hours
            - Adjust insulin and fluids based on ongoing labs""")

        with st.expander("7️⃣ Transition to Subcutaneous Insulin"):
            st.markdown("""
            - Start **basal-bolus regimen** when:
                - pH > 7.3
                - Bicarbonate > 18 mEq/L
                - Patient able to take oral intake""")

        with st.expander("8️⃣ Identify & Treat Precipitating Factors"):
            st.markdown("""
            - Infection
            - MI or other acute illness
            - Medication non-compliance""")

        st.markdown("""
        **References:**
        - AIIMS Clinical Endocrinology Guidelines, 2023  
        - ISPAD / ADA DKA Management Guidelines  
        - Indian Journal of Endocrinology and Metabolism, DKA Protocol
        """)


    elif selected_protocol == "Acute MI":
        st.subheader("Acute Myocardial Infarction (AMI) Management Protocol (India)")

        with st.expander("1️⃣ Immediate Assessment"):
            st.markdown("""
            - **Airway, Breathing, Circulation (ABCs)**
            - **Vitals:** BP, HR, SpO₂, temperature
            - **ECG:** perform **within 10 minutes** of arrival
            - **Identify type of MI:** STEMI vs NSTEMI
            - **Assess risk factors:** age, diabetes, hypertension, smoking, prior CAD""")

        with st.expander("2️⃣ Initial Investigations"): 
            st.markdown("""
            - 12-lead ECG
            - Cardiac biomarkers: Troponin I/T, CK-MB
            - CBC, renal function, electrolytes
            - Chest X-ray if pulmonary edema suspected
            - Echocardiography for wall motion abnormalities if available""")

        with st.expander("3️⃣ Immediate Management (First Aid)"):
            st.markdown("""
            - **Oxygen** if SpO₂ < 90%
            - **Aspirin 150–300 mg** orally, chewed
            - **Nitroglycerin** sublingual 0.3–0.6 mg if no hypotension
            - **Morphine** 2–4 mg IV for pain if not relieved by nitro
            - **IV access** and continuous cardiac monitoring""")

        with st.expander("4️⃣ Reperfusion Strategy"): 
            st.markdown("""
            **STEMI:**
            - **Primary PCI** (preferred, within 120 min of first medical contact)
            - If PCI not available: **Fibrinolysis** (alteplase, tenecteplase) within 30 min
            - **Anticoagulation** with UFH or LMWH during reperfusion

            **NSTEMI:**
            - Risk stratification (TIMI / GRACE score)
            - **Early invasive strategy** for high-risk patients
            - **Medical management** for low-risk patients""")

        with st.expander("5️⃣ Adjunct Medications"):
            st.markdown("""
            - **Beta-blockers:** IV or oral if no hypotension or bradycardia
            - **ACE inhibitors / ARBs:** start early if LV dysfunction, hypertension
            - **Statins:** high-intensity (atorvastatin 40–80 mg)
            - **Antiplatelets:** dual therapy (aspirin + clopidogrel/ticagrelor)
            - **Anticoagulants:** UFH, enoxaparin as per protocol""")

        with st.expander("6️⃣ Monitoring & Supportive Care"):
            st.markdown("""
            - Continuous ECG monitoring
            - Monitor for arrhythmias, heart failure, cardiogenic shock
            - Serial cardiac biomarkers
            - Manage complications: pulmonary edema, hypotension, ventricular arrhythmias""")

        with st.expander("7️⃣ Discharge & Secondary Prevention"):
            st.markdown("""
            - Lifestyle modification: smoking cessation, diet, exercise
            - Continue **dual antiplatelet therapy** (DAPT)
            - **Beta-blockers, ACE inhibitors/ARBs, statins**
            - Cardiac rehabilitation referral
            - Patient education on warning signs of recurrent MI""")

        st.markdown("""
        **References:**
        - AIIMS Cardiology Protocols, 2023  
        - Indian Council of Medical Research (ICMR) STEMI/NSTEMI Guidelines  
        - European Society of Cardiology (ESC) Guidelines adapted for India
        """)

    elif selected_protocol == "Status Asthmaticus":
        st.subheader("Status Asthmaticus Management Protocol (India)")

        with st.expander("1️⃣ Immediate Assessment"):
            st.markdown("""
            - **Airway, Breathing, Circulation (ABCs)**
            - **Vitals:** BP, HR, RR, SpO₂, temperature
            - **Severity assessment:**
                - SpO₂ < 90%
                - PEF < 50% predicted
                - Inability to speak full sentences
                - Use of accessory muscles""")

        with st.expander("2️⃣ First Aid / Initial Measures"):
            st.markdown("""
            - Place patient **upright** to aid breathing
            - **Administer high-flow oxygen** to maintain SpO₂ ≥ 94%
            - **Continuous cardiac and SpO₂ monitoring**
            - Establish **IV access**""")

        with st.expander("3️⃣ Rapid-Acting Bronchodilators"):
            st.markdown("""
            - **Salbutamol (Albuterol)**
                - Nebulization: 2.5 mg every 20 min for first hour, then q1–4h
                - Alternative: MDI with spacer if available
            - **Ipratropium bromide**: 0.5 mg nebulization every 6–8 h""")

        with st.expander("4️⃣ Systemic Corticosteroids"):
            st.markdown("""
            - **IV Hydrocortisone:** 4–8 mg/kg/day divided q6–8h (max 300 mg/day)
            - **Oral Prednisolone:** 1–2 mg/kg/day if patient can swallow
            - Continue for 5–7 days""")

        with st.expander("5️⃣ Adjunct / Escalation Therapy"):
            st.markdown("""
            - **Magnesium sulfate:** 25–75 mg/kg IV over 20 min if severe obstruction persists
            - **Aminophylline IV infusion:** 5–6 mg/kg loading, then 0.5–1 mg/kg/h
            - **Heliox or non-invasive ventilation** if available""")

        with st.expander("6️⃣ Monitoring & Supportive Care"):
            st.markdown("""
            - Continuous ECG, SpO₂, and blood pressure
            - Monitor mental status for CO₂ retention
            - Repeat **PEF or spirometry** if feasible
            - Assess response to therapy every 15–30 min""")

        with st.expander("7️⃣ Indications for ICU / Intubation"):
            st.markdown("""
            - Altered consciousness
            - Respiratory fatigue or PaCO₂ rising
            - Hypoxemia not improving with oxygen
            - Impending respiratory arrest""")

        with st.expander("8️⃣ Discharge & Follow-up"):
            st.markdown("""
            - Continue inhaled bronchodilators and oral steroids
            - Educate patient and caregivers on:
                - Trigger avoidance
                - Early recognition of exacerbations
                - Proper inhaler technique
            - Schedule **follow-up with pulmonologist**""")

        st.markdown("""
        **References:**
        - AIIMS Asthma Management Guidelines, 2023  
        - GINA 2023 Guidelines (adapted for India)  
        - Indian Journal of Pediatrics: Severe Asthma Protocols
        """)


st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; color: #888888; font-size: 12px; line-height: 1.4;'>
    ⚠️ <b>Disclaimer:</b> This app is intended for educational and informational purposes only.  
    It is <i>not</i> a substitute for professional medical advice, diagnosis, or treatment.  
    Always consult a qualified healthcare provider for clinical decisions.
    <br><br>
    © 2025 <b>ksnath.com</b>. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
