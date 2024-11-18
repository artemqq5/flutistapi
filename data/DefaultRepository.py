from data.DefaultDataBase import DefaultDataBase


class DefaultRepository(DefaultDataBase):

    def _news(self, offset):
        query = "SELECT * FROM `news` ORDER BY `created` ASC LIMIT 5 OFFSET %s;"
        return self._select(query, (offset, ))

    def _post(self, title, desc, img_data):
        query = "INSERT INTO `news` (`title`, `desc`, `img_url`) VALUES (%s, %s, %s);"
        return self._insert(query, (title, desc, img_data))

    def _remove(self, identify):
        query = "DELETE FROM `news` WHERE `id` = %s;"
        return self._delete(query, (identify,))

    def _set_admin(self, uuid, android_id):
        query = "UPDATE `keys` SET `android_id` = %s, `activated` = NOW() WHERE `uuid` = %s;"
        return self._update(query, (android_id, uuid))

    def _is_admin(self, uuid, android_id):
        query = "SELECT * FROM `keys` WHERE `uuid` = %s AND `android_id` = %s;"
        return self._select_one(query, (uuid, android_id))

