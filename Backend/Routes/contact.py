from fastapi import FastAPI,HTTPException,Depends,APIRouter
from Core.database import get_supabase_client
from Utils.sys_validation import ChatwithusValidation

contact_router = APIRouter(prefix="/contact",
                        tags=['Contact with admin in case of queries or Hiring me for project'])

@contact_router.post("/send")
def chatwithus(payload:ChatwithusValidation,supabase = Depends(get_supabase_client)):
    try:
        response = supabase.table("ChatUs").insert({
        "name": payload.name,
        "email": payload.email,
        "topic": payload.topic,
        "message": payload.message
        }).execute()
        if not response.data:
            raise HTTPException(
                status_code=400,
                detail="Message could not be sent"
            )

        return {
            "message": "Your message has been delivered successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internel Server Down/Error")