import streamlit as st
import numpy as np
import pickle
from pdfgen import generate_pdf_report

# List of symptoms and diseases
l1 = ['anorexia','abdominal_pain','anaemia','abortions','acetone','aggression','arthrogyposis',
    'ankylosis','anxiety','bellowing','blood_loss','blood_poisoning','blisters','colic','Condemnation_of_livers',
    'coughing','depression','discomfort','dyspnea','dysentery','diarrhoea','dehydration','drooling',
    'dull','decreased_fertility','diffculty_breath','emaciation','encephalitis','fever','facial_paralysis','frothing_of_mouth',
    'frothing','gaseous_stomach','highly_diarrhoea','high_pulse_rate','high_temp','high_proportion','hyperaemia','hydrocephalus',
    'isolation_from_herd','infertility','intermittent_fever','jaundice','ketosis','loss_of_appetite','lameness',
    'lack_of-coordination','lethargy','lacrimation','milk_flakes','milk_watery','milk_clots',
    'mild_diarrhoea','moaning','mucosal_lesions','milk_fever','nausea','nasel_discharges','oedema',
    'pain','painful_tongue','pneumonia','photo_sensitization','quivering_lips','reduction_milk_vields','rapid_breathing',
    'rumenstasis','reduced_rumination','reduced_fertility','reduced_fat','reduces_feed_intake','raised_breathing','stomach_pain',
    'salivation','stillbirths','shallow_breathing','swollen_pharyngeal','swelling','saliva','swollen_tongue',
    'tachycardia','torticollis','udder_swelling','udder_heat','udder_hardeness','udder_redness','udder_pain','unwillingness_to_move',
    'ulcers','vomiting','weight_loss','weakness']

disease = ['mastitis','blackleg','bloat','coccidiosis','cryptosporidiosis',
        'displaced_abomasum','gut_worms','listeriosis','liver_fluke','necrotic_enteritis','peri_weaning_diarrhoea',
        'rift_valley_fever','rumen_acidosis',
        'traumatic_reticulitis','calf_diphtheria','foot_rot','foot_and_mouth','ragwort_poisoning','wooden_tongue','infectious_bovine_rhinotracheitis',
    'acetonaemia','fatty_liver_syndrome','calf_pneumonia','schmallen_berg_virus','trypanosomosis','fog_fever']

# Function to predict disease based on symptoms
def predict_disease(symptoms):
    with open("random_forest_model.pkl", "rb") as file:
        model = pickle.load(file)
    # Preprocess input symptoms
    input_symptoms = [1 if symptom in symptoms else 0 for symptom in l1]
    # Reshape input symptoms for prediction
    input_symptoms = np.array(input_symptoms).reshape(1, -1)
    # Use the trained model for prediction
    prediction_rf = model.predict(input_symptoms)
    predicted_disease_rf = disease[int(prediction_rf)]
    # Return predictions
    return predicted_disease_rf

# Load the trained model

def disease_finder():
    st.markdown("<h1 style='text-align: left; color: #49f222; font-size: 46px; font-weight:600;'>Animal Disease Prediction</h1>", unsafe_allow_html=True)
    st.write("Select 5 symptoms from the dropdown menus:")

    # Dropdown menus for symptoms
    selected_symptoms = []
    for i in range(5):
        symptom = st.selectbox(f"Symptom {i+1}", l1)
        selected_symptoms.append(symptom)

    # Predict button
    if st.button("Predict"):
        if selected_symptoms:
            # Predict disease based on input symptoms
            predicted_disease_rf = predict_disease(selected_symptoms)
            # Display predicted disease
            st.write("Predicted Disease:", predicted_disease_rf)
            pdf_filename = generate_pdf_report(selected_symptoms, predicted_disease_rf)
            st.write(f"PDF Report Generated: {pdf_filename}")
        else:
            st.write("Please select symptoms.")

        
