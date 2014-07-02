import unittest
from unittest import mock

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from apy2.response.response import *

class TestResponse(unittest.TestCase):  # pragma: no cover

    def setUp(self):
        pass

    def test_base_response_must_be_empty_by_default(self):
        r = Response()
        self.assertIsInstance(r, Response)
        self.assertIsNone(r.content)
        self.assertEqual(r.type, "empty")
        self.assertIsNone(r.exception)

    def test_cant_pass_parameters_to_base(self):
        with self.assertRaises(Exception):
            Response(78)

    def test_good_response(self):
        r = GoodResponse(89)
        self.assertEqual(r.content, 89)
        self.assertIsNone(r.exception)
        self.assertEqual(r.type, "int")

    def test_unwrap(self):
        r = GoodResponse(79)
        self.assertEqual(r.unwrap(), 79)

    def test_good_many_types(self):
        many = [2, "a", "8989-a",
                [2, 9], [3, "90"],
                0.21, {"a": 90, "2": "bbb"},
                False, None, True]
        for x in many:
            r = GoodResponse(x)
            self.assertEqual(r.content, x)

    def test_json_unfriendly_response(self):
        class HateJson():
            pass
        with self.assertRaises(Exception):
            GoodResponse(HateJson())

    def test_json_friendly_response(self):
        class LoveJson():

            def to_json(self):
                return {}
        r = GoodResponse(LoveJson())
        self.assertEqual(r.content, {})
        self.assertEqual(r.type, "LoveJson")

    def test_good_response_serialize(self):
        r = GoodResponse({"num": 89, "y": True, "l": [3.14159, None]})
        j = r.serialize()
        self.assertEqual(j, '{'
                            '\n    "content": {'
                            '\n        "l": ['
                            '\n            3.14159, '
                            '\n            null'
                            '\n        ], '
                            '\n        "num": 89, '
                            '\n        "y": true'
                            '\n    }, '
                            '\n    "exception": null, '
                            '\n    "type": "dict"'
                            '\n}')

    def test_bad_response_serialize(self):
        class MyException(Exception):
            pass
        r = BadResponse(MyException("Ho ho ho"))
        s = r.serialize()
        self.assertEqual(s, '{\n'
                            '    "content": null, \n'
                            '    "exception": {\n'
                            '        "msg": "Ho ho ho", \n'
                            '        "type": "MyException"\n'
                            '    }, \n'
                            '    "type": "exception"\n'
                            '}')

    def test_bad_response(self):
        e = Exception("Alacazam")
        r = BadResponse(e)
        self.assertIsInstance(r, Response)
        self.assertEqual(r.type, "exception")
        self.assertIsNone(r.content)
        self.assertEqual(r.exception, e)

    def test_details_response(self):
        r = DetailsResponse()
        self.assertIsInstance(r, Response)
        self.assertEqual("details", r.type)
        self.assertIn("cluster_type", r.content)
        # TODO: add more details

    def test_unwrap_goes_bad(self):
        e = Exception("This will break bad")
        r = BadResponse(e)
        with self.assertRaisesRegex(Exception, "This will break bad"):
            r.unwrap()

    def test_response_cant_have_other_than_string_as_dict_key(self):
        with self.assertRaises(Exception):
            GoodResponse({9: "0000"})


class TestSerializedResponse(unittest.TestCase):  # pragma: no cover

    def test_unserialize(self):
        original = "I'm scary"
        r = GoodResponse(original)
        s = r.serialize()
        r2 = JsonResponse(s)
        self.assertIsInstance(r2, Response)
        self.assertEqual(r.type, r2.type)
        self.assertEqual(original, r2.content)

    def test_bad_unserialize(self):
        r2 = JsonResponse("$a$s\rdh\n98n#w##ua\nBBaB4FFx00")
        self.assertIsInstance(r2, Response)
        self.assertEqual(r2.type, "exception")

    def test_unserialize_bad(self):
        r = BadResponse(Exception("I shall pass"))
        s = r.serialize()
        r2 = JsonResponse(s)
        self.assertEqual(r2.type, "exception")
        with self.assertRaisesRegex(Exception, "I shall pass"):
            raise r2.exception

    def test_raise_kindle_exceptions(self):
        r = BadResponse(TypeError("immma typo"))
        s = r.serialize()
        r2 = JsonResponse(s)
        with self.assertRaisesRegex(TypeError, "immma typo"):
            raise r2.exception
        r = BadResponse(NameError("who immam"))
        s = r.serialize()
        r2 = JsonResponse(s)
        with self.assertRaisesRegex(NameError, "who immam"):
            raise r2.exception

    @unittest.skip("Really have to do something with that eval")
    def test_python_injection(self):
        from json import dumps, loads
        r = BadResponse(Exception("oh!"))
        s = r.serialize()
        o = loads(s)
        o["exception"]["type"] = "lambda x=2: Exception('Shit happens')"
        s = dumps(o)
        with self.assertRaisesRegex(Exception, "Shit happens"):
            r2 = JsonResponse(s)
            r2.unwrap()
        self.fail("Shit must not happen")

    def test_good_many_types(self):
        many = [2, "a", "8989-a",
                [2, 9], [3, "90"],
                0.21, 89,
                False, None, True]
        for x in many:
            r = JsonResponse(GoodResponse(x).serialize())
            self.assertEqual(r.content, x)

    def test_json_is_fine_but_is_incomplete(self):
        r2 = JsonResponse('{"imma": "cheatin yo"}')
        with self.assertRaisesRegex(Exception, "Exception format error: *"):
            r2.unwrap()

if __name__ == "__main__":
    unittest.main()
