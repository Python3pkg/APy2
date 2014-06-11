from ..core.api import Api


def CreateLocalConnector(x):
        if isinstance(x, Api):
            return FullLocalConnector(x)
        elif isinstance(x, list):
            return PartialLocalConnector(x)
        else:
            raise Exception("TODO: EXCEPTION")


class LocalConnector():

    def __init__(self, *args, **kwargs):
        pass

    def details(self):
        pass


class FullLocalConnector(LocalConnector):

    def __init__(self, api):
        pass


class PartialLocalConnector(LocalConnector):

    def __init__(self, foo_list):
        pass
