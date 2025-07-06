from .pdf_controller import *

pdf_router = APIRouter(
    prefix="/pdf",
    tags=["PDF"],
    responses={404: {"description": "Not found"}},
)

@pdf_router.post("/upload")
async def upload_pdf_router(file: UploadFile = File(...)):
    return await upload_pdf_controller(file)

@pdf_router.get("/pdf/{file_id}/text")
async def get_page_text(file_id: str, page: int = 1):
    return await get_page_text_controller(file_id, page)