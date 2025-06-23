from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import fitz

router = APIRouter(prefix="/test")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



@router.get("/items/{id}")
async def test_get_param(id: int):
    return {"items" : id}


@router.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    print(file.content_type)
    if not file.filename.endswith(".pdf"):
        return {"error" : "file was not a pdf"}
    
    
    content = await file.read()

    # open byte stream using fitz
    doc = fitz.open(stream=content, filetype="pdf")


    text = ""
    for page in doc:
        text += page.get_text()

    print(text)
    # return content
    return {"hi":"hello"}
