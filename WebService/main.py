from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/upload/")
async def upload_files(images: list[UploadFile] = File(...), number: int = Form(...)):
    for image in images:    
        image_location = f"{UPLOAD_DIRECTORY}/{image.filename}"
        with open(image_location, "wb") as image_obj:
            image_obj.write(await image.read())
    
    return {"message": "File uploaded successfully!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
