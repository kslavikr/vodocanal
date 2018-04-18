from django.forms import (ModelForm, Form, ModelChoiceField, EmailField,
                          CharField, ChoiceField, FloatField, DecimalField,
                          PasswordInput)               
from django.forms.widgets import Textarea, Select
from django.contrib.auth.models import User
from webapp.utilities.db_handler import DbSyncHandler
# from webapp.models import Payments


class PassChengeForm(Form):

    new_pass = CharField(label="Новий Пароль",
                        max_length=500,
                        required=True,
                        error_messages={'required':
                                        "Це поле є обов'язковим"},
                        help_text="Введіть новий пароль")

    confirmation = CharField(label="Підтвердження Паролю",
                        max_length=500,
                        required=True,
                        error_messages={'required':
                                        "Це поле є обов'язковим"},
                        help_text="Введіть новий пароль ще раз")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_pass'].widget = PasswordInput()
        self.fields['new_pass'].widget.attrs['class'] = "form-control"
        self.fields['confirmation'].widget = PasswordInput()
        self.fields['confirmation'].widget.attrs['class'] = "form-control"

    def clean(self):
        '''Method validates form fields'''
        form_data = self.cleaned_data
        self._check_pass_identity(form_data)
        return form_data

    def _check_pass_identity(self, form_data):
        new_pass = form_data.get("new_pass", "")
        confirmation = form_data.get("confirmation", "")
        print(new_pass)
        if new_pass != confirmation:
            self._errors["confirmation"] =\
                ['Пароль відрізняється від введеного вище']
        if len(new_pass) < 8:
            self._errors["new_pass"] =\
                ['Довжина паролю повинна бути не менше 8 символів']
        if not new_pass.isalnum():
            self._errors["new_pass"] =\
                ['Пароль може складатися лише з літер та цифр']

                
