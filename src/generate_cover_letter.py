from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

from get_cv_content import get_cv
from get_job_content import Job_info

load_dotenv()

def get_job_info(job_link, llm):
    job_info = Job_info(llm)
    job_info_response = job_info.get_job(job_link=job_link)

    # exception: check is job_info_response is null

    return job_info_response


def generate_cover_letter(job_link, cv_text):
    '''Generate Cover letter based on provided job URL and CV document'''
    llm = ChatGroq(temperature=0, api_key=os.getenv("API_KEY"), model_name="llama-3.1-70b-versatile")
    job_info = get_job_info(job_link, llm)

    # Write a prompt that create a cover letter for a given job based on my previous cover letters and CV
    cover_letter_prompt = PromptTemplate.from_template(
    """
    ### Job Description
    {job_description}

    ### Instruction
    You are an expert in writing cover letters for given job decriptions and CVs of the candidates.

    Write an cover letter for the above mentioned Job description using professional language yet personal to the cv provided.
    Please use the previously written {cv} to get information of expereince, skills and knowledge of the candidate.
    When creating the cover letter follow:
        1. Make it human written
        2. Do not parapahase the job description but be creative
        3. Argue that based on the expereince, skills and knowledge, that this candidate is suitable for the job
        4. Importantly, show that the candidate is willing and has potential learn new domain and skills to presfom the job basd on his/her previous professional experience.
        5. Make a positive imparession of the canditate from the beggining.
        6. Include keywords, terms and phrases, that may important picked from CV that match with job description and requirements to make the cover letter pass through computer systems when short listing.
        7. No postamble at the end just the cover letter.
    """
    )

    # Use LLM to generate cover letter given job ad, CV and reference cover letters
    chain_cover_letter = cover_letter_prompt | llm
    cover_letter = chain_cover_letter.invoke({"job_description": str(job_info), "cv": cv_text})
    
    return cover_letter.content



if __name__ == "__main__":
    llm = ChatGroq(temperature=0, api_key=os.getenv("API_KEY"), model_name="llama-3.1-70b-versatile")
    # inputs
    #job_link = "https://www.google.com/about/careers/applications/jobs/results/105369930748043974-software-engineer-google-cloud-computing-cloud-learning-services?q=%22Software%20Engineer%22"
    #cv_dir = 'resources/cv.pdf'
    # get info
    #job_info = get_job_info(job_link, llm)
    #cv = get_cv(cv_dir)






