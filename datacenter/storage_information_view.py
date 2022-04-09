from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
import django


def storage_information_view(request):
  visits=Visit.objects.filter(leaved_at = None)
  non_closed_visits = []
  for visit in visits:
    non_closed_visits += [
        {
            "who_entered": visit.passcard,
            "entered_at": visit.entered_at,
            "duration": visit.format_duration(visit.get_duration()),
            "is_strange": visit.is_visit_long()       
          }
    ]
  context = {
      "non_closed_visits": non_closed_visits,
  }
  return render(request, 'storage_information.html', context)
