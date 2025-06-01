import shutil
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    # to open a new file in the binary mode and copy the content 
    # of the uploadfile to that new binary file
    with open (f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename}
    
@app.get("/downloadfile/{filename}", response_class=FileResponse)
async def download_file(filename: str): 
    # to allow files from the /uploads directory to be downloaded
    # FileResponse automatically sets the content-type and hader based on the filetype
    if not Path(f"uploads/{filename}").exists():
        raise HTTPException(status_code = 404, detail = f"file {filename} not found")
    return FileResponse(path=f"uploads/{filename}", filename=filename)
