from django.db.models import (Model, CharField, ForeignKey, BooleanField,
                              DateTimeField, IntegerField,DecimalField)
from django.contrib.auth.models import User

#
# class DbInfo(Model):
#
#     class Meta:
#         verbose_name = "Db info"
#         verbose_name_plural = "Db info"
#
#     host = CharField(max_length=50,
#                                 verbose_name="db host",
#                                 default="",
#                                 unique=False,
#                                 blank=False,
#                                 null=False)
#
#     database = CharField(max_length=50,
#                                 verbose_name="db name",
#                                 default="",
#                                 unique=False,
#                                 blank=False,
#                                 null=False)
#
#     user = CharField(max_length=50,
#                                 verbose_name="user name",
#                                 default="",
#                                 unique=False,
#                                 blank=False,
#                                 null=False)
#
#     password = CharField(max_length=50,
#                                 verbose_name="user password",
#                                 default="",
#                                 unique=False,
#                                 blank=False,
#                                 null=False)
#
#     def __str__(self):
#         return self.host
class DefaultSettingModel(Model):

    class Meta:
        verbose_name = "Default Setting"
        verbose_name_plural = "Default Setting"

    param = CharField(max_length=500,
                      verbose_name="param",
                      default="",
                      unique=False,
                      blank=True,
                      null=True)
    value = CharField(max_length=500,
                      verbose_name="param",
                      default="",
                      unique=False,
                      blank=True,
                      null=True)

class UsersDetailModel(Model):

    class Meta:
        verbose_name = "User Detail Model"
        verbose_name_plural = "Users Detail Model"

    user = ForeignKey(User,
                      null=False)

    town = CharField(max_length=500,
                     verbose_name="user town",
                     default="",
                     unique=False,
                     blank=True,
                     null=True)

    street = CharField(max_length=500,
                      verbose_name="user street",
                      default="",
                      unique=False,
                      blank=True,
                      null=True)

    house = CharField(max_length=500,
                      verbose_name="user house",
                      default="",
                      unique=False,
                      blank=True,
                      null=True)
                      
    appartment = CharField(max_length=500,
                           verbose_name="user appartment",
                           default="",
                           unique=False,
                           blank=True,
                           null=True)

    phone = CharField(max_length=20,
                      verbose_name="user phone number",
                      default="",
                      unique=False,
                      blank=True,
                      null=True)

    def __str__(self):
        return self.user.username

# class ContractId(Model):
#
#     class Meta:
#         verbose_name = "Contract Id"
#         verbose_name_plural = "Contracts Ids"
#
#     user = ForeignKey(User,
#                       null=False)
#
#     contract_id = CharField(max_length=100,
#                             verbose_name="contract id",
#                             unique=False,
#                             blank=False,
#                             null=False)
#
#     contract_descr = CharField(max_length=100,
#                               verbose_name="contract desc",
#                               unique=False,
#                               blank=True,
#                               null=False)
#
#     def __str__(self):
#         return self.contract_id
#
# class CountersValues(Model):
#
#     class Meta:
#         verbose_name = "Counter value"
#         verbose_name_plural = "Counter values"
#
#     contract = ForeignKey(ContractId)
#
#     value_user = IntegerField(verbose_name="user counter value",
#                               unique=False,
#                               blank=True,
#                               null=True)
#
#     value_vodocanal = IntegerField(verbose_name="vodocanal counter value",
#                                   unique=False,
#                                   blank=True,
#                                   null=True)
#
#     registration_time = DateTimeField(verbose_name="time of value registration",
#                                       unique=False,
#                                       blank=False,
#                                       null=True)
#
#     def __str__(self):
#         return self.registration_time.strftime("%Y-%m-%d %H:%M:%S")

# class Payments(Model):
#
#     class Meta:
#         verbose_name = "Payment"
#         verbose_name_plural = "Payments"
#
#     user = ForeignKey(User,
#                       null=False)
#
#     date_added = DateTimeField(verbose_name="add time",
#                               unique=False,
#                               blank=False,
#                               null=False)
#
#     payed_paid = DecimalField(verbose_name="payed paid",
#                               unique=False,
#                               blank=True,
#                               null=True,
#                               max_digits=15,
#                               decimal_places=2
#                               )
#
#     to_pay = DecimalField(verbose_name="to pay",
#                           unique=False,
#                           blank=True,
#                           null=True,
#                           max_digits=15,
#                           decimal_places=2)
#     payed_paid_user = DecimalField(verbose_name="payed_paid_user",
#                                    unique=False,
#                                    blank=True,
#                                    null=True,
#                                    max_digits=15,
#                                    decimal_places=2)
#     payed_paid_subs = DecimalField(verbose_name="payed_paid_subs",
#                                    unique=False,
#                                    blank=True,
#                                    null=True,
#                                    max_digits=15,
#                                    decimal_places=2)
#     payed_paid_pilgy = DecimalField(verbose_name="payed_paid_pilgy",
#                                     unique=False,
#                                     blank=True,
#                                     null=True,
#                                     max_digits=15,
#                                     decimal_places=2)
#     calc_to_pay = DecimalField(verbose_name="to pay 1",
#                                unique=False,
#                                blank=True,
#                                null=True,
#                                max_digits=15,
#                                decimal_places=2)
#
#     def __str__(self):
#         return self.date_added.strftime("%Y-%m-%d %H:%M:%S")


class LogModel(Model):

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    date_added = DateTimeField(verbose_name="add time",
                               unique=False,
                               blank=False,
                               null=False)

    user_id = CharField(max_length=100,
                        verbose_name="user id",
                        unique=False,
                        blank=False,
                        null=False)

    msg_source = CharField(max_length=100,
                           verbose_name="source",
                           unique=False,
                           blank=False,
                           null=False)

    msg_type = CharField(max_length=100,
                         verbose_name="type",
                         unique=False,
                         blank=False,
                         null=False)

    msg = CharField(max_length=500,
                     verbose_name="msg",
                     unique=False,
                     blank=False,
                     null=False)
     