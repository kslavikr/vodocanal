from django.contrib.auth.models import User
import datetime
from decimal import Decimal

class Payments_SQL:
    def __init__(self, user ,payment_info):
        self.user = user
        self.date_added = payment_info[1]
        self.payed_paid = to_decimal(payment_info[2])
        self.to_pay = to_decimal(payment_info[3])
        self.payed_paid_user = to_decimal(payment_info[4])
        self.payed_paid_subs = to_decimal(payment_info[5])
        self.payed_paid_pilgy = to_decimal(payment_info[6])
        self.calc_to_pay = to_decimal(payment_info[7])

    def __str__(self):
        return self.date_added.strftime("%Y-%m-%d %H:%M:%S")

def to_decimal(pay):
    return round(Decimal.from_float(pay),2)

class Contracts_SQL:

    def __init__(self, contracts):
        self.user = contracts[0]
        self.contract_id = contracts[1]
        self.contract_descr = contracts[2]

    def __str__(self):
        return self.contract_id

class CountersValues_SQL:

    def __init__(self, contract_value):
        self.contract = contract_value[0]
        self.value_user = contract_value[2]
        self.value_vodocanal = contract_value [3]
        self.registration_time = contract_value [1]

    def __str__(self):
        return self.registration_time.strftime("%Y-%m-%d %H:%M:%S")

