from django.forms import (ModelForm, Form, ModelChoiceField, EmailField,
                          CharField, ChoiceField, FloatField, DecimalField)               
from django.forms.widgets import Textarea, Select
from django.contrib.auth.models import User
from webapp.utilities.db_handler import DbSyncHandler
# from webapp.models import Payments
from webapp.utilities.log_handler import write_log


class RegistrationeForm(Form):

    user_id = CharField(label="Номер особового рахунку (Контракту)",
                        max_length=500,
                        required=True,
                        error_messages={'required':
                                        "Це поле є обов'язковим"},
                        help_text="Номер присвоєний клієнту водоканалом")
                        
    last_bill = DecimalField(label="Заборгованість/переплата",
                           required=False,
                           error_messages={'required':
                                           "Це поле є обов'язковим"},
                           help_text="Сума заборгованості/переплати на початок попереднього місяця")

    email = EmailField(label="Електронна скринька",
                       required=True,
                       error_messages={'required':
                                       "Це поле є обов'язковим"},
                       help_text="Адреса Вашої електронної скриньки")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].widget.attrs['class'] = "form-control"
        self.fields['last_bill'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        bill_help_text = "Сума заборгованості/переплати на початок попереднього місяця"
        #month = self._get_month()
        #if month:
        #    bill_help_text = bill_help_text + " (" + month + ")"
        self.fields['last_bill'].help_text = bill_help_text

    def clean(self):
        '''Method validates form fields'''
        form_data = self.cleaned_data
        self._check_user_existence(form_data)
        return form_data

    def _get_month(self):
        monthDict = {1:'січень', 2:'лютий', 3:'березень', 4:'квітень',
                     5:'травень', 6:'червень', 7:'липень', 8:'серпень',
                     9:'вересень', 10:'жовтень', 11:'листопад', 12:'грудень'}
        db_handler = DbSyncHandler()
        month_num = db_handler.get_bill_month()
        if month_num:
            return monthDict.get(month_num, None)
        return None


    def _check_user_existence(self, form_data):
        user_obj = User.objects.filter(pk=form_data.get("user_id", ""))
        print(user_obj)
        if user_obj:
            self._errors["user_id"] =\
                ['Користувач із вказаним номером контракту уже зараєстрований']
            write_log(user=user_obj.first().pk,
                      place="Реєстрація",
                      msg_type="Невдало",
                      message="Невдала спроба реєстрації (користувач із вказаним id уже існує)")
        else:
            user_obj = User.objects.filter(email=form_data.get("email", "@"))
            if user_obj:
                self._errors["email"] =\
                    ['Користувач із вказаною електронною скринькою  уже зараєстрований']
                write_log(user=user_obj.first().pk,
                          place="Реєстрація",
                          msg_type="Невдало",
                          message="Невдала спроба реєстрації (користувач із вказаним email уже існує)")
            else:
                db_handler = DbSyncHandler()
                user_id = form_data.get("user_id", "")
                email = form_data.get("email", "@")
                to_pay = form_data.get("last_bill", "")
                user_obj, status = db_handler.fetch_user_info(user_id, email, to_pay)
                if status=="user_id":
                    self._errors["user_id"] =\
                        ['Користувач із вказаним номером контракту відсутній в базі данних']
                    write_log(user=user_id,
                              place="Реєстрація",
                              msg_type="Невдало",
                              message="Невдала спроба реєстрації (користувач із вказаним id не доступний)")
                if status=="to_pay":
                    self._errors["last_bill"] =\
                        ['Не вірна сума останнього рахунку']
                    write_log(user=user_id,
                              place="Реєстрація",
                              msg_type="Невдало",
                              message="Невдала спроба реєстрації (вказано невірну суму до оплати {})".format(to_pay))
