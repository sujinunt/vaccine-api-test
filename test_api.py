"""Testing API service class."""
import requests
import unittest



class GovernmentApiTest(unittest.TestCase):
    """Test wcg api class for find defect."""

    def setUp(self):
        """Set up the parameters for testing."""
        self.URL = "https://wcg-apis.herokuapp.com"

    def create_url_citizen(self,citizen_id, name, surname, birth_date, occupation, address):
        """Create url for citizen."""
        return f"citizen_id={citizen_id}&name={name}&surname={surname}&birth_date={birth_date}&occupation={occupation}&address={address}"

    def test_get_all_citizen_registration(self):
        """Test get all citizen information. It should return status 200."""
        response = requests.get(self.URL+f"/registration")
        self.assertEqual(200, response.status_code)

    def test_get_citizen(self):
        """Test get valid citizen information."""
        citizen = self.create_url_citizen("1234567890147","ABCD","DEF","01/02/1992","Student","Home")
        requests.post(self.URL+f"/registration?{citizen}")
        response = requests.get(self.URL+f"/citizen/1234567890147")
        requests.delete(self.URL+f"/citizen")
        res_json = response.json()
        self.assertEqual("ABCD", res_json["name"])

    def test_get_invalid_citizen(self):
        """Test get invalid citizen information."""
        response = requests.get(self.URL+f"/citizen/123456789")
        self.assertEqual(403, response.status_code)

    def test_duplicate_registration(self):
        """Test post duplicate registration information."""
        citizen = self.create_url_citizen("1234567890147","ABC","DEF","01/02/1992","Student","Home")
        endpoint = self.URL+f"/registration?{citizen}"
        requests.post(endpoint)
        response = requests.post(endpoint)
        res_json = response.json()
        requests.delete(self.URL+f"/citizen")
        self.assertEqual("registration failed: this person already registered", res_json["feedback"])

    def test_delete_citizen_data(self):
        """Test delete all citizen."""
        requests.delete(self.URL+f"/citizen")
        response = requests.get(self.URL+f"/registration")
        res_json = response.json()
        self.assertEqual([], res_json)

    def test_not_number_citizen_id(self):
        """Test registration with citizen id that are not number."""
        citizen = self.create_url_citizen("ABC*><","ABC","DEF","01/02/1992","Student","Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: invalid citizen ID", res_json["feedback"])

    def test_less_digits_citizen_id(self):
        """Test registration with citizen id that less number than require."""
        citizen = self.create_url_citizen("123","ABC","DEF","01/02/1992","Student","Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: invalid citizen ID", res_json["feedback"])

    def test_missing_value(self):
        """Test registration with missing value."""
        citizen = self.create_url_citizen("1234567890147","ABC","DEF","","Student","Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: missing some attribute", res_json["feedback"])

    def test_invalid_birth_date(self):
        """Test registration with invalid birth date."""
        citizen = self.create_url_citizen("1234567890148","ABC","DEF","32/13/12000","Student","Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: invalid birth date format", res_json["feedback"])

    def test_get_reservation(self):
        """Test get reservation. It should return status 200."""
        response = requests.get(self.URL+f"/reservation")
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()