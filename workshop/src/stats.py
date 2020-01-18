from workshop.models import *
from django.db.models import Q, QuerySet, Sum
import workshop.constants.models as Constants 

# Services
def services_by_year(model_s, year)->QuerySet:
    return model_s.objects.filter(date__year=year).filter(Q(state=Constants.WARRANTY) | Q(state=Constants.NO_WARRANTY))
    
def user_services_by_year(model_s, user, year)->QuerySet:
    return services_by_year(model_s, year).filter(user= user)


# Services on workshop
def services_w_by_year(year)->QuerySet:
    return services_by_year(Service, year) 

def user_services_w_by_year(user, year)->QuerySet:
    return user_services_by_year(Service, year)

def user_money_w_by_year(user, year)->int:
    services = user_services_w_by_year(user, year)
    money = 0
    for item in services:
        money += item.fix.total_price()
    return money

# Services on Road
def services_r_by_year(year)->QuerySet:
    return services_by_year(RoadService, year) 

def user_services_r_by_year(user, year)->QuerySet:
    return user_services_by_year(RoadService, year)

def user_money_r_by_year(user, year)->int:
    services = user_services_r_by_year(user, year)
    money = 0
    for service in services:
        money += service.fix.total_price()
        for sub_service in service.others_services.all():
            money += sub_service.fix.total_price()
    return money

# Workshop Stats 
def workshop_money_by_year(year):
    money = 0

    s_w = services_w_by_year(year)
    for service in s_w:
        money += service.fix.total_price()

    s_r = services_r_by_year(year)
    for service in s_r:
        money += service.fix.total_price()
        for sub_service in service.others_services.all():
            money += sub_service.fix.total_price()
    return money


# Sources




