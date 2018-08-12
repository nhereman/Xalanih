class RequestHandler:

    def request_xalanih_table(self):
        """
        Returns the request to check if the Xalanih table exists.
        """
        raise Exception("RequestHandler is an abstract and " 
                "should not be called directly.")

    def request_xalanih_table_creation(self):
        """
        Returns the request that create the Xalanih table.
        """
        raise Exception("RequestHandler is an abstract and " 
                "should not be called directly.")

    def request_update_recording(self):
        """
        Returns the request that insert an update.
        """
        raise Exception("RequestHandler is an abstract and " 
                "should not be called directly.")

    def request_update(self):
        """
        Returns the request that select an update.
        """
        raise Exception("RequestHandler is an abstract and " 
                "should not be called directly.")
