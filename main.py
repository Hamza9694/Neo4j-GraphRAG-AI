import streamlit as st
from PyPDF2 import PdfReader
from neo4j import GraphDatabase

# Neo4j database connection details
NEO4J_URI = ""
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = ""

# Function to initialize Neo4j driver
def init_neo4j_driver(uri, user, password):
    print("Initializing Neo4j driver...")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    print("Neo4j driver initialized.")
    return driver

# Function to upload PDF content to Neo4j
def upload_pdf_to_neo4j(file_content, file_name, driver):
    print("Uploading PDF to Neo4j...")
    with driver.session() as session:
        session.write_transaction(create_pdf_node, file_content, file_name)
    print("PDF uploaded to Neo4j.")

# Cypher query to create a PDF node in Neo4j
def create_pdf_node(tx, content, file_name):
    print(f"Creating node for file: {file_name}")
    tx.run("CREATE (p:PDF {name: $name, content: $content})", name=file_name, content=content)
    print(f"Node created for file: {file_name}")

# Streamlit app
def main():
    st.title("PDF Upload to Neo4j")
    print("Starting Streamlit app...")
    driver = init_neo4j_driver(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        try:
            print(f"File uploaded: {uploaded_file.name}")
            pdf_reader = PdfReader(uploaded_file)
            pdf_content = ""
            for page_num, page in enumerate(pdf_reader.pages):
                pdf_content += page.extract_text()
                print(f"Extracted text from page {page_num}")
            
            file_name = uploaded_file.name
            upload_pdf_to_neo4j(pdf_content, file_name, driver)
            
            st.success(f"File '{file_name}' uploaded to Neo4j successfully!")
        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
