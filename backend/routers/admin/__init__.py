# routers/admin.py
import base64
from fastapi import APIRouter, Depends, UploadFile
from utils.auth import oauth2_scheme, is_admin, get_current_user
from typing import List

from .analytics import get_analytics
from .upload import upload_to_db, copy_files_if_exist, get_list_of_selected_docs, get_list_of_all_docs
from .ingest import ingest
from .sendbulk import send_mails

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@router.get("/")
async def check():
    return {"message": "Admin Endpoint"}


@router.get("/analytics")
async def analytics(_: str = Depends(is_admin)):
    return get_analytics()


@router.post("/upload_pdf")
async def upload_pdf(pdf_file: UploadFile, _: str = Depends(is_admin)):
    return upload_to_db(pdf_file)

@router.post("/update_selected_docs")
async def selected_document_list(filenames: List[str], _: str = Depends(is_admin)):
    copy_files_if_exist(filenames)

# ingest the pdfs
@router.post("/ingest")
async def ingest_pdfs(
    current_user: dict = Depends(get_current_user), _: str = Depends(is_admin)
):
    await ingest(current_user)
    return {"message": "Ingested", "status": "Done"}


@router.get("/generate_proposal")
async def generate_proposal(
    current_user: dict = Depends(get_current_user), _: str = Depends(is_admin)
):
    generate_proposal(current_user)
    pass

@router.get("/get_selected_docs")
async def get_selected_docs(_: str = Depends(is_admin)):
    return get_list_of_selected_docs()

@router.get("/get_all_docs")
async def get_all_docs(_: str = Depends(is_admin)):
    return get_list_of_all_docs()

@router.post("/send_bulk_email")
async def send_bulk_email(
    template:str,
    email_list: List[str], _: str = Depends(is_admin)
):
    send_mails(template,email_list)

