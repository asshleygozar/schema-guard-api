import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, URLSafeTimedSerializer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database_session import get_session
from app.models.user import User, UserSession
from app.util.hash_token import hash_token

authRouter = APIRouter()

signer = URLSafeTimedSerializer(settings.SESSION_SECRET)
SESSION_DAYS = 7


@authRouter.get("/github/login")
def github_login():
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)

    challenge = (
        base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode()).digest()
        ).rstrip(b"=").decode()
    )

    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.github_callback_url,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    url = "https://github.com/login/oauth/authorize?"
    response = RedirectResponse(url + urlencode(params))

    response.set_cookie(
        key="oauth_flow",
        value=signer.dumps({"state": state, "verifier": verifier}),
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        max_age=600,
        path="/api/v1/auth",
    )
    return response

@authRouter.get("/github/callback")
def github_callback(
    code: str,
    state: str,
    oauth_flow: str | None = Cookie(default=None),
    db: Session = Depends(get_session),
):
    if not oauth_flow:
        raise HTTPException(400, "Missing OAuth session")

    try:
        flow = signer.loads(oauth_flow, max_age=600)
    except BadSignature:
        raise HTTPException(400, "Invalid or expired OAuth session")

    if not secrets.compare_digest(flow["state"], state):
        raise HTTPException(400, "OAuth state mismatch")

    with httpx.Client(timeout=10.0) as client:
        token_response = client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.github_callback_url,
                "code_verifier": flow["verifier"],
            },
        )
        token_response.raise_for_status()
        token_data = token_response.json()

        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(400, "GitHub authorization failed")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        }

        profile_response = client.get(
            "https://api.github.com/user",
            headers=headers,
        )
        profile_response.raise_for_status()
        profile = profile_response.json()

    user = db.scalar(
        select(User).where(User.github_user_id == profile["id"])
    )

    if user is None:
        user = User(
            github_user_id=profile["id"],
            github_username=profile["login"],
            avatar_url=profile.get("avatar_url"),
        )
        db.add(user)
    else:
        user.github_username = profile["login"]
        user.avatar_url = profile.get("avatar_url")

    db.commit()
    db.refresh(user)

    session_token = secrets.token_urlsafe(32)
    db_session = UserSession(
        user_id=user.id,
        token_hash=hash_token(session_token),
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=SESSION_DAYS),
    )
    db.add(db_session)
    db.commit()

    response = RedirectResponse(
        url=f"{settings.FRONTEND_ORIGIN}/dashboard", status_code=303
    )
    response.delete_cookie("oauth_flow", path="/api/v1/auth")
    response.set_cookie(
        key="schema_guard_session",
        value=session_token,
        httponly=True,
        secure=settings.is_production,
        samesite="none" if settings.is_production else "lax",
        max_age=SESSION_DAYS * 86400,
        path="/",
    )
    return response

def get_current_user(
    schema_guard_session: str | None = Cookie(default=None),
    db: Session = Depends(get_session),
) -> User:
    if not schema_guard_session:
        raise HTTPException(401, "Not authenticated")

    record = db.scalar(
        select(UserSession).where(
            UserSession.token_hash
            == hash_token(schema_guard_session)
        )
    )

    if not record:
        raise HTTPException(401, "Invalid session")

    expires = record.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if expires <= datetime.now(timezone.utc):
        raise HTTPException(401, "Session expired")

    user = db.get(User, record.user_id)
    if not user:
        raise HTTPException(401, "User not found")

    return user


@authRouter.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "github_id": user.github_user_id,
        "username": user.github_username,
        "avatar_url": user.avatar_url,
    }


@authRouter.post("/logout")
def logout(
    schema_guard_session: str | None = Cookie(default=None),
    db: Session = Depends(get_session),
):
    if schema_guard_session:
        record = db.scalar(
            select(UserSession).where(
                UserSession.token_hash
                == hash_token(schema_guard_session)
            )
        )
        if record:
            db.delete(record)
            db.commit()

    from fastapi.responses import JSONResponse

    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("schema_guard_session", path="/")
    return response