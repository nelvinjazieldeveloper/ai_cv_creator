# AI-Powered CV Generator

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ai-cv-generator.git
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the API with Uvicorn
  ```
  uvicorn main:app --reload
  ```

2. Start the Streamlit application:
   ```
   streamlit run app.py
   ```
3. Open your web browser and navigate to `http://localhost:8000`.
4. Fill out the form with your personal information, work experience, education, skills, and languages.
5. Click the "🪄 Generate CV with AI" button to generate your professional CV.
6. Review and edit the generated CV as needed.
7. Click the "📄 Generate PDF" button to download your CV as a PDF file.

## API

The project includes a backend API built with FastAPI. The API endpoint `/generate-cv` accepts a JSON payload with the following structure:

```json
{
  "full_name": "John Doe",
  "profession": "Software Engineer",
  "email": "john@example.com",
  "phone": "+358 40 123 4567",
  "location": "Helsinki, Finland",
  "linkedin": "https://linkedin.com/in/johndoe",
  "experiences": [
    {
      "title": "Software Engineer",
      "company": "Acme Inc.",
      "start_date": "01/2018",
      "end_date": "12/2020",
      "description": "- Developed and maintained web applications\n- Improved system performance by 30%\n- Led cross-functional team"
    }
  ],
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University of Helsinki",
      "year": 2017
    }
  ],
  "skills": "- Python\n- JavaScript\n- Project Management",
  "languages": "- English (Fluent)\n- Finnish (Intermediate)"
}
```

The API will respond with a JSON object containing the generated CV in Markdown format.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).