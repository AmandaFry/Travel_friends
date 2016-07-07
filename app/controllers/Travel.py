"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Travel(Controller):
    def __init__(self, action):
        super(Travel, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.
        """
        self.load_model('Travel')
        # self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """

    def add_travel(self):
        return self.load_view('addplan.html')
