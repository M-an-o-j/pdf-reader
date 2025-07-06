from configuration.config import APIRouter, app, UploadFile, File, pp, Dict, Path, uuid, logger
from utils.handler import error_handler


# Store file metadata (in production, use a database)
file_metadata: Dict[str, Dict] = {}

# Create directories
UPLOAD_DIR = Path("uploads")
AUDIO_CACHE_DIR = Path("audio_cache")
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_CACHE_DIR.mkdir(exist_ok=True)

async def upload_pdf_service(file):

    # Generate unique file ID
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract page count and basic info
        with pp.open(file_path) as pdf:
            page_count = len(pdf.pages)
        
        # Store metadata
        file_metadata[file_id] = {
            "filename": file.filename,
            "page_count": page_count,
            "file_path": str(file_path),
            "file_size": len(content)
        }
        
        logger.info(f"Successfully uploaded file: {file.filename} with ID: {file_id}")
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "page_count": page_count,
            "file_size": len(content)
        }
    except Exception as e:
        # Clean up on error
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup file {file_path}: {cleanup_error}")
        
        logger.error(f"Error processing PDF {file.filename}: {str(e)}")
        error_handler(500, "Error processing PDF", str(e))

async def get_page_text_service(file_path, file_id, page, metadata):
    try:
        with pp.open(file_path) as pdf:
            page_obj = pdf.pages[page - 1]  # 0-indexed
            
            # Extract text
            text = page_obj.extract_text() or ""
            
            # Extract words with positions
            words = []
            try:
                word_blocks = page_obj.extract_words()
                
                for word_info in word_blocks:
                    word_text = word_info.get('text', '').strip()
                    if word_text:  # Only non-empty words
                        words.append({
                            "text": word_text,
                            "bbox": [
                                round(word_info.get('x0', 0), 2),
                                round(word_info.get('top', 0), 2),
                                round(word_info.get('x1', 0), 2),
                                round(word_info.get('bottom', 0), 2)
                            ]
                        })
            except Exception as word_error:
                logger.warning(f"Failed to extract word positions for page {page}: {word_error}")
                # Continue without word positions
        
        return {
            "text": text,
            "words": words,
            "page_count": metadata["page_count"],
            "current_page": page,
            "filename": metadata["filename"]
        }
    except Exception as e:
        logger.error(f"Error extracting text from {file_id} page {page}: {str(e)}")
        error_handler(500, f"Error extracting text : {str(e)}")