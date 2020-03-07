from workshop.models import *
from django.db.models import Count, Sum
from workshop.constants.models import FINISHED


# Sources
def sources_counts():
    src_counts = Source.objects.annotate(count=Count('client__source'))
    return src_counts

def workers_earnings():
    wkrs_earnings = User.objects.annotate(sum=Sum('service__fix__base_price'), road_sum=Sum('roadservice__fix__base_price'))
    return wkrs_earnings

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