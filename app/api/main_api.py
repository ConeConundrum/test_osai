from fastapi import APIRouter, status, Request, HTTPException
from pydantic import HttpUrl

from app.components.http_errors import HttpErrorEnum
from app.components.generate_url import generate_short_url, generate_key, get_key_from_short_url
from app.database.crud_operations import get_short_url_db, create_url_db, delete_url_db, get_full_url_db

api_router = APIRouter()


@api_router.post('/', status_code=status.HTTP_201_CREATED, response_model=str)
async def create_short_link(request: Request, original_url: HttpUrl) -> str:
    """Create short link based on full link"""
    db = request.app.state.db

    # check url exist in database
    existed_url = await get_full_url_db(db=db, original_url=original_url)
    if existed_url:
        raise HTTPException(status.HTTP_409_CONFLICT, HttpErrorEnum.URL_CREATED_409)

    # generate key for short url
    key = await generate_key(db=db, original_url=original_url)
    if not key:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, HttpErrorEnum.BAD_KEY_GENERATION_400)
    # generate short url
    short_url = generate_short_url(original_url=original_url, key=key)
    # create record
    created = await create_url_db(
        db=db,
        original_url=original_url,
        short_url=short_url,
        generated_key=key
    )
    if not created:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, HttpErrorEnum.CREATION_ERROR_400)
    return created


@api_router.get('/', status_code=status.HTTP_200_OK, response_model=HttpUrl)
async def get_short_link(request: Request, short_url: str) -> HttpUrl:
    """Get short link based on full link"""
    db = request.app.state.db

    # get key to get data by indexed column
    key = get_key_from_short_url(short_url=short_url)
    if not key:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, HttpErrorEnum.BAD_URL_422)

    url_data = await get_short_url_db(db=db, key=key)
    if not url_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, HttpErrorEnum.URL_NOT_FOUND_404)
    return url_data


@api_router.delete('/', status_code=status.HTTP_200_OK, response_model=str)
async def delete_short_link(request: Request, short_url: str) -> str:
    """Delete short link"""
    db = request.app.state.db
    # get key to get data by indexed column
    key = get_key_from_short_url(short_url=short_url)
    if not key:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, HttpErrorEnum.BAD_URL_422)

    original_url = await delete_url_db(db=db, key=key)
    if not original_url:
        raise HTTPException(status.HTTP_404_NOT_FOUND, HttpErrorEnum.URL_NOT_FOUND_404)
    return 'OK'
