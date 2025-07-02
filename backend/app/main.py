from configuration.config import app
# from api.example.example_router import *
import uvicorn
from api.pdf.pdf_router import pdf_router

app.include_router(pdf_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost",port=5001, reload=True)