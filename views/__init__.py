from home import home_page
from map import map_page
from dashboard import dashboard_page
from route import route_page

def temp(request):
    from trailguide.models import Segment
    import json
    from django.http import HttpResponse
    seg = Segment.objects.all()[0]
    profile = seg.elevation_profile()
    profile = [ [ d[0].m, d[1].m ] for d in profile ]
    return HttpResponse(json.dumps(profile), content_type="application/json")
