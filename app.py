import utils
import streamlit as st
import streamlit_ext as ste
import os
import openai
import json
import asyncio
from llama_index import SimpleDirectoryReader
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv
from doc_utils import extract_text_from_upload
from templates import generate_latex, template_commands
from prompt_engineering import generate_json_resume, tailor_resume
from render import render_latex
from livecareerData.scraper import livecareerResumeUtill
from prompt.prompt import roles_extraction_qa, cv_prompt
from data_retrieval.database_loader import ChatBotManager
from dask import delayed, compute


def open_ai_key():
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        os.environ["OPENAI_API_KEY"] = openai_api_key

def init_page() -> None:
    st.set_page_config(
    )
    st.sidebar.title("Options")
    icon, title = st.columns([3, 20])
    with icon:
        st.image('./resume.png')
    with title:
        st.title('Generate A Resume')
        
        
async def get_rfp():
        rfp_docs = st.file_uploader(
            label="##### Here, upload your RFP document",
            key="rfp_docs_uploader"  # Unique key for this file uploader

        )
        return rfp_docs
    
@st.cache_data(ttl="2h")      
def request_files(rfp_docs) -> None:
    import tempfile
    from utils.utility import rerank
    
    rfp_docs_uploaded = False
    if rfp_docs:
        rfp_docs_uploaded = True
        with tempfile.NamedTemporaryFile(delete=False) as tpfile:
            tpfile.write(rfp_docs.getvalue())
            st.session_state['rfpfile'] = tpfile.name

        # Get the directory of the first org document.
    if rfp_docs_uploaded:
        with st.spinner("Loading Files"):
            rfpfile = st.session_state.get('rfpfile')
    else:
        if not rfp_docs_uploaded:
            st.warning("Please upload your RFP document.")
        st.stop()
        
    chatbot = ChatBotManager(rerank)
    document =  chatbot.get_docs(path=rfpfile)
    query_engine = chatbot.get_query_engine(document)
    print('Extracting Resume Qualification')
    resume_qualification = chatbot.parallel_process_inputs(roles_extraction_qa, query_engine)
    st.session_state['resume_qualification'] = resume_qualification
    # st.session_state['chatbot'] = chatbot
    # st.session_state['qa'] = qa
    
    return resume_qualification
    
@st.cache_data(ttl="2h")    
def clean_text(text):
    data = json.loads(text)
    st.session_state['json_resume_qualification'] = data
    job_titles = [ job_title.replace("/"," ") for job_title in list(data.keys())]
    job_titles.sort()
    tasks = [delayed(livecareerResumeUtill(role).fetch)() for role in job_titles]
    results = compute(*tasks, scheduler='threads')
    parent_folder = os.path.join(os.getcwd(), "resume")
    return job_titles, parent_folder

@st.cache_data(ttl="2h")    
def qa(parent_folder, job_titles):
    print(job_titles)
    from utils.utility import rerank
    qa_dict = {}
    role_dict = {}
    for index, dir in tqdm(enumerate(os.listdir(parent_folder)), bar_format="{l_bar}{bar}{r_bar}"):
        directory = os.path.join(parent_folder, dir)
        reader = SimpleDirectoryReader(input_dir=directory, recursive=True)
        docs = reader.load_data()
        chatbot = ChatBotManager(rerank)
        query_engine = chatbot.get_query_engine(docs)
        print(job_titles[index])
        qa_dict[job_titles[index]] = query_engine
    json_resume_qualification = st.session_state.get('json_resume_qualification')
    separate_dicts = [{key: value} for key, value in json_resume_qualification.items()]
    separate_dicts.sort(key=lambda x: list(x.keys())[0])

    for index, role in tqdm(enumerate(separate_dicts), desc="Loading"):
        print(role, "------------------------------",job_titles[index])
        result = chatbot.parallel_process_inputs(cv_prompt.format(role), qa_dict[job_titles[index]])
        role_dict[job_titles[index]] = result
    
    return role_dict

def generate_resume_structure(role_dict):
    
    template_options = list(template_commands.keys())

    chosen_option = st.selectbox(
            "Select a template to use for your resume [(see templates)](/Template_Gallery)",
            template_options,
            index=0,  # default to the first option
        )

    section_ordering = st.multiselect(
            "Optional: which section ordering would you like to use?",
            ["education", "work", "skills", "projects", "awards"],
            ["education", "work", "skills", "projects", "awards"],
        )
    
    improve_check = st.checkbox("I want to improve the resume with LLMs", value=True)
    generate_button = st.button("Generate Resume")
    
    if generate_button:
        try:
            if improve_check:
                with st.spinner("Tailoring the resume"):
                    text = tailor_resume(role_dict['Project Software Manager'].response)

            json_resume = generate_json_resume(role_dict['Project Software Manager'].response)
            latex_resume = generate_latex(chosen_option, json_resume, section_ordering)
            resume_bytes = render_latex(template_commands[chosen_option], latex_resume)
            
            col1, col2, col3 = st.columns(3)

            try:
                with col1:
                    btn = ste.download_button(
                        label="Download PDF",
                        data=resume_bytes,
                        file_name="resume.pdf",
                        mime="application/pdf",
                    )
            except Exception as e:
                st.write(e)

            with col2:
                ste.download_button(
                    label="Download LaTeX Source",
                    data=latex_resume,
                    file_name="resume.tex",
                    mime="application/x-tex",
                )

            with col3:
                ste.download_button(
                    label="Download JSON Source",
                    data=json.dumps(json_resume, indent=4),
                    file_name="resume.json",
                    mime="text/json",
                )
        except openai.RateLimitError as e:
            st.markdown(
                "It looks like you do not have OpenAI API credits left. Check [OpenAI's usage webpage for more information](https://platform.openai.com/account/usage)"
            )
            st.write(e)
        except Exception as e:
            st.error("An error occurred while generating the resume. Please try again.")
            st.write(e)
    else:
        st.info("Please upload a file to get started.")
            

def main():
    # Load the OpenAI API key from the environment variable
    _ = load_dotenv(find_dotenv())
    # print(os.getenv("OPENAI_API_KEY"))

    init_page()
    open_ai_key()
    rfp_docs = asyncio.run(get_rfp())

    resume_qualification = request_files(rfp_docs)
    job_titles, parent_folder = clean_text(resume_qualification.response)
    role_dict = qa(parent_folder, job_titles)
    generate_resume_structure(role_dict)
    
if __name__ == "__main__":
    main()
    
    