from fastapi import APIRouter

from api.endpoints.board import router_board
from api.endpoints.pin import router_pin
from api.endpoints.tag import router_tag
from api.endpoints.image import router_image

router = APIRouter()

router.include_router(router_board)
router.include_router(router_pin)
router.include_router(router_tag)
router.include_router(router_image)
