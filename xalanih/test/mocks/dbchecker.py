class DBChecker:

    def __init__(self, exists=True, last_patch=None):
        self.exists = exists
        self.last_patch = last_patch

    def check_db_exists(self):
        return self.exists

    def check_last_update(self):
        return self.last_patch
