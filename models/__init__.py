"""Models that persist information about trails"""
from description import Description
from pointofinterest import PointOfInterest
from region import Region
from route import Route
from segment import Segment
from trailhead import Trailhead
from comment import Comment
from profile import UserProfile
from upload import UserUpload

trail_conditions = (
    (1, "Easy"),
    (2, "Fucking Terrible")
)

difficulties = (
    (1, "Simple"),
    (2, "All night long")
)