import string
import random
import datetime
# import os
from django.views.generic import View, TemplateView, FormView
# from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from webapp.models import (UsersDetailModel,
                           DefaultSettingModel,
                           LogModel,
                           # DbInfo, ContractId,
                           # CountersValues
                           )
from webapp.forms.registration import RegistrationeForm
from webapp.forms.authorization import AuthorizationForm
from webapp.forms.counter_value import SetCounterValForm
from webapp.forms.restore_pass import PassRestoreForm
from webapp.forms.chenge_pass import PassChengeForm
from webapp.utilities.db_handler import DbSyncHandler
from webapp.utilities.log_handler import write_log
from webapp.utilities.site_util import allow_update
from countersweb.settings import host_url

class UserRegistration(FormView):
    template_name = "registration.html"
    form_class = RegistrationeForm
    success_url = reverse_lazy("user_authorization")

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, ("Вітаємо з реєстрацією. Пароль до Вашого"
                                        " облікового запису було відправлено на"
                                        " вказану при реєстрації адресу"
                                        " електронної скриньки"))
        return super().form_valid(form)


class UserAutorization(FormView):
    template_name = "authorization.html"
    form_class = AuthorizationForm
    success_url = reverse_lazy("counters_info")
    

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get("logout", False):
            user_pk = request.user.pk
            logout(request)
            write_log(user=user_pk,
                      place="Вихід",
                      msg_type="Успішно",
                      message="Користувач {} вилогувався із системи".format(request.user.pk))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id", "")
        password = form.cleaned_data.get("password", "")
        user = authenticate(username=user_id, password=password)
        login(self.request, user)
        write_log(user=user.pk,
                  place="Вхід в систему",
                  msg_type="Успішно",
                  message="Користувач {} увійшов в систему".format(user.pk))
        # db_handler = DbSyncHandler()
        # db_handler.sync_user_info(user)
        return super().form_valid(form)


class UserCountersInfo(TemplateView):
    template_name = "counters_list.html"

    @method_decorator(login_required(login_url="/authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        if user_obj:
            # print(self.request)
            if not user_obj.is_superuser:
                counters_info = self._get_sql_counters_info(user_obj)
                context['counters_info'] = counters_info
                user_payments = self._get_payments_info(user_obj)
                context['user_payments'] = user_payments
                context['bill_info'] = self._get_bill_info(user_obj,user_payments,counters_info)
                context['user_detail'] = get_user_details(user_obj)
                context['to_pay_info'] = self._get_topay_info(user_payments)
                context['allow_add'] = allow_update()
            else:
                userd_id_access = self.request.GET.get("id",'')
                if not userd_id_access:
                    userd_id_access = DefaultSettingModel.objects.get(param="default_id").value
                else:
                    default_id = DefaultSettingModel.objects.get(param="default_id")
                    default_id.value = userd_id_access
                    default_id.save()
                if userd_id_access:
                    print("Admin Access for - ",userd_id_access)
                    user_obj = User.objects.get(pk=userd_id_access)
                    counters_info = self._get_sql_counters_info(user_obj)
                    context['counters_info'] = counters_info
                    user_payments = self._get_payments_info(user_obj)
                    context['user_payments'] = user_payments
                    context['bill_info'] = self._get_bill_info(user_obj, user_payments,counters_info)
                    context['user_detail'] = get_user_details(user_obj)
                    context['to_pay_info'] = self._get_topay_info(user_payments)
                    context['allow_add'] = False
                    context['user_identity'] = userd_id_access
        return context

    def _get_topay_info(self, all_payments):
        monthDict = {0:'грудні', 1:'січні', 2:'лютому', 3:'березні', 4:'квітні',
                     5:'травні', 6:'червні', 7:'липні', 8:'серпні',
                     9:'вересні', 10:'жовтні', 11:'листопаді', 12:'грудні'}
        if all_payments:
            last_topay = all_payments[0]
            to_pay = 0
            if last_topay.to_pay and last_topay.to_pay < 0:
                to_pay = abs(last_topay.to_pay)
            return {"to_pay": to_pay,
                    "month": monthDict[last_topay.date_added.month]}
        return {"to_pay": 0,
                "month": monthDict[datetime.datetime.now().month]}
            

    # def _get_counters_info(self, user_obj):
    #     contracts_query = ContractId.objects.filter(user=user_obj).order_by("contract_descr")
    #     counters_info = []
    #     for contract in contracts_query:
    #         contract_val = CountersValues.objects.filter(contract=contract).order_by("-registration_time")
    #         counters_info.append({"contract":contract,
    #                               "value":contract_val})
    #     return counters_info

    def _get_sql_counters_info(self, user_obj):
        counters_info = DbSyncHandler()._get_sql_user_contracts(user_obj)
        return counters_info

    def _get_payments_info(self, user_obj):
        user_payments = DbSyncHandler()._get_sql_payments(user_obj)
        return user_payments

    def _maximum_value(self, value1, value2):
        if value1:
            if value2:
                return max(value1, value2)
            else:
                return value1
        else:
            return value2

    def _get_bill_info(self, user_obj ,user_payments, counters_info_input):
        user_name = user_obj.first_name
        user_detail_obj = UsersDetailModel.objects.get(user=user_obj)
        town = "м." + user_detail_obj.town if user_detail_obj.town else ""
        street = "вул." + user_detail_obj.street if user_detail_obj.street else ""
        house = "буд." + user_detail_obj.house if user_detail_obj.house else ""
        appartment = "кв." + user_detail_obj.appartment if user_detail_obj.appartment else ""
        user_last_calc_payment = 0
        payment = None
        if user_payments:
            payment = user_payments[0]
            for payment_item in user_payments:
                if payment_item.calc_to_pay!=0:
                    user_last_calc_payment = payment_item
                    break
        print(payment)
        # print(user_last_calc_payment)
        # print(user_last_calc_payment.date_added.year)
        # print(user_last_calc_payment.date_added.month)

        current_year = user_last_calc_payment.date_added.year
        current_month = user_last_calc_payment.date_added.month
        if current_month == 1:
            previous_year = current_year - 1
            previous_month = 12
        else:
            previous_year = current_year
            previous_month = current_month - 1

        counters_info = []
        current_counter = None
        previous_counter = None
        for contract in counters_info_input:
            for contract_value in contract["value"]:
                if contract_value.registration_time.year == current_year:
                    if contract_value.registration_time.month == current_month:
                        current_counter= contract_value
                        break
            for contract_value in contract["value"]:
                if contract_value.registration_time.year == previous_year:
                    if contract_value.registration_time.month == previous_month:
                        previous_counter = contract_value
                        break
            if current_counter:
                contract_val_current = self._maximum_value(current_counter.value_vodocanal,current_counter.value_user)
            else:
                contract_val_current = 0
            if previous_counter:
                contract_val_previous =self._maximum_value(previous_counter.value_vodocanal,previous_counter.value_user)
            else:
                contract_val_previous = 0
            counters_info.append({"contract": contract["contract"],
                                  "current_value": contract_val_current,
                                  "previous_value": contract_val_previous})
        return {"user_id":user_obj.pk,
                "user_name":user_name,
                "addres":town+" "+street+" "+house+" "+appartment,
                "payment":payment,
                "calc_payment":user_last_calc_payment,
                "counters":counters_info}
        
    
class CounterValueSet(FormView):
    template_name = "set_counter_val.html"
    form_class = SetCounterValForm
    success_url = reverse_lazy("counters_info")

    @method_decorator(login_required(login_url="/authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({
    #         'initial': {
    #             'user_id': self.request.user.pk
    #         }
    #     })
    #     return kwargs

    def get_initial(self):
        initial_dict = super().get_initial()
        initial_dict.update({'counter_id': self.request.GET.get('id')})
        initial_dict["user_id"] = self.request.user.pk
        return initial_dict

    def form_valid(self, form):
        counter_id = form.cleaned_data.get("counter_id", "")

        counter_val = form.cleaned_data.get("counter_val", "")

        user_id = self.request.user.pk
        db_handler = DbSyncHandler()
        contracts = db_handler._get_sql_user_contracts_by_id(user_id, counter_id)[0]
        origin_user = contracts["contract"].user

        if origin_user==user_id:
            counter_vals = contracts["value"]
            if counter_vals:
                if counter_vals.value_vodocanal:
                    last_val = counter_vals.value_vodocanal
                else:
                    last_val = None
            counter_id_db = contracts["contract"].contract_id
            time = datetime.datetime.now()
            if allow_update():
                result = db_handler.save_counter_value(user_id, counter_id_db, counter_val, time, last_val)
            else:
                result = False
            if result:
                write_log(user=self.request.user.pk,
                          place="Подання Показника",
                          msg_type="Успішно",
                          message="Подано показник. Лічильник - {}, показник - {}".format(counter_id_db, counter_val))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = get_user_details(self.request.user)
        context['allow_add']=allow_update()
        return context

class RestorePass(FormView):
    template_name = "restore_pass.html"
    form_class = PassRestoreForm
    success_url = reverse_lazy("user_authorization")

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id", "")
        user_obj = User.objects.get(pk=user_id)
        user_email = user_obj.email
        new_pass = self._generate_pass()
        print("NEW PASS = ", new_pass)
        user_obj.set_password(new_pass)
        user_obj.save()
        self._send_email_reg(user_obj, new_pass)
        write_log(user=user_obj.pk,
                  place="Відновлення Паролю",
                  msg_type="Успішно",
                  message="Відновлено пароль. Пароль {} відправлено на {}".format(new_pass, user_email))
        messages.success(self.request, ("Ваш пароль було змінено. Новий пароль відправлено на " + user_email))
        return super().form_valid(form)

    def _generate_pass(self, size=8,
                       chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def _send_email_reg(self, user_obj, user_pass):
        subject = "Restore password Success"
        text = ("Лічильники вітають Вас \n" +
                "Ваш логін - " + str(user_obj.pk) + "\n" +
                "Новий пароль - " + str(user_pass) + "\n"+
                "Спробуйте залогуватись на сторінці - <a href='"+host_url+"'>ВХІД</a>" +"\n")
        html_mess = ("Лічильники вітають Вас <BR>" +
                "Ваш логін - " + str(user_obj.pk) + "<BR>" +
                "Новий пароль - " + str(user_pass) + "<BR>"+
                "Спробуйте залогуватись на сторінці - <a href='"+host_url+"'>ВХІД</a>" +"<BR>")
        sender = '"Vodokanal" <vodokanal@forever.in.net>'
        html_mess = "<!DOCTYPE html><html><head> </head><body>"+html_mess+" </body></html>"
        try:
            print("TRY TO SEND EMAIL")
            send_mail(subject, text, sender, [user_obj.email], html_message=html_mess)
        except BaseException as e:
            print("ERROR DURING SEND EMAIL")
            print(e)

class HelpPageInfo(TemplateView):
    template_name = "help.html"

    # @method_decorator(login_required(login_url="/authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("counters_info"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = get_user_details(self.request.user)
        return context

class AdminPanelPage(TemplateView):
    template_name = "admin_tool.html"

    # @method_decorator(login_required(login_url="/authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse_lazy("counters_info"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            # context['users'] = [user.pk for user in User.objects.all()]
            context['logs'] = LogModel.objects.order_by('-date_added')[:500]
            # context['link'] = "http://"+self.request.META.get("HTTP_HOST")+"/counters/info?id="
        return context

class UserChengePass(FormView):
    template_name = "chenge_pass.html"
    form_class = PassChengeForm
    success_url = reverse_lazy("counters_info")
    

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_obj = self.request.user
        new_pass = form.cleaned_data.get("new_pass", "")
        user_obj.set_password(new_pass)
        user_obj.save()
        write_log(user=user_obj.pk,
                  place="Зміна Паролю",
                  msg_type="Успішно",
                  message="Успішно змінено пароль. Новий пароль - {}".format(new_pass))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = get_user_details(self.request.user)
        return context


def get_user_details(user_obj):
    print(user_obj.is_anonymous)
    if not user_obj.is_anonymous:
        print("Not Anonymus")
        user_detail = UsersDetailModel.objects.filter(user=user_obj)
        if user_detail:
            return user_detail.first()
    return None