from rest_framework.exceptions import MethodNotAllowed, NotFound

class WebsocketTemplate:
    VALID_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    VALID_ENDPOINTS = ["/objects/"]
    
    @classmethod
    def construct_message(self, method, endpoint="/", url_params={}, query_params={}, data={}):
        if method not in self.VALID_METHODS:
            raise MethodNotAllowed(method)
        if endpoint not in self.VALID_ENDPOINTS:
            raise NotFound("Wrong endpoint.")
        message = {
            "method": method,
            "endpoint": endpoint,
            "url_params": url_params,
            "query_params": query_params,
            "data": data
        }
        return message

    @classmethod
    def validate_message(self, request):
        method = request.get("method", None)
        if method not in self.VALID_METHODS:
            raise MethodNotAllowed(method)
        
        endpoint = request.get("endpoint", "/")
        if endpoint not in self.VALID_ENDPOINTS:
            raise NotFound("Wrong endpoint.")
        
        url_params = request.get("url_params", {})
        query_params = request.get("query_params", {})
        data = request.get("data", None)
        
        valid_request = {
            "method": method,
            "endpoint": endpoint,
            "url_params": url_params,
            "query_params": query_params,
            "data": data
        }
        
        return valid_request