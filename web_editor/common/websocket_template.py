from rest_framework.exceptions import MethodNotAllowed

class WebsocketTemplate:
    VALID_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    VALID_ENDPOINTS = ["/objects/"]
    
    @classmethod
    def construct_message(self, method, endpoint="/", url_params={}, query_params={}, data={}):
        if method not in self.VALID_METHODS: # TODO check valid format
            raise MethodNotAllowed("Invalid method")
        message = {
            "method": method,
            "endpoint": endpoint,
            "url_params": url_params,
            "query_params": query_params,
            "data": data
        }
        return message