class WebsocketTemplate:
    VALID_METHODS = ["GET", "POST", "PUT"]
    VALID_ENDPOINT_FORMAT = r"/./"
    
    @classmethod
    def construct_message(self, method, endpoint, data):
        if method not in self.VALID_METHODS: # TODO check valid format
            return False
        message = {
            "method": method,
            "endpoint": endpoint,
            "data": data
        }
        return message