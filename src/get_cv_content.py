# Load pdf file
from langchain_community.document_loaders import PyPDFLoader
from io import BytesIO
import PyPDF2


def get_cv(cv_dir):

    doc_loader = PyPDFLoader(cv_dir)

    cv = doc_loader.load()
    cv = cv[0].page_content

    #cv = clean_data(cv)

    return cv

def extract_text_from_cv(uploaded_file):
    if uploaded_file is not None:
        # Extract text from the uploaded PDF file using PyPDF2
        # Convert the uploaded file to a BytesIO object
        file_stream = BytesIO(uploaded_file.getvalue())
        # Initialize the PDF reader
        pdf_reader = PyPDF2.PdfReader(file_stream)
        # Concatenate text from each page
        cv = ""
        for page in pdf_reader.pages:
            cv += page.extract_text() or ""  # or use page.extract_text() + '\n' for space between pages
        return cv
    else: 
        return "No file uploaded or file is empty."


if __name__ == "__main__":
    cv_dir = 'resources/cv.pdf'
    cv = get_cv(cv_dir)
    print(cv)