from fastapi import APIRouter, status, Request

api_router = APIRouter()


@api_router.post('/', status_code=status.HTTP_200_OK, response_model=str)
async def create_short_link(request: Request) -> str:
    """Create short link based on full link"""
    db = request.app.state.db
    return 'OK'


@api_router.get('/', status_code=status.HTTP_201_CREATED, response_model=str)
async def get_short_link(request: Request) -> str:
    """Get short link based on full link"""
    db = request.app.state.db
    return 'OK'


@api_router.delete('/', status_code=status.HTTP_200_OK, response_model=str)
async def delete_short_link(request: Request) -> str:
    """Delete short link"""
    db = request.app.state.db
    return 'OK'
