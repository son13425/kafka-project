"""Эндпоинты для работы с сообщениями пользователей."""
from fastapi import APIRouter, HTTPException

from core.config import logger
from schemas.msg_schema import OutgoingMessageSchema
from schemas.user_msg_schema import (IncomingBlockedMessageSchema,
                                     IncominUserMessageSchema)
from kafka_client.producer_plain import get_plain_producer


router = APIRouter()


@router.post(
    '/user-message',
    response_model=OutgoingMessageSchema,
    response_model_exclude_none=True
)
async def set_user_message(
    data_msg: IncominUserMessageSchema
):
    """Получает сообщение пользователя и отправляет его в Kafka."""
    logger.info(
                f'Получено сообщение от пользователя {data_msg.user_id} '
                f'для пользователя {data_msg.recipient_id}'
    )
    producer = get_plain_producer()
    if not producer:
        logger.info("Простой Kafka-продюсер не инициализирован")
        raise HTTPException(
            status_code=500,
            detail="Простой Kafka-продюсер не инициализирован"
        )
    success = producer.send_message(
        key='user_msg',
        topic='messages_topic',
        message=data_msg.model_dump_json()
    )
    if not success:
        logger.info("Ошибка при отправке простого сообщения в Kafka")
        raise HTTPException(
            status_code=500,
            detail="Ошибка при отправке простого сообщения в Kafka"
        )
    return {
        "msg": (f"Сообщение от пользователя {data_msg.user_id} получено "
                f"сервером и отправлено в Kafka")
    }


@router.post(
    '/blocked-message',
    response_model=OutgoingMessageSchema,
    response_model_exclude_none=True
)
async def set_blocked_user(
    data_msg: IncomingBlockedMessageSchema
):
    """
    Получает сообщение о блокировке/разблокировке
    пользователя и отправляет его в Kafka.
    """
    logger.info(
        f'Получено сообщение от пользователя {data_msg.user_id} '
        f'для {data_msg.action} пользователя'
        f'{data_msg.blocked_user_id}'
    )
    producer = get_plain_producer()
    if not producer:
        logger.info("Простой Kafka-продюсер не инициализирован")
        raise HTTPException(
            status_code=500,
            detail="Простой Kafka-продюсер не инициализирован"
        )
    success = producer.send_message(
        key='user_msg',
        topic='blocked_users_topic',
        message=data_msg.model_dump_json()
    )
    if not success:
        logger.info("Ошибка при отправке сообщения о блокировке в Kafka")
        raise HTTPException(
            status_code=500,
            detail="Ошибка при отправке сообщения о блокировке в Kafka"
        )
    return {
        "msg": (f"Сообщение от пользователя {data_msg.user_id} получено "
                f"сервером и отправлено в Kafka")
    }
