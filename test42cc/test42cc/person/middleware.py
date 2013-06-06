from models import HttpStoredQuery

class HttpStoredQueryMiddleware:
    def process_request(self, request):
        req = HttpStoredQuery()
        req.path = request.path
        req.method = request.method
        if request.user.is_authenticated():
           req.user = request.user
        req.save()
        return None

