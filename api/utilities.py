import tarantool
connection = tarantool.connect("localhost", 3301, user='admin', password='pass')
tester = connection.space('tester')

class DataBase:
    pk = 1

    def __init__(self):
        self.tester = tester

    def post_db(self, data):
        #try:
        self.tester.insert((self.pk, data['key'], str(data['value'])))
        self.pk += 1
        #    return True
        #except DatabaseError:
        #    return False

    def put_db(self, pk, data):
        self.tester.update(pk, [('=', 2, str(data['value']))])

    def delete_db(self, pk):
        self.tester.delete(pk)

    def get_db(self, pk):
        return self.tester.select(pk)

    def valid_value(self, data):
        if "value" not in data.keys() or type(data['value']) != dict:
            return False
        return True

    def valid_key(self, data):
        if "key" not in data.keys() or type(data['key']) != str:
            return False
        return True

    def valid_put_data(self, data):
        if self.valid_value(data) and len(data.keys()) == 1:
            return True
        return False

    def valid_post_data(self, data):
        if self.valid_value(data) and self.valid_key(data) and len(data.keys()) == 2:
            return True
        return False

db = DataBase()
