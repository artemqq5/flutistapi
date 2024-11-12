from asyncio.log import logger

import pymysql
import pymysql.cursors

from config import DATABASE_PASSWORD, DATABASE_NAME


class DefaultDataBase:

    def __init__(self):
        self._connect()

    def _connect(self):
        """Створює нове з'єднання."""
        self._connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    def _insert(self, query, args=None):
        try:
            with self._connection.cursor() as cursor:
                result = cursor.execute(query, args)
                return result
        except Exception as e:
            logger.error(f"_insert: {e}")
            self._connection.rollback()

    def _update(self, query, args=None):
        try:
            with self._connection.cursor() as cursor:
                result = cursor.execute(query, args)
                return result
        except Exception as e:
            logger.error(f"_update: {e}")
            self._connection.rollback()

    def _delete(self, query, args=None):
        try:
            with self._connection.cursor() as cursor:
                result = cursor.execute(query, args)
                return result
        except Exception as e:
            logger.error(f"_delete: {e}")
            self._connection.rollback()

    def _select_one(self, query, args=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"_select_one: {e}")

    def _select(self, query, args=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"_select_all: {e}")

    def _commit(self):
        """Коміт транзакції."""
        try:
            self._connection.commit()
        except Exception as e:
            logger.error(f"commit: {e}")
            self._connection.rollback()

    def _rollback(self):
        """Відкат транзакції."""
        try:
            self._connection.rollback()
        except Exception as e:
            logger.error(f"rollback: {e}")

    def _ensure_connection(self):
        """Перевіряє, чи з'єднання активне, і створює нове, якщо потрібно."""
        if not self._connection or not self._connection.open:
            self._connect()

    def _close(self):
        """Закриває з'єднання з базою даних."""
        try:
            if self._connection and self._connection.open:
                self._connection.close()
        except Exception as e:
            logger.error(f"close: {e}")