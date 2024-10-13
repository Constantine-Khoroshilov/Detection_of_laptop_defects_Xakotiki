import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI, File, UploadFile, Form,Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from scan import Detection
import json
from generate_report import create_report
app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

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
        dictionary = Detection(UPLOAD_DIRECTORY_CODE + '/' + filename)
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

@app.get("/uploads/{folder_number}/{image_name}")
async def get_image(folder_number: str, image_name: str):
    # Формируем путь к изображению
    image_path = os.path.join("uploads", folder_number, image_name)
    
    # Проверяем, существует ли файл
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.post("/report/{id_laptop}")
async def get_report_info(id_laptop :int, json_file: list[dict]=Body(...)):
    create_report(json_file,id_laptop)
    return "/Отчет о ноутбуке №" + str(id_laptop) + ".pdf"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
