from functools import wraps
from fastapi import HTTPException
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    OperationalError,
    TimeoutError,
    StatementError,
    DBAPIError,
    DisconnectionError,
    NoResultFound,
    PendingRollbackError,
)
import asyncpg


def db_errors_to_http(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            raise HTTPException(
                status_code=409, detail="Нарушено ограничение целостности данных"
            )

        except DataError as e:
            raise HTTPException(
                status_code=400, detail="Некорректные данные при работе с БД"
            )

        except OperationalError as e:
            raise HTTPException(
                status_code=500, detail="Ошибка операционной работы с БД"
            )

        except TimeoutError as e:
            raise HTTPException(
                status_code=504, detail="Превышено время ожидания БД"
            )

        except StatementError as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Неправильный SQL-запрос"
            )

        except DBAPIError as e:
            raise HTTPException(
                status_code=500, detail="Ошибка низкоуровневого драйвера БД"
            )

        except DisconnectionError as e:
            raise HTTPException(
                status_code=503, detail="Потеряно соединение с БД"
            )

        except NoResultFound as e:
            raise HTTPException(
                status_code=404, detail="Запись не найдена"
            )

        except PendingRollbackError as e:
            raise HTTPException(
                status_code=500, detail="Транзакция БД в состоянии отката"
            )

        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPException(
                status_code=409, detail="Нарушено ограничение уникальности"
            )
        except asyncpg.exceptions.ForeignKeyViolationError as e:
            raise HTTPException(
                status_code=409, detail="Нарушено внешнее ограничение (FK)"
            )
        except asyncpg.exceptions.NotNullViolationError as e:
            raise HTTPException(
                status_code=400, detail="Обязательное поле имеет NULL‑значение"
            )
        except asyncpg.exceptions.CheckViolationError as e:
            raise HTTPException(
                status_code=400, detail="Нарушено условие CHECK"
            )
        except asyncpg.PostgresError as e:
            raise HTTPException(
                status_code=500, detail="Ошибка PostgreSQL: " + e.__class__.__name__
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Внутренняя ошибка сервера: {e}"
            )

    return wrapper