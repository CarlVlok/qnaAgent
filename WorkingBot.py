from langchain_community.document_loaders import PyPDFLoader
from docx import Document
import pandas as pd
import os
import openai

openapi = os.environ['OPENAI_API_KEY']

def pdfLoader():
    folder_path = "data/pdf/"
    names =os.listdir(folder_path)
    # print(names)
    loader = []
    all_pages = []
    for f in names:
        loader = PyPDFLoader(folder_path+f)
        pages = loader.load_and_split()
        #print((len(pages)))
        for p in pages:
            all_pages.append(p)
    return all_pages

def wordFolder():
    folder_path = "data/worddoc/"
    all_text = []
    names=os.listdir(folder_path)
    for name in names:
        # print(name)
        doc = Document(folder_path+name)
        for p in doc.paragraphs:
            all_text.append(p.text)
    return all_text

def excelFolder():
    folder_path = "data/excel/"
    all_text = []
    names = os.listdir(folder_path)
    # print(names)
    for name in names:
        excel_data = pd.read_excel(folder_path+name, sheet_name=None)
        all_text.append(excel_data)
    return all_text


pdfs = pdfLoader()
text = wordFolder()
excel = excelFolder()

content = pdfLoader()+wordFolder()+excelFolder()


# query = input("Ask the agent a question: ")

# context = f"""Use the below information to answer a query from the user:
# Infromation:
# {content}

# Query: "{query}
# """
def agent(query, context):
    client = openai
    response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about documents and text given to you'},
        {'role': 'user', 'content': context},
    ],
    model='gpt-4o',
    temperature=0.7,
    )
    return response.choices[0].message.content

chatChain = []

while True:
    query = input('Ask the agent a question | Exit: ')
    if query.lower() == 'exit':
        break
    context = f"""Use the below information to answer a query from the user, also use previous responses as context:
    Infromation:
    {content}{chatChain}

    Query: "{query}
    """
    response = agent(query, context)
    print(response)
    chatChain.append(response)



