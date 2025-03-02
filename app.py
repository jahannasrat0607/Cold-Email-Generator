import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utility import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    st.title("🚀 Cold Email Generator")
    st.subheader("Generate personalized cold emails for job opportunities")
    
    with st.sidebar:
        st.header("🔗 Job Advertisement Links")
        urls = st.text_area("Enter job advertisement links (one per line)")
    
    st.markdown("### Example Job Advertisement Link")
    st.write("You can use the following example link for reference:")
    st.code('https://careers.nike.com/senior-software-engineer-full-stack-itc/job/R-46165', language='markdown')
    
    st.markdown("**Click the button below to generate cold emails based on the provided job advertisement links.**")
    submit_button = st.button("Generate Cold Emails ✉️")
    
    if submit_button:
        st.write("### Generated Emails:")
        links = urls.split("\n") if urls else []
        
        for url in links:
            url = url.strip()
            if url:
                try:
                    loader = WebBaseLoader([url])
                    data = clean_text(loader.load().pop().page_content)
                    portfolio.load_portfolio()
                    jobs = llm.extract_jobs(data)
                    
                    if not jobs:
                        st.warning(f"No valid job descriptions extracted from {url}. Please check the job link.")
                        continue
                    
                    # Select only the first relevant job to avoid mismatches
                    job = jobs[0] 
                    skills = job.get('skills', [])
                    relevant_links = [meta['links'] for meta in portfolio.query_links(skills) if 'links' in meta]  # Extract only links
                    relevant_links = list(set(relevant_links))[:2]  # Ensure unique links, limit to 2
                    email = llm.write_mail(job, relevant_links)
                    email = '\n\n'.join(email.split('. '))  # Format email for better readability
                    
                    st.markdown("---")
                    st.code(email, language='markdown')
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)