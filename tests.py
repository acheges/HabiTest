try:
    from App import app
    import unittest
except Exception as e:
    print(f"There must be a missing module =>{e}")

class FlaskTest(unittest.TestCase):
    """Verifying the response 200 status"""
    def test_index(self):
        testresponse = app.test_client(self)
        response = testresponse.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_responsetype(self):
        """Verifying the response type"""
        testresponse = app.test_client(self)
        response = testresponse.get("/api/v1/updatedproperties")
        self.assertEqual(response.content_type, "application/json")

    def test_responselen(self):
        """Verifying the response len"""
        testresponse = app.test_client(self)
        response = testresponse.get("/api/v1/updatedproperties")
        self.assertGreater(len(response.json),2 )

    def test_non_response(self):
        """Verifying Null response example"""
        testresponse = app.test_client(self)
        response = testresponse.get("http://127.0.0.1:3000/api/v1/updatedproperties?city=moscu")
        self.assertTrue(b'no results for this query' in response.data)

    def test_returned(self):
        """Verifying the response example"""
        testresponse = app.test_client(self)
        response = testresponse.get("/")
        self.assertTrue(b'Habi' in response.data)


if __name__ == "__main__":
    unittest.main()