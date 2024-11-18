from asyncio.log import logger
from datetime import datetime

from flask import jsonify

from AuthService import AuthService
from data.DefaultRepository import DefaultRepository


class DefaultTransaction(DefaultRepository):

    def news(self, offset):
        """
        Робить запит з метою витягування всіх постів
        """
        try:
            # Починаємо транзакцію
            self._ensure_connection()
            self._connection.begin()

            news_response = self._news(offset)

            if not news_response:
                raise Exception("Error: request database is null")

            # Конвертуємо нестандартні типи (наприклад, bytes)
            for item in news_response:
                if isinstance(item.get('img_data'), bytes):
                    item['img_data'] = item['img_data'].decode('utf-8')  # Декодуємо у текст
                if isinstance(item.get('created'), datetime):
                    item['created'] = item['created'].isoformat()  # Перетворюємо дату у ISO-формат

            # Повертаємо результат
            return jsonify({"result": True, "news": news_response}), 200

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return str(e), 400
        finally:
            self._close()

    def register_auth(self, uuid, android_id):
        """
        Реєструє або перевіряє адміна на валідність
        """
        try:
            # Починаємо транзакцію
            self._ensure_connection()
            self._connection.begin()

            # need authorization weekly
            new_token = AuthService.create_jwt(data={"uuid": uuid, "android_id": android_id}, expires_in=3600 * 24 * 7)

            if not self._is_admin(uuid, android_id) and not self._set_admin(uuid, android_id):
                raise Exception("Error: registration fail, auth key is not correct")

            self._commit()

            return jsonify({"result": True, "Token": new_token}), 200

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return str(e), 400
        finally:
            self._close()

    def post(self, title, desc, img_url):
        """
        Додає новину до бази
        """
        try:
            # Починаємо транзакцію
            self._ensure_connection()
            self._connection.begin()

            if not self._post(title, desc, img_url):
                raise Exception("Error: database can`t add this")

            self._commit()

            return jsonify({"result": True, "message": "post success"}), 200

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return str(e), 400
        finally:
            self._close()

    def remove(self, identify):
        """
        Видаляє новину з бази по id
        """
        try:
            # Починаємо транзакцію
            self._ensure_connection()
            self._connection.begin()

            if not self._remove(identify):
                raise Exception("Error: database can`t delete this")

            self._commit()

            return jsonify({"result": True, "message": "delete success"}), 200

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return str(e), 400
        finally:
            self._close()
