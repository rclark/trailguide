from django.db.models.loading import get_model
from django.http import HttpResponseNotAllowed, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize, deserialize
from django.core.serializers.base import DeserializationError
import json

# -------------------------------------------------------------------
#    Functions that respond to urls - we'll revisit csrf later
# -------------------------------------------------------------------
@csrf_exempt
def single(request, model_name, pk):
    """Dispatch API requests related to a single resource"""
    single = SingleController(request, model_name, pk)
    return single.http_response

@csrf_exempt
def collection(request, model_name):
    """Dispatch API requests related to a collection of resources"""
    collection = CollectionController(request, model_name)
    return collection.http_response

# -------------------------------------------------------------------
#    Classes to manage the work of constructing the responses
# -------------------------------------------------------------------
class BaseController(object):
    """A base class for controllers that respond to API requests"""
    # Derivative classes should override to indicate what requests are acceptable
    allowed = ["GET", "PUT", "POST", "DELETE"]
    
    def __init__(self, request, model_name, pk=None):
        # Pass kwargs into instance object
        self.request = request
        self.model_name = model_name
        self.model = get_model('trailguide', model_name)
        self.pk = pk
        
        # Check that the requested model name was valid
        if not self.model:
            raise Http404
        
        # Check that the requested method is allowed
        if not self._method_allowed():
            self.http_response = HttpResponseNotAllowed(self.allowed)
        
        # Find models relevant to this request
        self.models = self._filtered_set()
        
    def _method_allowed(self):
        """Determine if the request is an allowed method"""
        if self.request.method not in self.allowed:
            return False
        else:
            return True
        
    def _serialize(self, queryset):
        """Serialize a queryset as JSON"""
        json_string = serialize("json", queryset)
        
        # If there is only one object, pull it out
        if queryset.count() == 1:
            collection = json.loads(json_string)
            json_string = json.dumps(collection[0])
        
        return json_string
            
    def _filtered_set(self):
        """Inspect the request and generate a list of model instances that match"""
        # If a primary key has been identified, that constrains the query
        if self.pk:
            return self.model.objects.filter(pk=self.pk)
        
        # Otherwise, use URL query parameters to filter
        # Find keys in the query that are also fields in the model
        query_keys = [ key for key in self.request.GET.keys() if key in self.model._meta.get_all_field_names() ]
        query_params = {}
        for key in query_keys:
            query_params[key] = self.request.GET[key]
        return self.model.objects.filter(**query_params)
        
    def view_models(self):
        """Serialize the filtered set of models and return them as an HttpResponse"""
        json_string = self._serialize(self.models)
        return HttpResponse(json_string, content_type="application/json")
    
    def _validate_post_data(self):
        """Validate that the POST data is correct and return a DeserializedObject, None if body is invalid"""
        try:
            for obj in  deserialize("json", self.request.body):
                print(obj)
        except DeserializationError as err:
            return None
        # Do any additional validation of the deserialized object before returning it
        return obj
    
    def _create_new_model(self):
        """Generate and return a new model instance based on the POST body"""
        new_model = self._validate_post_data()
        new_model.save()
        return new_model
    
    def new_model(self):
        """Generate a new instance of the model and return an HttpResponse with the URL for it"""
        model = self._create_new_model()
        response = HttpResponse()
        response["Location"] = "/api/%s/%s/" % ( self.model_name, model.pk )
        return response
    
    def del_model(self):
        """Destroy an existing instance of the model and return the proper HTTP response"""
        self.model.delete()
        response = HttpResponse(status=204)
        return response
    
class CollectionController(BaseController):
    """A controller for API requests to collections of models"""
    acceptable = ["GET", "POST"]
    
    def __init__(self, request, model_name):
        # Call the base constructor
        super(CollectionController, self).__init__(request, model_name, None)
        
        # Bail if we already have an http_response
        if getattr(self, "http_response", None):
            return
        
        # Dispatch the request
        if request.method == "GET":
            self.http_response = self.view_models() 
        elif request.method == "POST":
            self.http_response = self.new_model()
    
class SingleController(BaseController):
    """A controller for API requests to a single instance of models"""
    acceptable = ["GET", "PUT", "DELETE"]
    
    def __init__(self, request, model_name, pk):        
        super(CollectionController, self).__init__(request, model_name, pk)        
        if getattr(self, "http_response", None):
            return
        
        if request.method == "GET":
            self.http_response = self.view_models() 
        elif request.method == "PUT":
            self.http_response = self.new_model()
        elif request.method == "DELETE":
            self.http_response = self.del_model()    
    