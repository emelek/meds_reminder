import db


class Med:
    def __init__(self, name):
        self.name = name
        self.value_in_full = None
        self.valid_before = None

    def create_new_med(self):
        need_to_create = db.existor('med', 'name', self.name)
        if not need_to_create:
            pass
        else:
            create_new_med_sql = """
            INSERT INTO med (name, value_in_full) 
            VALUES ('%s', '%s');
            """ % (self.name, self.value_in_full)
            return db.executor(create_new_med_sql)
