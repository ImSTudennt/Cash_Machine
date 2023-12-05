from django.urls import path
from payment.views import CashMachineView


app_name = "payment"
urlpatterns = [
    path("cash_machine", CashMachineView.as_view(), name="mashine"),
    path("media/<str:filename>/", CashMachineView.as_view(), name="link_pdf"),
]
