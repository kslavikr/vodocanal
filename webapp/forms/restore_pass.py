from django.forms import (ModelForm, Form, ModelChoiceField, EmailField,
                          CharField, ChoiceField, FloatField, DecimalField)               
from django.forms.widgets import Textarea, Select
from django.contrib.auth.models import User
from webapp.utilities.db_handler import DbSyncHandler
# from webapp.models import Payments
from webapp.utilities.log_handler import write_log


class PassRestoreForm(Form):

    user_id = CharField(label="Номер контракту",
                        max_length=500,
                        required=True,
                        error_messages={'required':
                                        "Це поле є обов'язковим"},
                        help_text="Номер присвоєний клієнту водоканалом")
                        
    last_bill = DecimalField(label="Останній рахунок",
                           required=False,
                           error_messages={'required':
                                           "Це поле є обов'язковим"},
                           help_text="Сума до оплати з останнього рахунку")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].widget.attrs['class'] = "form-control"
        self.fields['last_bill'].widget.attrs['class'] = "form-control"

    def clean(self):
        '''Method validates form fields'''
        form_data = self.cleaned_data
        self._check_user_existence(form_data)
        return form_data

    def _check_user_existence(self, form_data):
        user_obj = User.objects.filter(pk=form_data.get("user_id", ""))
        print(user_obj)
        if not user_obj:
            self._errors["user_id"] =\
                ['Користувач із вказаним номером контракту не зареєстрований в базі']
            write_log(user=form_data.get("user_id", ""),
                      place="Відновлення Паролю",
                      msg_type="Невдало",
                      message="Невдала спроба відновлення паролю (користувач не зареєстрований)")
        else:
            user_obj = user_obj[0]
            db_handler = DbSyncHandler()
            db_handler.sync_user_info(user_obj)
            payments = DbSyncHandler()._get_sql_payments(user_obj)[::-1]
            # payments = list(Payments.objects.filter(user=user_obj).order_by("date_added"))
            user_bill = abs(form_data.get("last_bill", ""))
            if payments:
                last_bill = abs(payments[-1].to_pay)
                prev_bill = last_bill
                if len(payments) > 1:
                    prev_bill = abs(payments[-2].to_pay)
                # print(form_data.get("last_bill", ""), last_bill)
                # print(type(form_data.get("last_bill", "")), type(last_bill))
                # print(form_data.get("last_bill", "")==last_bill)
                if last_bill != user_bill and prev_bill != user_bill:
                    self._errors["last_bill"] =\
                        ['Не вірна сума останнього рахунку']
                    write_log(user=user_obj.pk,
                              place="Відновлення Паролю",
                              msg_type="Невдало",
                              message="Невдала спроба відновлення паролю (введена сума - {}|{},{}|)".format(user_bill, last_bill, prev_bill))
                
