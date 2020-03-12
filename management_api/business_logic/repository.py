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
            logging.exception('Cannot create restaurant')
            raise
        finally:
            self.cursor.close()

    def upload_menu(self, restaurant_name, user_name, file_name, file_body):
        try:
            self.cursor.execute("BEGIN")
            self.cursor.callproc("pr_upload_menu", [restaurant_name, user_name, file_name, file_body])
            new_menu_id = self.cursor.fetchone()
            self.cursor.execute("COMMIT")
            return new_menu_id[0]
        except Exception as e:
            logging.exception('Cannot upload menu')
            raise
        finally:
            self.cursor.close()

    def user_vote(self, restaurant_name, user_name):
        try:
            self.cursor.execute("BEGIN")
            self.cursor.callproc("pr_user_vote", [restaurant_name, user_name])
            votes_count = self.cursor.fetchone()
            self.cursor.execute("COMMIT")
            return votes_count[0]
        except Exception as e:
            logging.exception('Cannot vote for restaurant')
            raise
        finally:
            self.cursor.close()

    def current_day_winner(self, skip_last_consecutive_working_days):
        try:
            self.cursor.execute("BEGIN")
            self.cursor.callproc("pr_winner", [skip_last_consecutive_working_days])
            winner = self.cursor.fetchone()
            self.cursor.execute("COMMIT")
            return winner[0]
        except Exception as e:
            logging.exception('Cannot find current day winner')
            raise
        finally:
            self.cursor.close()
