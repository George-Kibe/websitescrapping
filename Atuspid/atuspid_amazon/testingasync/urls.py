from offersapp import views, coupons, daily_deals, multiple_deals
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('coupons/', coupons.home, name="coupons"),
    path('daily-deals/', daily_deals.home, name="daily_deals"),
    path('multiple-deals/', multiple_deals.home, name="multiple_deals"),
]
