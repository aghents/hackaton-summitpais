import os
from typing import Union

from asyncpg import Connection
from crud import get_session, get_transcripcion
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, WebSocket
from langchain.chains import LLMChain, RetrievalQA
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from pydantic import BaseModel

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY") or ""
API_BASE = os.getenv("OPENAI_API_BASE") or ""
API_TYPE = os.getenv("OPENAI_API_TYPE") or ""
API_VERSION = os.getenv("OPENAI_API_VERSION") or ""

DB_NAME = os.getenv("DB_NAME") or ""
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or ""

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class Question(BaseModel):
    query: str


@app.get("/summary/resumen/{id}")
async def generar_resumen(id: str, conn: Connection = Depends(get_session)):
    transcripcion, descripcion = await get_transcripcion(id, conn)
    # Load the summary.txt

    model = AzureChatOpenAI(
        openai_api_base=API_BASE,
        openai_api_version=API_VERSION,
        deployment_name="capibarai_chat35_16k",
        openai_api_key=API_KEY,
        openai_api_type="azure",
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(
        f"Este es un video con los siguientes datos. Descripcion: {descripcion} Contenido: {transcripcion}"
    )

    human_template = "{input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=model, prompt=chat_prompt)
    response = chain.run("Generame un resumen de los contenido vistos en el video.")
    return {"answer": response}


@app.get("/summary/palabras/{id}")
async def palabras_clave(id: str, conn: Connection = Depends(get_session)):
    transcripcion, descripcion = await get_transcripcion(id, conn)
    # Load the summary.txt

    model = AzureChatOpenAI(
        openai_api_base=API_BASE,
        openai_api_version=API_VERSION,
        deployment_name="capibarai_chat35_16k",
        openai_api_key=API_KEY,
        openai_api_type="azure",
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(
        f"Este es un video con los siguientes datos. Descripcion: {descripcion} Contenido: {transcripcion}"
    )

    human_template = "{input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=model, prompt=chat_prompt)
    response = chain.run(
        "Dame un listado de palabras clave del video separadas por espacio y entre comillas"
    )
    return {"answer": response}


@app.post("/summary/{id}")
async def ask_question(
    question: Question, id: str, conn: Connection = Depends(get_session)
):
    transcripcion, descripcion = await get_transcripcion(id, conn)
    # Load the summary.txt

    model = AzureChatOpenAI(
        openai_api_base=API_BASE,
        openai_api_version=API_VERSION,
        deployment_name="capibarai_chat35_16k",
        openai_api_key=API_KEY,
        openai_api_type="azure",
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(
        f"Este es un video con los siguientes datos. Descripcion: {descripcion} Contenido: {transcripcion}"
    )

    human_template = "{input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=model, prompt=chat_prompt)
    response = chain.run(question.query)
    return {"answer": response}


# Iniciamos un websocket para que exista una "conversacion" con el usuario
@app.websocket("/summary/{id}/ws")
async def websocket_endpoint(
    websocket: WebSocket, id: str, conn: Connection = Depends(get_session)
):
    # Aceptamos la conexion
    await websocket.accept()
    # Buscamos la transcripcion del video y la descripcion a partir del id
    transcripcion, descripcion = await get_transcripcion(id, conn)
    # Load the summary.txt

    # Instanciamos el modelo de chat
    model = AzureChatOpenAI(
        openai_api_base=API_BASE,
        openai_api_version=API_VERSION,
        deployment_name="capibarai_chat35_16k",
        openai_api_key=API_KEY,
        openai_api_type="azure",
    )

    # Generamos un retriver para buscar en la base de datos (Chroma) que contiene los
    # embeddings de la transcripcion de nuestro video
    doc = Document(
        page_content=f"Descripcion: {descripcion}. Contenido: {transcripcion}",
        metadata={"source": "local"},
    )
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents([doc])

    # Usamos el model de embeddings capibarai_emb
    embeddings = OpenAIEmbeddings(
        deployment="capibarai_emb",
        model="text-embedding-ada-002",
        openai_api_base=API_BASE,
        openai_api_type="azure",
    )

    # Generamos la DB valida solo por el tiempo de la conversacion
    db = Chroma.from_documents(texts, embeddings)

    retriever = db.as_retriever()

    qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever)
    while True:
        data = await websocket.receive_text()
        print("Ejecutando pregunta:...")
        result = qa.run(data)
        print(result)
        await websocket.send_text(f"{result}")
