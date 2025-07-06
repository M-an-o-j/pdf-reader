from configuration.config import HTTPException

def error_handler(status_code, message):
    return HTTPException(status_code=status_code, detail=message)