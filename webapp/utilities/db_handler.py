import psycopg2
import string
import random
import math
import datetime
from decimal import Decimal
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from webapp.models import (UsersDetailModel,
                           # DbInfo,
                           # ContractId,
                           # CountersValues,
                           # Payments
                           )
from countersweb.settings import (user_sync_db,
                                  passw_sync_db,
                                  host_sync_db,
                                  name_sync_db,
                                  host_url)
from webapp.utilities.log_handler import write_log
from webapp.models_sql import (Payments_SQL,
                               Contracts_SQL,
                               CountersValues_SQL)

class DbSyncHandler():

    def __init__(self):
        self.connection = psycopg2.connect(host=host_sync_db,
                                           database=name_sync_db,
                                           user=user_sync_db,
                                           password=passw_sync_db)

    def get_bill_month(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT max(dateadded) FROM payments where topay!=0")
            last_bill = cursor.fetchall()
            cursor.close()
            if last_bill:
                return last_bill[-1][0].month
            return None
        except Exception as e:
            print(e)
            return None

    def fetch_user_info(self, user_id, email, to_pay):
        cursor = self.connection.cursor()
        cursor.execute("SELECT userid, pib, street, housenumber, appnumber  FROM users WHERE userid=" + str(user_id))
        user_list = cursor.fetchall()
        cursor.close()
        if user_list:
            if self._check_topay(user_id, to_pay):
                new_user = self._create_user(user_list[0], email)
                self.sync_user_info(new_user)
                return (new_user, "")
            else:
                return (None, "to_pay")
        return (None, "user_id")

    def _check_topay(self, user_id, to_pay):
        cursor = self.connection.cursor()
        cursor.execute("SELECT userid, dateadded, debt, topay, debt_user, debt_subs, debt_pilgy, topay_1  FROM payments WHERE userid=" + str(user_id) +" ORDER BY dateadded")
        payment_list = cursor.fetchall()
        if payment_list:
            last_payment = payment_list[-1]
            result = (abs(round(to_pay, 2)) == abs(round(Decimal.from_float(last_payment[3]), 2)))
            if result:
                cursor.close() 
                return result
            if len(payment_list) > 1:
                last_payment = payment_list[-2]
                cursor.close() 
                return (abs(round(to_pay, 2)) == abs(round(Decimal.from_float(last_payment[3]), 2)))
        cursor.close() 
        return False
          
    def _create_user(self, user, email):
        user_obj = User(pk=user[0],
                        first_name=user[1][0:29],
                        username=str(user[0]),
                        email=email)
        user_pass = self._generate_pass()
        # print(user_pass)
        user_obj.set_password(user_pass)
        user_obj.save()
        user_datail_obj = UsersDetailModel(user=user_obj,
                                           town="",
                                           street=user[2],
                                           house=user[3],
                                           appartment=user[4],
                                           phone="")
        user_datail_obj.save()
        try:
            print("TRY TO SEND EMAIL")
            self._send_email_reg(user_obj, user_pass)
        except BaseException as e:
            print("ERROR DURING SEND EMAIL")
            print(e)
        write_log(user=user_obj.pk,
                  place="Реєстрація",
                  msg_type="Успішно",
                  message="Реєстрація користувача (пароль - {})".format(user_pass))
        return user_obj

    def _generate_pass(self, size=8,
                       chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def _send_email_reg(self, user_obj, user_pass):
        subject = "Registration Success"
        text = ("Лічильники вітають вас з реєстрацією \n" +
                "Ваш логін - " + str(user_obj.pk) + "\n" +
                "Ваш пароль - " + str(user_pass) + "\n"+
                "Спробуйте залогуватись на сторінці - <a href='"+host_url+"'>ВХІД</a>" +"\n")
        html_mess = ("Лічильники вітають вас з реєстрацією <BR>" +
                "Ваш логін - " + str(user_obj.pk) + "<BR>" +
                "Ваш пароль - " + str(user_pass) + "<BR>"+
                "Спробуйте залогуватись на сторінці - <a href='"+host_url+"'>ВХІД</a>" +"<BR>")
        sender = '"Vodokanal" <vodokanal@forever.in.net>'
        html_mess = "<!DOCTYPE html><html><head> </head><body>"+html_mess+" </body></html>"
        send_mail(subject, text, sender, [user_obj.email], fail_silently=True, html_message=html_mess)

    def sync_user_info(self, user_obj):
        # user_id = user_obj.pk
        # print("start user sync")
        # # contract_list = self._sync_user_contracts(user_id)
        # print("sync contracts finished")
        # # self._sync_user_contracts_value(contract_list,user_id)
        # print("sync contracts values finished")
        # # self._sync_user_payments(user_id)
        # print("sync payments finished")
        pass

    # def _sync_user_contracts(self, user_id):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT userid, counterid, counterdesc FROM counters WHERE userid=" + str(user_id))
    #     contract_list = cursor.fetchall()
    #     self._contracts_save(contract_list, user_id)
    #     cursor.close()
    #     return contract_list

    def _get_sql_user_contracts(self, user):
        cursor = self.connection.cursor()
        cursor.execute("SELECT userid, counterid, counterdesc FROM counters WHERE userid=" + str(user.pk)+" ORDER BY counterdesc")
        contract_list = cursor.fetchall()
        contracts = []
        for contract in contract_list:
            contract_obj = Contracts_SQL(contract)
            sql_contract={"contract" : contract_obj,
                          "value":self._get_sql_user_contract_values(contract_obj)}
            contracts.append(sql_contract)
        cursor.close()
        return contracts

    def _get_sql_user_contracts_by_id(self, user_id, contract_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT userid, counterid, counterdesc FROM counters WHERE counterid = "+str(contract_id)+" and userid=" + str(user_id)+" ORDER BY counterdesc")
        contract_list = cursor.fetchall()
        contracts = []
        print(contract_list)
        for contract in contract_list:
            contract_obj = Contracts_SQL(contract)
            contract_values=self._get_sql_user_contract_values_to(contract_obj)
            if contract_values:
                sql_contract={"contract" : contract_obj,
                              "value":contract_values[0]}
            contracts.append(sql_contract)
        cursor.close()
        return contracts

    def _get_sql_user_contract_values_to(self, contract):
        cursor = self.connection.cursor()
        cursor.execute("SELECT counterid, dateadded, volumefrom, volumeto FROM accountants  WHERE counterid=" + str(
            contract.contract_id) + " and userid=" + str(contract.user) +
                       " and volumeto>0 ORDER BY dateadded DESC")
        contract_value_list = cursor.fetchall()
        counters_value_list = []
        for contract_value in contract_value_list:
            counters_value_list.append(CountersValues_SQL(contract_value))
        cursor.close()
        return counters_value_list

    def _get_sql_user_contract_values(self, contract):
        cursor = self.connection.cursor()
        cursor.execute("SELECT counterid, dateadded, volumefrom, volumeto FROM accountants  WHERE counterid=" + str(
            contract.contract_id) + " and userid=" + str(contract.user) + " ORDER BY dateadded DESC")
        contract_value_list = cursor.fetchall()
        counters_value_list = []
        for contract_value in contract_value_list:
            counters_value_list.append(CountersValues_SQL(contract_value))
        cursor.close()
        return counters_value_list
        # return sorted(counters_value_list, key=lambda x: x.registration_time, reverse=True)

    # def _sync_user_contracts_value(self, contract_list, user_id):
    #     for contract in contract_list:
    #         #Hard Synchronization
    #         #Should be removed in case of not needed synchronization every time
    #         print(contract)
    #         values = (CountersValues.objects.
    #                         filter(contract__contract_id=contract[1]))
    #         for value in values:
    #             value.delete()
    #         #end of Hard Synchronization
    #         counter_id = contract[1]
    #         cursor = self.connection.cursor()
    #         cursor.execute("SELECT counterid, dateadded, volumefrom, volumeto FROM accountants  WHERE counterid=" + str(counter_id) + " and userid=" + str(user_id)+" ORDER BY dateadded")
    #         contract_value_list = cursor.fetchall()
    #         self._contract_values_save(contract_value_list)
    #         cursor.close()

    # def _sync_user_payments(self, user_id):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT userid, dateadded, debt, topay, debt_user, debt_subs, debt_pilgy, topay_1 FROM payments WHERE userid=" + str(user_id) + " ORDER BY dateadded")
    #     payment_list = cursor.fetchall()
    #     print(payment_list)
    #     self._payments_save(payment_list)
    #     print(Payments.objects.filter(user__pk=user_id))
    #     cursor.close()

    def _get_sql_payments(self, user):
        cursor = self.connection.cursor()
        cursor.execute("SELECT userid, dateadded, debt, topay, debt_user, debt_subs, debt_pilgy, topay_1 FROM payments WHERE userid=" + str(user.pk) + " ORDER BY dateadded DESC")
        payment_list = cursor.fetchall()
        # print(payment_list)
        payments_sql = []
        for payment_info in payment_list:
            payments_sql.append(Payments_SQL(user, payment_info))
        return payments_sql
        # return sorted(payments_sql, key=lambda x: x.date_added, reverse=True)

    # def _contracts_save(self, contract_list,user_id):
    #     user = User.objects.filter(pk=user_id).first()
    #     for contract in contract_list:
    #         contract_obj_query = (ContractId.objects.
    #                               filter(contract_id=contract[1]).
    #                               filter(user=user))
    #         if not contract_obj_query:
    #             self._create_contract(contract)
    #         else:
    #             contract_obj = contract_obj_query.first()
    #             if not contract_obj.user.pk==contract[0]:
    #                 user = User.objects.filter(pk=contract[0])
    #                 if user:
    #                     contract_obj.user = user.first()
    #                     contract_obj.save()
                
    # def _create_contract(self, contract_info):
    #     user = User.objects.filter(pk=contract_info[0])
    #     if user:
    #         new_contract = ContractId(user=user.first(),
    #                                   contract_id=str(contract_info[1]),
    #                                   contract_descr=str(contract_info[2]))
    #         new_contract.save()
    #
    # def _contract_values_save(self, value_list):
    #     for value in value_list:
    #         values_query = (CountersValues.objects.
    #                         filter(contract__contract_id=value[0]).
    #                         filter(registration_time=value[1]))
    #         if values_query:
    #             self._update_value(value, values_query.last())
    #         else:
    #             self._create_value(value)
        

    # def _create_value(self, value_info):
    #     contract_query = ContractId.objects.filter(contract_id=value_info[0])
    #     if contract_query:
    #         contract_obj = contract_query.first()
    #         new_value = CountersValues(contract=contract_obj,
    #                                    value_user=value_info[2],
    #                                    value_vodocanal=value_info[3],
    #                                    registration_time=value_info[1])
    #         new_value.save()

    # def _update_value(self, value_info, value_obj):
    #     update = False
    #     if not value_obj.value_user==value_info[2]:
    #         value_obj.value_user=value_info[2]
    #         update = True
    #     if not value_obj.value_vodocanal==value_info[3]:
    #         value_obj.value_vodocanal = value_info[3]
    #         update = True
    #     if update:
    #         value_obj.save()

    # def _payments_save(self, payment_list):
    #     for payment in payment_list:
    #         payment_query = (Payments.objects.
    #                          filter(user__pk=payment[0]).
    #                          filter(date_added=payment[1]))
    #         if payment_query:
    #             self._update_payments(payment, payment_query.first())
    #         else:
    #             self._create_payment(payment)
    #
    # def _create_payment(self, payment_info):
    #     user = User.objects.filter(pk=payment_info[0])
    #     if user:
    #         new_payment = Payments(user=user.first(),
    #                                date_added=payment_info[1],
    #                                payed_paid=payment_info[2],
    #                                to_pay=payment_info[3],
    #                                payed_paid_user=payment_info[4],
    #                                payed_paid_subs=payment_info[5],
    #                                payed_paid_pilgy=payment_info[6],
    #                                calc_to_pay=payment_info[7]
    #                                )
    #         new_payment.save()
    #
    # def _update_payments(self, payment_info, payment_obj):
    #     update = False
    #     if not payment_obj.payed_paid==payment_info[2]:
    #         payment_obj.payed_paid = payment_info[2]
    #         update = True
    #     if not payment_obj.to_pay==payment_info[3]:
    #         payment_obj.to_pay = payment_info[3]
    #         update = True
    #     if not payment_obj.payed_paid_user==payment_info[4]:
    #         payment_obj.payed_paid_user = payment_info[4]
    #         update = True
    #     if not payment_obj.payed_paid_subs==payment_info[5]:
    #         payment_obj.payed_paid_subs = payment_info[5]
    #         update = True
    #     if not payment_obj.payed_paid_pilgy==payment_info[6]:
    #         payment_obj.payed_paid_pilgy = payment_info[6]
    #         update = True
    #     if not payment_obj.calc_to_pay==payment_info[7]:
    #         payment_obj.calc_to_pay = payment_info[7]
    #         update = True
    #     if update:
    #         payment_obj.save()

    def save_counter_value(self, user_id, counter_id, counter_value, time, last_val):
        result = False
        try:
            print(user_id, counter_id, counter_value, time)
            cursor = self.connection.cursor()
            command = "Select * from accountants where userid = %s and counterid = %s and date_part('year', current_date) = date_part('year', dateadded) and date_part('month',current_date) = date_part('month',dateadded);"
            cursor.execute(command, (user_id, counter_id))
            t_list = cursor.fetchall()
            number_counters_in_month = len(t_list)
            cursor.close()
            if (number_counters_in_month==0):
                self.save_counter_value_old(user_id, counter_id, counter_value, time,last_val)
            else:
                cursor = self.connection.cursor()
                command = "UPDATE accountants SET volumefrom = %s,dateadded = %s WHERE userid = %s and counterid = %s and date_part('year', current_date) = date_part('year', dateadded) and date_part('month',current_date) = date_part('month',dateadded);"
                cursor.execute(command, (counter_value,time, user_id, counter_id))
                self.connection.commit()
                cursor.close()
            result = True
            # self._sync_user_contracts_value([(user_id,counter_id)],user_id)
        except BaseException as e:
            print (e)
        return result

    def save_counter_value_old(self, user_id, counter_id, counter_value, time, last_val):
        result = False
        try:
            print(user_id, counter_id, counter_value, time)

            cursor = self.connection.cursor()
            command = "INSERT INTO accountants (userid, counterid, dateadded, volumefrom, volumeto)  VALUES(%s, %s, %s, %s, %s);"
            cursor.execute(command, (user_id, counter_id, time, counter_value, last_val))
            self.connection.commit()
            cursor.close()
            result = True
        except BaseException as e:
            print(e)
        return result



    # def sync_users(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT userid, pib, street, housenumber, appnumber  FROM users")
    #     users_list = cursor.fetchall()
    #     for user in users_list:
    #         user_obj = UsersModel.objects.filter(pk=user[0])
    #         if user_obj:
    #             self._update_user(user, user_obj.first())
    #         else:
    #             self._create_user(user)
    #     cursor.close()

    # def sync_users_by_id(self, user_id):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT userid, pib, street, housenumber, appnumber  counterdesc FROM users WHERE userid=" + str(user_id))
    #     user_list = cursor.fetchall()
    #     if user_list:
    #         user_obj = UsersModel.objects.filter(pk=user_list[0][0])
    #         if user_obj:
    #             self._update_user(user_list[0], user_obj.first())
    #         else:
    #             self._create_user(user_list[0])
    #     cursor.close()

    # def _update_user(self, user, user_obj):
    #     update = False
    #     if not user_obj.user_first_last==user[1]:
    #         user_obj.user_first_last = user[1]
    #         update = True
    #     if not user_obj.street==user[2]:
    #         user_obj.street = user[2]
    #         update = True
    #     user_addr = ""
    #     if user[3]:
    #         user_addr = "буд."+user[3]
    #     if user[4]:
    #         user_addr = user_addr + " кв. " + user[4]
    #     if not user_obj.house==user_addr:
    #         user_obj.house = user_addr
    #         update = True
    #     if update:
    #         user_obj.save()



    # def sync_contracts(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT userid, counterid, counterdesc FROM counters")
    #     contract_list = cursor.fetchall()
    #     self._contracts_save(contract_list)
    #     cursor.close()


        
    # def sync_counters_value(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT counterid, dateadded, volumefrom, volumeto FROM accountants ORDER BY dateadded")
    #     value_list = cursor.fetchall()
    #     self._contract_values_save(value_list)
    #     cursor.close()



    # def sync_payments(self):
    #     cursor = self.connection.cursor()
    #     cursor.execute("SELECT userid, dateadded, debt, topay FROM payments ORDER BY dateadded")
    #     payment_list = cursor.fetchall()
    #     self._payments_save(payment_list)
    #     cursor.close()

    # def _payments_save(self, payment_list):


    # def sync_user_info(self, user_obj):
    #     user_id = user_obj.pk
    #     print("start user sync")
    #     contract_list = self._sync_user_contracts(user_id)
    #     print("sync contracts finished")
    #     self._sync_user_contracts_value(contract_list)
    #     print("sync contracts values finished")
    #     self._sync_user_payments(user_id)
    #     print("sync payments finished")
        


    # def save_counter_value(self, user_id, counter_id, counter_value, time):
    #     result = False
    #     cursor = self.connection.cursor()
    #     command = "INSERT INTO accountants (userid, counterid, dateadded, volumefrom, volumeto)  VALUES(%s, %s, %s, %s, %s);"
    #     cursor.execute(command, (user_id, counter_id, time, counter_value, None))
    #     self.connection.commit()
    #     cursor.close()
    #     result = True
    #     return result