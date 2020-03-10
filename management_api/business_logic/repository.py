import logging


class ManagementApiRepository:
    def __init__(self, cursor):
        self.cursor = cursor

    def logout(self, user):
        try:
            self.cursor.execute("BEGIN")
            self.cursor.callproc("pr_log_out_", [user])
            self.cursor.execute("COMMIT")
        except Exception as e:
            logging.exception('Cannot perform logout')
            raise
        finally:
            self.cursor.close()

    def create_restaurant(self, name):
        try:
            self.cursor.execute("BEGIN")
            self.cursor.callproc("pr_create_restaurant", [name])
            new_restaurant_id = self.cursor.fetchone()
            self.cursor.execute("COMMIT")
            return new_restaurant_id[0]
        except Exception as e:
            logging.exception('Cannot perform logout')
            raise
        finally:
            self.cursor.close()

