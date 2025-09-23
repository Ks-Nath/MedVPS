import streamlit as st
import json
from itertools import combinations
import math
from streamlit_tags import st_tags
 
# ------------------ APP CONFIG ------------------
st.set_page_config(page_title="Advanced Medical App", layout="wide")

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
    st.title("🏥 Welcome to the Medical Suite")
    st.markdown("""
    This app is DESIGNED for doctors, medical students, and healthcare professionals.  
    Use the sidebar to navigate to:
    - **Calculator:** Access medical calculators by specialty  
    - **Drug Assistant:** Search interactions, dosages, side effects  
    - **Indian Protocols:** View evidence-based clinical protocols
    
    ---
    🔬 *All tools are built for educational and professional support only.*
    """)


# ------------------ CALCULATORS ------------------
elif app_mode == "Calculator":
    st.title("🧮 Medical Calculators")
    #sri
    # Define calculator categories
    calculators_by_category = {
    "General": ["BMI", "BSA", "Ideal Body Weight", "Body Fat %", "Creatinine Clearance", "MAP"],
    "Cardiology": ["CHA2DS2-VASc", "HAS-BLED", "Heart Rate", "Framingham Risk", "TIMI Risk", "GRACE Score", "eGFR"],
    "Pulmonology": ["Wells Score PE", "CURB-65", "PaO2/FiO2", "Predicted PFT"],
    "Nephrology": ["eGFR", "Creatinine Clearance", "Urine Output", "FeNa"],
    "Endocrinology": ["HbA1c to Avg Glucose", "HOMA-IR", "Total Daily Insulin Requirement", "Corrected Calcium", "Corrected Sodium", "Calcium-Phosphate Product", "FRAX", "Serum Osmolality", "Water Deficit", "Anion Gap"],
    "Mental Health": ["GAD-7", "PHQ-9", "MMSE"],
    "Hematology": ["INR", "NLR", "PLR"],
    "Gastroenterology": ["Child-Pugh", "MELD", "APRI"],
    "Critical Care": ["SOFA", "APACHE II", "SIRS"],
    "Obstetrics": ["Gestational Age", "Bishop Score", "BMI in Pregnancy"]
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
        st.info("SOFA Score requires multiple organ parameters. Add inputs for PaO2/FiO2, Platelets, Bilirubin, MAP, GCS, Creatinine.")
        st.info("You can calculate total score by assigning 0-4 points per organ system.")

    elif selected_calculator == "APACHE II":
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
    # -----------------------------
    # Load JSON
    # -----------------------------
    with open("filtered_ddi.json", "r") as f:
        ddi_data = json.load(f)

    # Build list of all drugs
    nlem_drugs = list(ddi_data.keys())
    for interactions in ddi_data.values():
        for drug in interactions.keys():
            if drug not in nlem_drugs:
                nlem_drugs.append(drug)
    nlem_drugs = sorted(nlem_drugs)

    # Helper to get interaction
    def get_interaction(d1, d2):
        return ddi_data.get(d1, {}).get(d2) or ddi_data.get(d2, {}).get(d1)

    # -----------------------------
    # Streamlit App
    # -----------------------------
    st.title("💊 Drug Assistant")
    st.subheader("Drug Interaction Checker")

    # Initialize session state
    if "selected_drugs" not in st.session_state:
        st.session_state.selected_drugs = []

    # ---------------- Search like calculator ----------------
    search_query = st.text_input("🔍 Search Drug", "")

    if search_query:
        matching_drugs = [drug for drug in nlem_drugs if search_query.lower() in drug.lower()]
        if matching_drugs:
            selected_drug = st.selectbox("Matching Drugs", matching_drugs, key="drug_select")
            if st.button("➕ Add Drug"):
                if selected_drug not in st.session_state.selected_drugs:
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

    # Normal values grouped by system
    normal_values = {
        "Cardiovascular": {
            "Blood Pressure": "Systolic 90–120 mmHg, Diastolic 60–80 mmHg",
            "Pulse Rate": "60 – 100 bpm",
            "Mean Arterial Pressure": "70 – 100 mmHg",
        },
        "Respiratory": {
            "Respiratory Rate": "12 – 20 breaths/min",
            "Oxygen Saturation (SpO₂)": "95 – 100%",
            "PaO₂": "80 – 100 mmHg",
            "PaCO₂": "35 – 45 mmHg",
        },
        "Renal / Electrolytes": {
            "Sodium (Na⁺)": "135 – 145 mmol/L",
            "Potassium (K⁺)": "3.5 – 5.0 mmol/L",
            "Creatinine": "0.7 – 1.3 mg/dL (men), 0.6 – 1.1 mg/dL (women)",
            "Urea": "15 – 40 mg/dL",
        },
        "Hematology": {
            "Hemoglobin (Hb)": "13.5 – 17.5 g/dL (men), 12.0 – 15.5 g/dL (women)",
            "WBC Count": "4,000 – 11,000 /µL",
            "Platelet Count": "150,000 – 450,000 /µL",
            "Hematocrit (Hct)": "41 – 53% (men), 36 – 46% (women)",
        },
        "Metabolic / Endocrine": {
            "Random Blood Sugar": "< 140 mg/dL",
            "Fasting Blood Sugar": "70 – 99 mg/dL",
            "Postprandial Blood Sugar": "< 140 mg/dL",
            "HbA1c": "< 5.7% (normal)",
        },
        "General": {
            "Body Temperature": "36.5 – 37.5 °C",
            "BMI": "18.5 – 24.9 kg/m²",
        }
    }

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
    st.title("📋 Indian Protocols")
    st.info("Coming soon: Indian medical treatment protocols and clinical pathways.")
