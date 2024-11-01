import streamlit as st
from generate_cover_letter import generate_cover_letter
from get_cv_content import extract_text_from_cv

def app() -> None:
    """Main application for cover letter generation"""
    st.title('Cover Letter Generator')

    job_post_link = st.text_input('Enter job URL: ', value=None)
    uploaded_file = st.file_uploader("Upload you CV (pdf only)", type=['pdf'])

    if uploaded_file is not None:
        st.success('File successfully uploaded!')

    if st.button("Submit and Generate"):
        if not job_post_link or uploaded_file is None:
            st.error("Please provide both a job URL and upload your CV.")
            return
        
        try:
            extracted_text = extract_text_from_cv(uploaded_file)
            cover_letter = generate_cover_letter(job_post_link, extracted_text)
            #st.code(motivation_letter, language='markdown')
            st.write(cover_letter)

        # Exception handling
        except FileNotFoundError:
            st.error("The upladed file cannot be found")
        except ValueError as value_error:
            st.error(f"Value error: {value_error}")
        except Exception as error:
            st.error(f"Error Occurred {error}")

if __name__ == "__main__":
    app()
#

