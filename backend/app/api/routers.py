from fastapi import APIRouter

from api.endpoints import msg_router, user_msg_router

main_router = APIRouter()

main_router.include_router(msg_router, tags=['Сообщения'])
main_router.include_router(user_msg_router, tags=['Переписка пользователей'])
