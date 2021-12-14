from pymyorm.model import Model


class User(Model):
    tablename = 't_user'
    datetime_fields = ['time']
    decimal_fields = ['money']

    gender_male = 1
    gender_female = 2
