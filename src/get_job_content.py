from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

class Job_info:
    def __init__(self, llm):
        # get LLM
        self.llm = llm
        # prompt template for LLM to extract job specific info
        self.prompt_job_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: 'role', 'experience', 'skills' and 'description'.
        Only return the valid JSON. 
        Also only take the job (prominant) that has most information on 'role', 'experience', 'skills' and 'description' for the final json.

        ### VALID JSON (NO PREAMBLE):    
        """
        )

    def get_job(self, job_link):
        ''' scrape job info from website'''
        loader = WebBaseLoader(job_link)
        page_data = loader.load().pop().page_content 
        
        # clean scraped data
        #page_data = clean_data(page_data)
        
        # Get LLM response given the prompt with job page data 
        chain_extract = self.prompt_job_extract | self.llm 
        response = chain_extract.invoke(input={'page_data':page_data})
        #print(response.content)

        # Get json parser for job info
        try:
            json_parser = JsonOutputParser()
            job_info = json_parser.parse(response.content)
        except:
            raise OutputParserException("Context is too large, unable to parse.")
        
        return job_info if isinstance(job_info, list) else [job_info]
    

if __name__ == "__main__":
    llm = ChatGroq(temperature=0, api_key=os.getenv("API_KEY"), model_name="llama-3.1-70b-versatile")
    job_link = "https://www.google.com/about/careers/applications/jobs/results/105369930748043974-software-engineer-google-cloud-computing-cloud-learning-services?q=%22Software%20Engineer%22"
    job_info = Job_info(llm)
    job_info_response = job_info.get_job(job_link=job_link)