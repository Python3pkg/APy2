from ..core.api import Api
from ..core.context import Context
from ..response.response import DetailsResponse


def CreateLocalConnector(x):
        if isinstance(x, Api):
            return LocalApiConnector(x)
        elif isinstance(x, Context):
            return LocalContextConnector(x)
        else:
            raise Exception("TODO: EXCEPTION")


class ApiConnector():

    def __init__(self, *args, **kwargs):
        pass

    def details(self):
        pass


class LocalApiConnector(ApiConnector):

    def __init__(self, api):
        pass


class ContextConnector():

    pass


class LocalContextConnector(ContextConnector):

    def __init__(self, context):
        self._context = context

    def details(self):
        return DetailsResponse("context").unwrap()

    def get_function(self, name):
        try:
            return self._context.__dict__[name]
        except KeyError:
            raise Exception("Context do not have function " + str(name))

    def __enter__(self):
        return LocalContext(self._context)

    def __exit__(self, ty, val, trace):
        pass

    def list_functions(self):
        d = {}
        l = self._context._api.find_functions(context=self._context._context)
        for f in l:
            d[f.name] = f
        return d


class LocalContext():

    def __init__(self, wrapped_context):
        self.__wrapped_context = wrapped_context

    def __getattr__(self, key):
        try:
            return self.__wrapped_context.__dict__[key]
        except KeyError:
            raise Exception("Context do not have function " + str(key))
