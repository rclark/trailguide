from django.db import models

class SegmentPosition(models.Model):
    """Correlates segments to trails in a prticular order"""
    class Meta:
        app_label = "trailguide"

    route = models.ForeignKey("Route")
    segment = models.ForeignKey("Segment")
    position = models.IntegerField()