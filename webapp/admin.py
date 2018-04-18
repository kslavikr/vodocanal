from django.contrib import admin
from webapp.models import (UsersDetailModel,
                           DefaultSettingModel,
                           # DbInfo,
                           # ContractId,
                           # CountersValues,
                           # Payments,
                           LogModel)

admin.site.register(UsersDetailModel)
# admin.site.register(DbInfo)
# admin.site.register(ContractId)
# admin.site.register(CountersValues)
# admin.site.register(Payments)
admin.site.register(LogModel)
admin.site.register(DefaultSettingModel)