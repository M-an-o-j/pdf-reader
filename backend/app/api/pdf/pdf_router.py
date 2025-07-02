from .pdf_controller import *

pdf_router = APIRouter(
    prefix="/pdf",
    tags=["PDF"],
    responses={404: {"description": "Not found"}},
)

@pdf_router.get("/")
async def root():
    return {"message": "Hello World"}