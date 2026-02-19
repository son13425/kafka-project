"""Приложение Faust."""
import os
import logging
import faust
from dotenv import load_dotenv


# Загружаем переменные окружения
load_dotenv('.env.streams')


# Получаем настройки из переменных окружения
kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()


log_level = getattr(logging, log_level)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Конфигурация Faust-приложения
app = faust.App(
    "message-processing-app",
    broker=kafka_bootstrap_servers,
    value_serializer="raw",  # Работа с байтами (default: "json")
)


class MessageModel(faust.Record):
    """Модель сообщения."""
    user_id: str
    recipient_id: str
    timestamp: str
    message: str


class MessageBlockedModel(faust.Record):
    """Модель сообщения о изменении списка заблокированных пользователей."""
    user_id: str
    blocked_user_id: str
    timestamp: str
    action: str


# Определение топиков для входных данных
messages_topic = app.topic(
    "messages_topic",
    key_type=str,
    value_type=MessageModel
)


blocked_users_topic = app.topic(
    "blocked_users_topic",
    key_type=str,
    value_type=MessageBlockedModel
)


# Определение топика для выходных данных
filtered_messages_topic = app.topic(
    "filtered_messages_topic",
    key_type=str,
    value_type=MessageModel
)


# Таблица для хранения заблокированых пользователей и запрещенных слов
blocked_user_table = app.Table(
    'blocked_user_table',
    default=lambda: [],
    partitions=1
)


@app.agent(blocked_users_topic)
async def process_blocked_users(stream):
    """
    Добавляет/удаляет пользователей в список заблокированных,
    добавляет/удаляет запрещенные слова по ключу forbidden_words.
    """
    async for value in stream:
        list_id = set(blocked_user_table[value.user_id])
        if value.action == 'blocked':
            if value.user_id == 'forbidden_words':
                logger.info('Получено сообщение о внесение слова '
                            '%s в список запрещенных', value.blocked_user_id)
            else:
                logger.info('Получено сообщение о блокировке пользователя '
                            '%s для пользователя %d',
                            value.blocked_user_id, value.user_id)
            list_id.add(value.blocked_user_id)
        else:
            if value.user_id == 'forbidden_words':
                logger.info('Получено сообщение о удалении слова '
                            '%s из списка запрещенных', value.blocked_user_id)
            else:
                logger.info('Получено сообщение о разблокировке пользователя '
                            '%s для пользователя %d',
                            value.blocked_user_id, value.user_id)
            list_id.pop(value.blocked_user_id)
        blocked_user_table[value.user_id] = list(list_id)
        if value.action == 'blocked':
            if value.user_id == 'forbidden_words':
                logger.info('Слово %s добавлено в список запрещенных',
                            value.blocked_user_id)
            else:
                logger.info('Пользователь %s заблокирован для пользователя %d',
                            value.blocked_user_id, value.user_id)
        else:
            if value.user_id == 'forbidden_words':
                logger.info('Слово %s удалено из списка запрещенных',
                            value.blocked_user_id)
            else:
                logger.info(
                    'Пользователь %s разблокирован для пользователя %d',
                    value.blocked_user_id,
                    value.user_id
                )


@app.agent(messages_topic)
async def process_filtered_messages(stream):
    """
    Фильтрует входящие сообщения от заблокированых пользователей
    и удаляет запрещенные слова.
    """
    async for value in stream:
        logger.info(
            'Получено сообщение от пользователя %s для пользователя %d',
            value.user_id,
            value.recipient_id
        )
        if value.user_id in blocked_user_table[value.recipient_id]:
            logger.info('Пользователь %s заблокирован для пользователя %d.'
                        'Сообщение отброшено',
                        value.user_id,
                        value.recipient_id)
            continue
        forbidden_words = blocked_user_table['forbidden_words']
        if forbidden_words and value.message:
            message_text = value.message
            for forbidden_word in forbidden_words:
                message_text = message_text.replace(forbidden_word, '')
            message_text = ' '.join(message_text.split())
            value.message = message_text
            logger.info('Сообщение от пользователя %s для пользователя %d '
                        'очищено от запрещенных слов', value.user_id,
                        value.recipient_id)
        await filtered_messages_topic.send(value=value)
        logger.info('Сообщение от пользователя %s для пользователя %d '
                    'отправлено в Кафка-топис filtered_messages_topic',
                    value.user_id, value.recipient_id)


if __name__ == '__main__':
    app.main()
