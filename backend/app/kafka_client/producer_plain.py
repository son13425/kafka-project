"""Простой продюсер кафка."""
from typing import Optional

from confluent_kafka import Producer
from core.config import logger


class MessagePlainProducer:
    """Простой продюсер кафка."""
    def __init__(
            self,
            bootstrap_servers: str
    ):
        """
        Инициализация продюсера
        """
        self.bootstrap_servers = bootstrap_servers

        # Конфигурация продюсера
        conf = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'python-plain-producer'
        }

        self.producer = Producer(conf)

    def delivery_callback(self, err, msg):
        """Callback для отслеживания доставки сообщений"""
        if err:
            logger.error(f'Ошибка доставки сообщения: {err}')
            print(f"Ошибка доставки: {err}")
        else:
            logger.info(
                f'Сообщение доставлено в {msg.topic()} [{msg.partition()}]'
            )
            print(
                f"Сообщение доставлено: topic={msg.topic()}, "
                f"partition={msg.partition()}, offset={msg.offset()}"
            )

    def send_message(self, key: str, topic: str, message: str) -> bool:
        """Отправка сообщения в Kafka."""
        try:
            print(f"Отправка сообщения в Kafka: {message}")

            # Сериализация ключа (просто строку в bytes)
            serialized_key = key.encode('utf-8') if key else None

            # Отправка сообщения
            self.producer.produce(
                topic=topic,
                key=serialized_key,
                value=message,
                callback=self.delivery_callback
            )

            # Обработка событий
            self.producer.poll(0)

            # Принудительная отправка всех сообщений
            self.producer.flush(timeout=5)

            return True

        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в Kafka: {e}")
            print(f"Ошибка при отправке: {e}")
            return False

    def close(self):
        """Закрытие продюсера"""
        try:
            self.producer.flush(timeout=10)
        except Exception as e:
            logger.error(f"Ошибка при закрытии продюсера: {e}")


# Глобальный экземпляр продюсера
producer_instance: Optional[MessagePlainProducer] = None


def init_plain_producer(
    bootstrap_servers: str
) -> MessagePlainProducer:
    """Инициализация глобального продюсера"""
    global producer_instance
    if producer_instance is None:
        producer_instance = MessagePlainProducer(
            bootstrap_servers
        )
    return producer_instance


def get_plain_producer() -> Optional[MessagePlainProducer]:
    """Получение глобального продюсера"""
    return producer_instance
