from fastapi import APIRouter

from api.endpoints.board import router_board
from api.endpoints.pin import router_pin
from api.endpoints.tag import router_tag

router = APIRouter()

router.include_router(router_board)
router.include_router(router_pin)
router.include_router(router_tag)
