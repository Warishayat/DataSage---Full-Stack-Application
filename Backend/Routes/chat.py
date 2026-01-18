import os
from fastapi import APIRouter, UploadFile, File, Depends
from Utils.Security import get_current_user

from Langgraph.chat_graph import (
    get_csv_metadata,
    load_data,
    preprocess_data,
    load_embeddings,
    create_vectorstore,
    build_csv_chat_graph,
    llm
)

chat_router = APIRouter(prefix="/csv-chat", tags=["CSV Chat"])

#a active chat only 
ACTIVE_CHAT_CSV = {}

@chat_router.post("/upload")
async def upload_csv_for_chat(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    user_id = str(user.id)
    temp_path = f"/tmp/chat_{user_id}.csv"

    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    metadata = get_csv_metadata(temp_path)
    raw_data = load_data(temp_path)
    docs = preprocess_data(raw_data)

    embeddings = load_embeddings()
    vectorstore = create_vectorstore(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    graph = build_csv_chat_graph(retriever, metadata, llm)

    ACTIVE_CHAT_CSV[user_id] = graph

    return {"message": "CSV uploaded. You can now chat with it."}


@chat_router.post("/chat")
async def chat_with_csv(
    question: str,
    user = Depends(get_current_user)
):
    user_id = str(user.id)

    if user_id not in ACTIVE_CHAT_CSV:
        return {"error": "Upload a CSV first"}

    graph = ACTIVE_CHAT_CSV[user_id]

    result = graph.invoke({"question": question})
    return {"answer": result["answer"]}
