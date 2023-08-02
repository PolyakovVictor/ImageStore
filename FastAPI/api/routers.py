from fastapi import APIRouter

from api.endpoints.board import router_board
from api.endpoints.pin import router_pin

router = APIRouter()

router.include_router(router_board)
router.include_router(router_pin)
