# auth.py
from fastapi import HTTPException, Header
from clerk import Clerk
import os

clerk = Clerk(os.getenv("CLERK_API_KEY"))

async def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=403, detail="Unauthorized")
    session_id = authorization.split(" ")[1]
    try:
        session = clerk.sessions.verify_session(session_id)
        user_id = session["data"]["user_id"]
        user = clerk.users.get_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=403, detail="Unauthorized")