import db


class AidKit:
    def __init__(self, med_id, user_id):
        self.med_id = med_id
        self.user_id = user_id
        self.value_now = None

    def create_new_aid_kit(self):
        create_new_aid_kit_sql = """
        INSERT INTO aid_kit (med_id, user_id, value_now) 
        VALUES ('%s', '%s', '%s');
        """ % (self.med_id, self.user_id, self.value_now)

        print(create_new_aid_kit_sql)

        db.executor(create_new_aid_kit_sql)