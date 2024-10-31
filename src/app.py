import streamlit as st
from generate_cover_letter import generate_cover_letter
from get_cv_content import extract_text_from_cv

def app():
    st.title('Cover Letter Generator')
    # inputs
    job_post_link = st.text_input('Enter job URL: ', value=None)

    # PDF File uploader
    uploaded_file = st.file_uploader("Upload you CV (pdf only)", type=['pdf'])
    if uploaded_file is not None:
        st.success('File successfully uploaded!')

    submit_button = st.button("Submit and Generate")

    if submit_button:
        try:
            #st.write(f"You submitted the URL: {job_post_link}")
            extracted_text = extract_text_from_cv(uploaded_file)
            cover_letter = generate_cover_letter(job_post_link, extracted_text)

            #st.code(motivation_letter, language='markdown')
            st.write(cover_letter)
            # write the letter to pdf doc and make it downloadable
    
        except Exception as error:
            st.error(f"Error Occurred {error}")

if __name__ == "__main__":
    app()
#

