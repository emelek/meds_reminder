import db


class User:
    def __init__(self, name):
        self.name = name
        self.tg_code = None
        self.register_at = None
        self.time_zone = None

    def create_new_user(self):
        need_to_create = db.existor('user', 'tg_code', self.tg_code)
        if not need_to_create:
            pass
        else:
            create_new_user_sql = """
            INSERT INTO user (tg_code, name, register_at) 
            VALUES ('%s', '%s', '%s');
            """ % (self.tg_code, self.name, self.register_at)

            db.executor(create_new_user_sql)
