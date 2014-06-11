from json import dumps, loads


class Response():

    def __init__(self):
        self.content = None
        self.type = "empty"
        self.exception = None

    def unwrap(self):
        if self.exception:
            raise self.exception
        return self.content

    def serialize(self):
        e = None
        if self.exception:
            e = {
                "type": type(self.exception).__name__,
                "msg": str(self.exception)
            }
        d = {
            "content": self.content,
            "type": self.type,
            "exception": e,
        }
        return dumps(d, indent=4, sort_keys=True)


def GoodResponse(x):

    def verify_keys_in_dicts(x):
        if not isinstance(x, dict):
            return True
        for y in x.keys():
            if not isinstance(y, str):
                return False
            if not verify_keys_in_dicts(x[y]):
                return False
        return True

    r = Response()
    r.type = type(x).__name__
    try:
        dumps(x)
    except Exception:
        if not hasattr(x, "to_json"):
            raise Exception("Must be a JSON friendly type, "
                            "or have a 'to_json()' at least")
        x = x.to_json()

    if not verify_keys_in_dicts(x):
        raise Exception("All keys in dicts must be string")

    r.content = x
    r.exception = None
    return r


def BadResponse(e):
    r = Response()
    r.type = "exception"
    r.exception = e
    return r


def DetailsResponse(cluster_type=None):
    r = Response()
    r.content = {}
    r.content["cluster_type"] = cluster_type
    r.type = "details"
    return r


def JsonResponse(xs):
    try:
        x = loads(xs)
    except Exception as e:
        return BadResponse(e)
    r = Response()
    r.content = x["content"]
    r.type = x["type"]
    r.exception = x["exception"]
    if r.exception:
        ext = get_exception_type(r.exception["type"])
        r.exception = ext(r.exception["msg"])
    return r


def get_exception_type(s):
    # TODO: HACK: SUPER UNSAFE
    ext = eval(s)
    if isinstance(ext(), BaseException):
        return ext
    return Exception
