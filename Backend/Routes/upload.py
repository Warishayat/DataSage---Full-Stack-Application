from fastapi import APIRouter, UploadFile, File, Depends,HTTPException
import uuid, os
from Core.database import get_supabase
from Utils.Security import get_current_user
from Langgraph.graph import Analysis_graph
from Langgraph.states import DataState
from Utils.sys_validation import sanitize

upload_router = APIRouter(
    prefix="/upload",
    tags=["CSV Charts and Dashbaord Insights."]
)

@upload_router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    user = Depends(get_current_user) 
):
    try:
        supabase = get_supabase()
        user_id = user.id

        file_id = str(uuid.uuid4())
        storage_path = f"{user_id}/{file_id}.csv"

        content = await file.read()

        #uploadstorage
        supabase.storage.from_("csv-files").upload(
            storage_path,
            content,
            {"content-type": "text/csv"}
        )

        #Metadata
        supabase.table("files").insert({
            "user_id": user_id,
            "file_name": file.filename,
            "storage_path": storage_path
        }).execute()

        #tempfile
        temp_path = f"/tmp/{file_id}.csv"
        with open(temp_path, "wb") as f:
            f.write(content)

        initial_state: DataState = {
            "file_path": temp_path,
            "df": None,
            "metadata": None,
            "eda": None,
            "charts": None,
            "insights": None,
            "report": None,
        }

        result = Analysis_graph.invoke(initial_state,config={"configurable":{"user_id":str(user_id)}})
        safe_result = {
        "metadata": result.get("metadata"),
        "eda": result.get("eda"),
        "charts": result.get("charts"),
        "insights": result.get("insights"),
        "report": result.get("report"),
        }
        result = sanitize(safe_result)
        return {
            "message": "CSV processed successfully",
            "result": safe_result
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internel Server Error")