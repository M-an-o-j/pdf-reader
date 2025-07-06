from fastapi import FastAPI, File, UploadFile, HTTPException, Response, Form, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

import os
import uuid
import hashlib
import json
import requests
from pathlib import Path
import pdfplumber as pp
from typing import List, Dict, Optional
import tempfile
import shutil
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Reader API", 
    version="1.0.0",
    description="API for reading PDF files"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)