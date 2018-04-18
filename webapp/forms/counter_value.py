from django.forms import (Form,
                          # ModelForm,
                          # ModelChoiceField,
                          # EmailField,
                          CharField,
                          # ChoiceField,
                          FloatField,
                          HiddenInput)
# from django.forms.widgets import Textarea, Select
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from webapp.utilities.db_handler import DbSyncHandler
# from webapp.models import (DbInfo,
#                            ContractId,
#                            CountersValues,
#                            Payments
#                            )
from webapp.utilities.log_handler import write_log


class SetCounterValForm(Form):

    counter_id = CharField(label="Ідентифікатор Лічильника",
                          max_length=500,
                          required=True,
                          error_messages={'required':
                                          "Це поле є обов'язковим"},
                          help_text="Номер присвоєний лічильнику водоканалом")
                        
    counter_val = FloatField(label="Значення Показника",
                             required=True,
                             min_value=0,
                             error_messages={'required':
                                             "Це поле є обов'язковим"},
                             help_text="Поточне значення лічильнику")


    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.get('initial').pop("user_id")
        super().__init__(*args, **kwargs)
        self.fields['counter_id'].widget.attrs['class'] = "form-control"
        self.fields['counter_id'].widget = HiddenInput()
        self.fields['counter_val'].widget.attrs['class'] = "form-control"


    def clean(self):
        '''Method validates form fields'''
        form_data = self.cleaned_data
        counter_pk = form_data.get("counter_id")
        user_id = self.user_id
        db_handler = DbSyncHandler()
        contracts_list = db_handler._get_sql_user_contracts_by_id(user_id, counter_pk)
        if contracts_list:
            contracts = contracts_list[0]
            origin_user = contracts["contract"].user

            if origin_user==user_id:
                counter_vals = contracts["value"]
                if counter_vals:
                    if counter_vals.value_vodocanal:
                        last_val = counter_vals.value_vodocanal
                    else:
                        last_val = None

                counter_val = form_data.get("counter_val")

                if last_val:
                    vals_diff = counter_val - last_val
                    if last_val > counter_val:
                        self._errors["counter_val"] =\
                            ['Показник не може бути нижчим за існуючий Для внесення корективів тел.: +38 097 281 47 28']
                        write_log(user=user_id,
                                  place="Подання Показника",
                                  msg_type="Невдало",
                                  message="Невдала спроба подати показник {} (останній зареєстрований показник {})".format(counter_val, last_val))
                    if vals_diff >= 100:
                        self._errors["counter_val"] =\
                            ['Введений показник занадто великий у порівнянні із попереднім']
                        write_log(user=user_id,
                                  place="Подання Показника",
                                  msg_type="Невдало",
                                  message="Невдала спроба подати показник {} (останній зареєстрований показник {})".format(counter_val, last_val))
            else:
                self._errors["counter_val"] = \
                    ['Некоректний номер лічильника. Спробуйте влогуватись і знову залогуватись!']
        else:
            self._errors["counter_val"] = \
                ['Некоректний номер лічильника. Спробуйте влогуватись і знову залогуватись!']

        return form_data
