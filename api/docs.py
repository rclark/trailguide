from django.shortcuts import render
from django.http import Http404

def docs(request, doc_name):
    """Render Swagger documentation"""
    # Default doc
    if doc_name == "":
        doc_name = "swagger.html"

    # Check that the request in valid
    available_docs = [
        "swagger.html",
        "api-docs.json",
        "segment.json",
        "route.json",
        "pointofinterest.json",
        "region.json",
        "trailhead.json"
    ]

    if doc_name not in available_docs:
        raise Http404

    # Setup context
    host = "http://%s/api/" % request.META.get("HTTP_HOST", "127.0.0.1:8000").rstrip("/")
    discovery = host + "docs/api-docs.json"
    context = { "host": host, "discovery": discovery }

    # Get the correct template and content type
    template = "trailguide/api/docs/%s" % doc_name
    mime = "text/html" if doc_name == "swagger.html" else "application/json"

    return render(request, template, context, content_type=mime)