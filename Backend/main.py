from fastapi import FastAPI
from Routes.auth import router
from Routes.upload import upload_router
from Routes.chat import chat_router
from Routes.contact import contact_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DataSage",description="User will pass csv and we will prove him/her detail insights.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def welcome():
    return{
        "status":200,
        "message" : "App is up"
    }

app.include_router(router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(contact_router)