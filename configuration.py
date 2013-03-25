from django.contrib.sites.models import Site

def apply_site_parameters(request):
    """
    This function can be used to apply some site-wide configuration parameters to template context
    
    Use this by adding a call to this function in settings.py:
    """
    return {
        "domain": Site.objects.get_current().domain, # Maybe this is dumb
        "site_title": "Tucson Trail Guide"
    }
    