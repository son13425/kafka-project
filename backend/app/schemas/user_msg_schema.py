from pydantic import BaseModel


class IncominUserMessageSchema(BaseModel):
    """Схема исходящего сообщения для ПР2"""
    user_id: str
    recipient_id: str
    timestamp: str
    message: str

    class Config:
        """Для совместимости с ORM."""
        from_attributes = True


class IncomingBlockedMessageSchema(BaseModel):
    """Схема входящего сообщения для П2"""
    user_id: str
    blocked_user_id: str
    timestamp: str
    action: str

    class Config:
        """Для совместимости с ORM."""
        from_attributes = True
