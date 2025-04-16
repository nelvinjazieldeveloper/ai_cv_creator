import streamlit as st
import requests
from fpdf import FPDF
import base64
import re

# Configuración
BACKEND_URL = "http://localhost:8000"  # Cambia en producción
st.set_page_config(page_title="AI CV Generator", layout="wide")

# Clase PDF mejorada
class EuropassPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(20, 15, 20)
        self.set_auto_page_break(True, 15)
    
    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, title, 0, 1)
        self.ln(2)
        self.set_font("Arial", "", 11)
        
        # Procesar contenido con viñetas
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('-'):
                self.cell(10)
                self.multi_cell(0, 6, line[1:].strip())
            else:
                self.multi_cell(0, 6, line)
        self.ln(5)

# Estado de la sesión
if 'cv_data' not in st.session_state:
    st.session_state.cv_data = None
if 'cv_markdown' not in st.session_state:
    st.session_state.cv_markdown = ""
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Formulario principal
st.title("AI-Powered CV Generator")
st.markdown("Complete the form and let AI create your professional CV")

with st.expander("🧑 Personal Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name*", placeholder="John Doe")
    with col2:
        profession = st.text_input("Profession*", placeholder="Software Engineer")
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email*", placeholder="john@example.com")
    with col2:
        phone = st.text_input("Phone", placeholder="+358 40 123 4567")
    
    location = st.text_input("Location*", placeholder="Helsinki, Finland")
    linkedin = st.text_input("LinkedIn", placeholder="https://linkedin.com/in/yourprofile")

with st.expander("💼 Work Experience"):
    jobs = []
    num_jobs = st.number_input("Number of positions", min_value=1, max_value=5, value=1)
    
    for i in range(num_jobs):
        st.markdown(f"#### Position {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input(f"Job Title* {i+1}", key=f"job_title_{i}")
        with col2:
            company = st.text_input(f"Company* {i+1}", key=f"company_{i}")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.text_input(f"Start Date* {i+1} (MM/YYYY)", key=f"start_{i}")
        with col2:
            end_date = st.text_input(f"End Date* {i+1} (MM/YYYY or Present)", key=f"end_{i}")
        
        description = st.text_area(
            f"Description & Achievements* {i+1}",
            value="• Improved system performance by 30%\n• Led cross-functional team",
            key=f"desc_{i}"
        )
        
        jobs.append({
            "title": job_title,
            "company": company,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        })

with st.expander("🎓 Education"):
    education = []
    num_edu = st.number_input("Number of degrees", min_value=1, max_value=3, value=1)
    
    for i in range(num_edu):
        st.markdown(f"#### Degree {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            degree = st.text_input(f"Degree* {i+1}", key=f"degree_{i}")
        with col2:
            institution = st.text_input(f"Institution* {i+1}", key=f"institution_{i}")
        
        year = st.number_input(f"Year Completed* {i+1}", min_value=1900, max_value=2100, value=2020, key=f"year_{i}")
        
        education.append({
            "degree": degree,
            "institution": institution,
            "year": year
        })

with st.expander("🛠️ Skills & Languages"):
    skills = st.text_area(
        "Skills*",
        value="- Python\n- JavaScript\n- Project Management",
        height=100
    )
    
    languages = st.text_area(
        "Languages*",
        value="- English (Fluent)\n- Finnish (Intermediate)",
        height=100
    )

# Generación del CV
if st.button("🪄 Generate CV with AI"):
    required_fields = [
        full_name, profession, email, location,
        any(job["title"] for job in jobs),
        any(edu["degree"] for edu in education),
        skills, languages
    ]
    
    if not all(required_fields):
        st.error("Please complete all required fields (*)")
    else:
        cv_data = {
            "full_name": full_name,
            "profession": profession,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "experiences": jobs,
            "education": education,
            "skills": skills,
            "languages": languages
        }
        
        st.session_state.cv_data = cv_data
        
        with st.spinner("Generating professional CV with AI..."):
            try:
                response = requests.post(f"{BACKEND_URL}/generate-cv", json=cv_data)
                if response.status_code == 200:
                    st.session_state.cv_markdown = response.json()["cv_markdown"]
                    st.session_state.edit_mode = True
                    st.success("CV generated! Review and edit below")
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# Edición y descarga
if st.session_state.edit_mode:
    st.markdown("---")
    st.subheader("Review & Edit Your CV")
    
    edited_cv = st.text_area(
        "Make any necessary adjustments:",
        value=st.session_state.cv_markdown,
        height=400,
        key="cv_editor"
    )
    
    if st.button("💾 Save Changes"):
        st.session_state.cv_markdown = edited_cv
        st.success("Changes saved!")
    
    # Generar PDF
    if st.button("📄 Generate PDF"):
        with st.spinner("Creating PDF..."):
            try:
                pdf = EuropassPDF()
                pdf.add_page()
                
                # Procesar markdown a PDF
                current_section = ""
                current_content = []
                
                for line in edited_cv.split('\n'):
                    if line.startswith('## '):  # Encabezado de sección
                        if current_section:
                            pdf.add_section(current_section, "\n".join(current_content))
                            current_content = []
                        current_section = line[3:].strip()
                    elif line.strip():
                        current_content.append(line)
                
                if current_section:  # Añadir última sección
                    pdf.add_section(current_section, "\n".join(current_content))
                
                pdf_output = pdf.output(dest="S").encode("latin-1", "replace")
                pdf_b64 = base64.b64encode(pdf_output).decode()
                
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_output,
                    file_name=f"{full_name.replace(' ', '_')}_CV.pdf",
                    mime="application/pdf"
                )
                
                st.markdown(
                    f'<a href="data:application/pdf;base64,{pdf_b64}" target="_blank">'
                    '<button style="padding: 0.5rem 1rem; background: #f0f2f6; border-radius: 4px; border: 1px solid #ddd;">'
                    '👀 Preview in Browser</button></a>',
                    unsafe_allow_html=True
                )
            
            except Exception as e:
                st.error(f"PDF generation error: {str(e)}")

# Instrucciones
st.markdown("---")
st.markdown("""
**Instructions:**
1. Fill all fields (required *)
2. Click "Generate CV with AI"
3. Review and edit the generated CV
4. Download as PDF when satisfied
""")