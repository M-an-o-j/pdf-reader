from .pdf_service import*

async def upload_pdf_controller(*args):

    file, = args

    # Validate file type
    error_handler(400, "No filename provided") if not file.filename else None
    
    error_handler(400, "Only PDF files are allowed") if not file.filename.lower().endswith('.pdf') else None

    error_handler(400, "File too large. Maximum size is 50MB") if file.size and file.size > 50 * 1024 * 1024 else None

    return await upload_pdf_service(file)

async def get_page_text_controller(*args):

    file_id, page = args
    error_handler(404, "File not found") if file_id not in file_metadata else None
    
    metadata = file_metadata[file_id]
    error_handler(400, f"Invalid page number. Must be between 1 and {metadata['page_count']}") if page < 1 or page > metadata["page_count"] else None
    
    file_path = Path(metadata["file_path"])
    error_handler(404, "PDF file not found on disk") if not file_path.exists() else None

    return await get_page_text_service(file_path,file_id, page, metadata)