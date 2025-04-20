from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, share, user


app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(share.router, prefix="/share", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])