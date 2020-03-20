class VKError(Exception):
    def __init__(self, error_json):
        self.error_code = error_json.get('error_code')
        self.error_msg = error_json.get('error_msg')
