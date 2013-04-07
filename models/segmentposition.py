from django.db import models

class SegmentPosition(models.Model):
    """Correlates segments to trails in a particular order"""
    class Meta:
        app_label = "trailguide"

    route = models.ForeignKey("Route")
    segment = models.ForeignKey("Segment")
    position = models.IntegerField()
    
    def save(self, *args, **kwargs):
        """On save, re-save the route (with new geometry)."""
        super(SegmentPosition, self).save(*args, **kwargs)
        self.route.create_geometry()