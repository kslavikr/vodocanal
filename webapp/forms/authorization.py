from django.forms import (ModelForm, Form, ModelChoiceField, EmailField,
                          CharField, ChoiceField, FloatField, PasswordInput)               
from django.forms.widgets import Textarea, Select
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from webapp.utilities.db_handler import DbSyncHandler
from webapp.utilities.log_handler import write_log


class AuthorizationForm(Form):

    user_id = CharField(label="Номер особового рахунку (Контракту)",
                        max_length=500,
                        required=True,
                        error_messages={'required':
                                        "Це поле є обов'язковим"},
                        help_text="Номер присвоєний клієнту водоканалом")
                        
    password = CharField(label="Пароль",
                         max_length=500,
                         required=True,
                         error_messages={'required':
                                         "Це поле є обов'язковим"},
                         help_text="Введіть в поле свій пароль")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].widget.attrs['class'] = "form-control"
        self.fields['password'].widget = PasswordInput()
        self.fields['password'].widget.attrs['class'] = "form-control"

    def clean(self):
        '''Method validates form fields'''
        form_data = self.cleaned_data
        user_id = form_data.get("user_id", "")
        password = form_data.get("password", "")
        print(user_id, password)
        user = authenticate(username=user_id, password=password)
        print(user)
        if not user:
            write_log(user=user_id,
                      place="Вхід",
                      msg_type="Невдало",
                      message="Невдала спроба Входу (введений пароль {})".format(password))
            self._errors["user_id"] =\
                ['Номер контракту, або пароль введено неправильно']
        return form_data
