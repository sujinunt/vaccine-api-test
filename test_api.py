"""Testing API service class."""
import requests
import unittest
from decouple import config

class GovernmentApiTest(unittest.TestCase):
    """Test wcg api class for find defect."""

    def create_url_citizen(self,citizen_id, name, surname, birth_date, occupation, phone_number, is_risk, address):
        """Create url for citizen."""
        return f"citizen_id={citizen_id}&name={name}&surname={surname}&birth_date={birth_date}&occupation={occupation}&phone_number={phone_number}&is_risk={is_risk}&address={address}"

    def create_url_vaccine(self,citizen_id, site_name, vaccine_name):
        """Create url for vaccine reserve."""
        return f"citizen_id={citizen_id}&site_name={site_name}&vaccine_name={vaccine_name}"

    def setUp(self):
        """Set up the parameters for testing."""
        self.URL = config('URL')

    def post_registration(self):
        """Post registration"""
        citizen = self.create_url_citizen("1234567890147","ABCD","DEF","01/02/1992","Student",'0818888888','False',"Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        return response

    def test_get_all_citizen_registration(self):
        """Test get all citizen information. It should return status 200."""
        response = requests.get(self.URL+f"/database/citizen")
        self.assertEqual(200, response.status_code)

    def test_get_registration_citizen(self):
        """Test get valid citizen information."""
        self.post_registration()
        response = requests.get(self.URL+f"/registration/1234567890147")
        res_json = response.json()
        requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual("ABCD", res_json['name'])

    def test_get_invalid_registration_citizen(self):
        """Test get invalid citizen information."""
        response = requests.get(self.URL+f"/citizen/123456789")
        self.assertEqual(404, response.status_code)

    def test_duplicate_registration(self):
        """Test post duplicate registration information."""
        self.post_registration()
        response = self.post_registration()
        res_json = response.json()
        requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual("registration failed: this person already registered", res_json["feedback"])

    def test_delete_registration_with_citizen_id(self):
        """Test delete registration with citizen id."""
        self.post_registration()
        response = requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual(200, response.status_code)

    def test_not_number_citizen_id(self):
        """Test registration with citizen id that are not number."""
        citizen = self.create_url_citizen("ABC*><","ABC","DEF","01/02/1992","Student",'0818888888','False',"Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: invalid citizen ID", res_json["feedback"])

    def test_less_digits_citizen_id(self):
        """Test registration with citizen id that less number than require."""
        citizen = self.create_url_citizen("123","ABC","DEF","01/02/1992","Student",'0818888888','False',"Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: invalid citizen ID", res_json["feedback"])

    def test_missing_value(self):
        """Test registration with missing value."""
        citizen = self.create_url_citizen("1234567890147","ABC","DEF","","Student",'0818888888','False',"Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: missing some attribute", res_json["feedback"])

    def test_invalid_birth_date(self):
        """Test registration with invalid birth date."""
        citizen = self.create_url_citizen("1234567890148","ABC","DEF","32/13/12000","Student",'0818888888','False',"Home")
        response = requests.post(self.URL+f"/registration?{citizen}")
        res_json = response.json()
        self.assertEqual("registration failed: invalid birth date format", res_json["feedback"])

    def test_get_reservation(self):
        """Test get reservation. It should return status 200."""
        response = requests.get(self.URL+f"/database/reservation")
        self.assertEqual(200, response.status_code)

    def test_reserve_vaccine(self):
        """Test reserve vaccine."""
        self.post_registration()
        vaccine_url = self.create_url_vaccine("1234567890147","Hospital", "Pfizer")
        response = requests.post(self.URL+f"/reservation?{vaccine_url}")
        res_json = response.json()

        requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual("reservation success!", res_json["feedback"])

    def test_reserve_vaccine_but_not_register(self):
        """Test reserve vaccine but not register."""
        vaccine_url = self.create_url_vaccine("1234567890147","Hospital", "Pfizer")
        response = requests.post(self.URL+f"/reservation?{vaccine_url}")
        res_json = response.json()
        self.assertEqual("reservation failed: citizen ID is not registered", res_json["feedback"])

    def test_reserve_vaccine_not_valid(self):
        """Test reserve vaccine that not Pfizer, Astra, Sinofarm and Sinovac."""
        self.post_registration()
        vaccine_url = self.create_url_vaccine("1234567890147","Hospital", "Vaccine*><Mกข๗")
        response = requests.post(self.URL+f"/reservation?{vaccine_url}")
        res_json = response.json()
        requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual("reservation failed: invalid vaccine name", res_json["feedback"])

    def test_reserve_duplicate_vaccine(self):
        """Test reserve duplicate vaccine."""
        self.post_registration()
        vaccine_url1 = self.create_url_vaccine("1234567890147","Hospital", "Pfizer")
        requests.post(self.URL+f"/reservation?{vaccine_url1}")
        vaccine_url2 = self.create_url_vaccine("1234567890147","Hospital", "Sinofarm")
        response = requests.post(self.URL+f"/reservation?{vaccine_url2}")
        res_json = response.json()
        requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual("reservation failed: there is already a reservation for this citizen", res_json["feedback"])

    def test_cancel_reserve(self):
        """Test cancel reserve."""
        self.post_registration()
        vaccine_url = self.create_url_vaccine("1234567890147","Hospital", "Pfizer")
        requests.post(self.URL+f"/reservation?{vaccine_url}")
        response = requests.delete(self.URL+f"/reservation/1234567890147")
        res_json = response.json()

        requests.delete(self.URL+f"/registration/1234567890147")
        self.assertEqual("cancel reservation success!", res_json["feedback"])


if __name__ == '__main__':
    unittest.main()