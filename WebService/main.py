import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from scan import Detection
import json

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

# ���������� ����������� �����
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/upload/")
async def upload_files(images: list[UploadFile] = File(...), number: int = Form(...)):
    UPLOAD_DIRECTORY_CODE =UPLOAD_DIRECTORY+ "/"+str(number)
    if not os.path.isdir(UPLOAD_DIRECTORY_CODE):
        os.mkdir(UPLOAD_DIRECTORY_CODE)
    for image in images:    
        image_location = f"{UPLOAD_DIRECTORY_CODE}/{image.filename}"
        with open(image_location, "wb") as image_obj:
            image_obj.write(await image.read())
    Deffect = []
    for filename in os.listdir(UPLOAD_DIRECTORY_CODE):
        dictionary = Detection(filename)
        onDellete = []
        for key, val in dictionary.items():
            if val == []:
                onDellete.append(key)
        for key in onDellete:
            dictionary.pop(key)
        temp ={"src":f"{UPLOAD_DIRECTORY_CODE}/{filename}",
               "defect": dictionary
               }
        Deffect.append(temp)
    return json.dumps(Deffect)

@apt.post("/upload")
async def get_report_info(items: list[Form()]):








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
