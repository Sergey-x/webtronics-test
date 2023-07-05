from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from models.like import LIKES_TABLE_NAME


SCHEMA: str = "public"

AFTER_INSERT_LIKE_FUNC_NAME: str = "after_insert_like"

after_insert_like = PGFunction(
    schema=SCHEMA,
    signature=f"{AFTER_INSERT_LIKE_FUNC_NAME}()",
    definition="""
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE posts SET likes = likes + 1 WHERE id = NEW.post_id;
            RETURN NEW;
        END
        $$ LANGUAGE 'plpgsql';
    """,
)

after_insert_like_trigger = PGTrigger(
    schema=SCHEMA,
    signature=f"{AFTER_INSERT_LIKE_FUNC_NAME}_trigger",
    on_entity=f"{SCHEMA}.{LIKES_TABLE_NAME}",
    is_constraint=False,
    definition=f"""
        AFTER INSERT ON {LIKES_TABLE_NAME}
        FOR EACH ROW
        EXECUTE PROCEDURE {AFTER_INSERT_LIKE_FUNC_NAME}();
    """,
)

# ------------------------------------------------------------------------------
AFTER_DELETE_LIKE_FUNC_NAME: str = "after_delete_like"
after_delete_like = PGFunction(
    schema=SCHEMA,
    signature=f"{AFTER_DELETE_LIKE_FUNC_NAME}()",
    definition="""
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE posts SET likes = likes - 1 WHERE id = OLD.post_id;
            RETURN OLD;
        END
        $$ LANGUAGE 'plpgsql';
    """,
)

after_delete_like_trigger = PGTrigger(
    schema=SCHEMA,
    signature=f"{AFTER_DELETE_LIKE_FUNC_NAME}_trigger",
    on_entity=f"{SCHEMA}.{LIKES_TABLE_NAME}",
    is_constraint=False,
    definition=f"""
        AFTER DELETE ON {LIKES_TABLE_NAME}
        FOR EACH ROW
        EXECUTE PROCEDURE {AFTER_DELETE_LIKE_FUNC_NAME}();
    """,
)
# ------------------------------------------------------------------------------

__all__ = (
    "after_insert_like",
    "after_insert_like_trigger",
    "after_delete_like",
    "after_delete_like_trigger",
)
