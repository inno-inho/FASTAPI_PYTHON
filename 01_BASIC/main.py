from fastapi import FastAPI, HTTPException, status, Query, Path, Header, Cookie, UploadFile, File, Form, Response, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict

app = FastAPI(title="FastAPI Minimal Step-by-Step")

@app.get("/health") # FastApi의 데코레이터 - 웹 요청(GET, POST...) 처리 핸들러 등록
def health():
    return {"status" : "HelloWorld"}

@app.get("/") 
def root():
    return {"message" : "Fast Api Main EndPoint"}

# ------------------------------------------------------------------------
# 2) Query 파라미터
# Get /echo?name=Alice
# Psotman: GET http://localhost:8000/echo?name=Alice
# ------------------------------------------------------------------------

@app.get("/echo")
def echo(name: str = Query(..., min_length=1, description="이름")):
    return{"hello" : name}



@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., ge=1),     # ...은 필수 파라미터, ge=1이라는거는 크기가 1보다 클 것이라는 뜻
    q: Optional[str] = Query(None, max_length=50)
):
    return {"item_id" : item_id, "q" : q}


# DTO 만들기
class ItemIn(BaseModel):                    # 사용자로부터 전달받는 내용 저장하는 DTO
                                            # BaseModel-> JSON같은 걸로 들어오는 데이터를 파이썬에 맞는 데이터형태로 바꿔주고 유효성 검증도 해주는 데이터바인더
    name : str=Field(..., min_length=1)     # 상품명
    price : float = Field(..., gt=0)        # 상품가격
    tags: List[str] = []                    # 태그
    in_stock : bool = True                  # 재고여부

class ItemOut(BaseModel):                  
                                        
    id : int                                    
    name : str=Field(..., min_length=1)     
    price : float = Field(..., gt=0)        
    tags: List[str] = []                    
    in_stock : bool = True                  


# ID 생성하기

_next_id = 1
def _gen_id() -> int:
    global _next_id
    val = _next_id
    _next_id += 1
    return val

# ':' = type.hint 문법
DB: Dict[int, ItemOut] = {}


@app.post("/items", response_model = ItemOut, status_code = status.HTTP_201_CREATED)
def create_item(payload: ItemIn):
    new_id = _gen_id()
    item = ItemOut(id = new_id, name = payload.name , price = payload.price, tags = payload.tags, in_stock = payload.in_stock)
    DB[new_id] = item
    print("payload", payload)
    return item

