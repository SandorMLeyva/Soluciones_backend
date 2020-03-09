from workshop.models import *
from django.db.models import Count, Sum
from workshop.constants.models import FINISHED
from collections import defaultdict
import datetime


# Sources
def sources_counts():
    src_counts = Source.objects.annotate(count=Count('client__source'))
    return src_counts

def workers_earnings():
    wkrs_earnings = defaultdict(float)
    for x in Service.objects.all():
        wkrs_earnings[x.user.username] += x.fix.total_price()
    for x in RoadService.objects.all():
        wkrs_earnings[x.user.username] += x.fix.total_price()
    return wkrs_earnings.items()

def work_completion_stats():
    services = Service.objects.all().count()
    completed_servs = Service.objects.filter(state=FINISHED).count()
    rservices = RoadService.objects.all().count()
    completed_rservs = RoadService.objects.filter(state=FINISHED).count()
    return {
        'completed_services': completed_servs,
        'uncompleted_services': services - completed_servs,
        'completed_roadservices': completed_rservs,
        'uncompleted_roadservices': rservices - completed_rservs
    }

def works_per_years():
    works = defaultdict(int)
    for s in Service.objects.all():
        works[s.date.year]+=1
    for s in RoadService.objects.all():
        works[s.datetime.year]+=1
    works = zip(works.keys(), works.values())
    works = list(works)
    works.sort(key = lambda x: int(x[0]))
    return [[x for x,_ in works], [y for _,y in works]]

def works_per_months():
    works = defaultdict(int)
    for s in Service.objects.all():
        works[str(s.date.month) + "-" + str(s.date.year)]+=1
    for s in RoadService.objects.all():
        works[str(s.datetime.month) + "-" + str(s.datetime.year)]+=1
    works = zip(works.keys(), works.values())
    works = list(works)
    works.sort(key = lambda x: int(x[0].split('-')[0]) + 365 * int(x[0].split('-')[1]))
    return [[x for x,_ in works], [y for _,y in works]]

def works_during_week(week):
    week_start = datetime.datetime.strptime(week, '%Y-%m-%d')
    week_end = week_start + datetime.timedelta(days=7)
    works = Service.objects.filter(date__lte=datetime.datetime.strftime(week_end, "%Y-%m-%d")) \
                           .filter(date__gte=(week_start)).count()
    works += RoadService.objects.filter(datetime__lte=datetime.datetime.strftime(week_end, "%Y-%m-%d")) \
                           .filter(datetime__gte=(week_start)).count()
    return datetime.datetime.strftime(week_start, "%Y/%m/%d") + " - " + datetime.datetime.strftime(week_end, "%Y/%m/%d"), works


def money_per_years():
    money = defaultdict(int)
    for x in Service.objects.all():
        money[x.date.year] += x.fix.total_price()
    for x in RoadService.objects.all():
        money[x.datetime.year] += x.fix.total_price()
    money = zip(money.keys(), money.values())
    money = list(money)
    money.sort(key = lambda x: int(x[0]))
    return [[x for x,_ in money], [y for _,y in money]]

def money_per_months():
    money = defaultdict(int)
    for s in Service.objects.all():
        money[str(s.date.month) + "-" + str(s.date.year)] += s.fix.total_price()
    for s in RoadService.objects.all():
        money[str(s.datetime.month) + "-" + str(s.datetime.year)] += s.fix.total_price()
    money = zip(money.keys(), money.values())
    money = list(money)
    money.sort(key = lambda x: int(x[0].split('-')[0]) + 365 * int(x[0].split('-')[1]))
    return [[x for x,_ in money], [y for _,y in money]]

def money_during_week(week):
    week_start = datetime.datetime.strptime(week, '%Y-%m-%d')
    week_end = week_start + datetime.timedelta(days=7)
    money = sum ([x.fix.total_price() for x in Service.objects.filter(date__lte=datetime.datetime.strftime(week_end, "%Y-%m-%d")) \
                                                        .filter(date__gte=(week_start))])
    money += sum ([x.fix.total_price() for x in RoadService.objects.filter(datetime__lte=datetime.datetime.strftime(week_end, "%Y-%m-%d")) \
                                                        .filter(datetime__gte=(week_start))])
    return datetime.datetime.strftime(week_start, "%Y/%m/%d") + " - " + datetime.datetime.strftime(week_end, "%Y/%m/%d"), money

