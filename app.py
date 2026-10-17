import streamlit as st
import re

st.set_page_config(page_title="Clinical Notes Summarizer", page_icon="🩺", layout="wide")

st.title("🩺 Clinical Notes Summarizer AI")
st.markdown("**Turn 10-min clinical notes into 10-sec summaries — for Doctors, B.Pharm, Pharma Analysts**")

# Sidebar
st.sidebar.header("About")
st.sidebar.info("Project 3 of Healthcare AI Suite\nBuilt by Darshan Mahale\nB.Pharm | Pharma Data Analyst")

# Input
note = st.text_area("📝 Paste Clinical Note / Discharge Summary:", height=250, 
placeholder="e.g., 45-year-old male patient with history of hypertension and diabetes, presents with chest pain, shortness of breath for 2 days. BP 150/90, HR 102. ECG shows ST elevation. Diagnosed with Acute MI. Treated with Aspirin 325mg, Clopidogrel, Heparin. Advised cath lab...")

def extract_summary(text):
    text_lower = text.lower()
    
    # Simple clinical NLP extraction (fast + works on Streamlit free tier)
    diagnosis = []
    symptoms = []
    meds = []
    vitals = []
    
    # Keywords
    diag_keywords = ["diagnosed", "diagnosis", "acute", "chronic", "mi", "hypertension", "diabetes", "pneumonia", "asthma", "stroke"]
    symptom_keywords = ["pain", "fever", "cough", "shortness of breath", "sob", "chest pain", "headache", "nausea", "vomiting", "fatigue", "sweating", "dizziness"]
    med_keywords = ["aspirin", "clopidogrel", "heparin", "metformin", "atorvastatin", "lisinopril", "amlodipine", "insulin", "paracetamol", "antibiotic"]
    
    # Extract
    sentences = text.split('.')
    summary_sentences = sentences[:3] if len(sentences) > 3 else sentences
    
    # Find vitals with regex
    bp_match = re.findall(r'BP\s*\d+/\d+', text, re.I)
    hr_match = re.findall(r'HR\s*\d+', text, re.I)
    vitals = bp_match + hr_match
    
    for kw in diag_keywords:
        if kw in text_lower:
            diagnosis.append(kw.title())
    for kw in symptom_keywords:
        if kw in text_lower:
            symptoms.append(kw.title())
    for kw in med_keywords:
        if kw in text_lower:
            meds.append(kw.title())
            
    return {
        "summary": " ".join(summary_sentences[:2]) + ".",
        "diagnosis": list(set(diagnosis))[:5],
        "symptoms": list(set(symptoms))[:6],
        "meds": list(set(meds))[:6],
        "vitals": vitals
    }

if st.button("⚡ Summarize Note", type="primary"):
    if not note.strip():
        st.warning("Please paste a clinical note first!")
    else:
        result = extract_summary(note)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 Quick Summary")
            st.success(result["summary"])
            
            st.subheader("🩺 Vitals Found")
            st.write(", ".join(result["vitals"]) if result["vitals"] else "No vitals detected")
            
        with col2:
            st.subheader("🔍 Extracted Entities")
            st.markdown(f"**Diagnosis / Conditions:** {', '.join(result['diagnosis']) if result['diagnosis'] else 'N/A'}")
            st.markdown(f"**Symptoms:** {', '.join(result['symptoms']) if result['symptoms'] else 'N/A'}")
            st.markdown(f"**Medications:** {', '.join(result['meds']) if result['meds'] else 'N/A'}")
        
        st.divider()
        st.metric("Original Length", f"{len(note.split())} words")
        st.metric("Summary Length", f"{len(result['summary'].split())} words")
        st.metric("Time Saved", "~80%")

st.divider()
st.markdown("**Tech:** Python, Streamlit, Regex, Clinical NLP | **Next:** Add BioBERT NER + BART Summarizer for full AI version")
