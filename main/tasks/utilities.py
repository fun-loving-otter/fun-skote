class MagicGetter:
    def __init__(self, data):
        self.data = data

    def get(self, keys):
        try:
            result = self.data
            for key in keys:
                result = result[key]
            return result
        except (KeyError, TypeError, IndexError):
            return None
