# # main.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# from src.chat.chat_service import get_response
# from src.config.config import config
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn

# class QueryRequest(BaseModel):
#     query: str

# class QueryResponse(BaseModel):
#     reply: str

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/chat/query", response_model=QueryResponse)
# async def chat_query(request: QueryRequest):
#     try:
#         reply = get_response(request.query)
#         return QueryResponse(reply=reply)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
