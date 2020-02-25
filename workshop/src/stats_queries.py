from workshop.models import *
from django.db.models import Count, Sum


# Sources
def sources_counts():
    src_counts = Source.objects.annotate(count=Count('client__source'))
    return src_counts

def workers_earnings():
    wkrs_earnings = User.objects.annotate(sum=Sum('service__fix__base_price'), road_sum=Sum('roadservice__fix__base_price'))
    return wkrs_earnings