from fastapi import APIRouter, HTTPException, Depends
from Core.database import get_supabase_client
from Utils.sys_validation import RegisterHandle,LoginHandle

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register_user(data: RegisterHandle, supabase=Depends(get_supabase_client)):
    try:
        res = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {
                    "name": data.name
                }
            }
        })

        if res.user is None:
            raise HTTPException(status_code=400, detail="Registration failed")

        return {
            "message": "User registered successfully",
            "user_id": res.user.id,
            "email": res.user.email
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login_user(data: LoginHandle, supabase=Depends(get_supabase_client)):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if res.session is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": res.user.id,
                "email": res.user.email
            }
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password")
