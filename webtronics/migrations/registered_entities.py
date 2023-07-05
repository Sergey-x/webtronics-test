# Добавьте сбда функции и триггеры для генерации миграций для них
from models.like_triggers import (
    after_delete_like,
    after_delete_like_trigger,
    after_insert_like,
    after_insert_like_trigger,
)


registered_entities = (
    after_insert_like,
    after_insert_like_trigger,
    after_delete_like,
    after_delete_like_trigger,
)

__all__ = (
    "registered_entities",
)
