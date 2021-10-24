"""Test Registration API endpoint from World Class Government"""
import unittest
import requests
import datetime

HOST = "https://wcg-apis.herokuapp.com"
DATABASE_URL = HOST + "/citizen"
URL = HOST + "/registration"


def create_citizen(citizen_id, firstname, lastname, birthdate,
                   occupation, address):
    """Create dict of citizen data"""
    return {
        'citizen_id': citizen_id,
        'name': firstname,
        'surname': lastname,
        'birth_date': birthdate,
        'occupation': occupation,
        'address': address
    }


def get_feedback(response):
    """Get feedback from response"""
    return response.json()['feedback']


class RegistrationTest(unittest.TestCase):
    """Unit tests for Registration API"""

    def setUp(self):
        requests.delete(DATABASE_URL, data=create_citizen("1101101101101", "Tester", "Test", "15 Jan 1990"
                                                          , "Office worker", "123/123 Test, Demo, Bangkok 10230"))
        self.user = create_citizen("1101101101101", "Tester", "Test", "15 Jan 1990"
                                   , "Office worker", "123/123 Test, Demo, Bangkok 10230")

    def test_register(self):
        """Test register success"""
        response = requests.post(URL, data=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_feedback(response), "registration success!")

    def test_register_with_missing_attribute(self):
        """test register with missing attribute"""
        test = create_citizen("1101101101102", "Tester", "Test", "15 Jan 1990"
                              , "", "123/123 Test, Demo, Bangkok 10230")
        response = requests.post(URL, data=test)
        self.assertEqual(get_feedback(response), "registration failed: missing some attribute")

    def test_invalid_citizen_id(self):
        """Test register when citizen id is invalid"""
        test = create_citizen("110110", "Tester2", "Test", "15 Jan 1990", "Office worker",
                              "123/123 Test, Demo, Bangkok 10230")
        test2 = create_citizen("abcde", "Tester3", "Test", "1 Feb 1999",
                               "Student", "124/23 Bakery, Bangkok 10120")
        response = requests.post(URL, data=test)
        response2 = requests.post(URL, data=test2)
        self.assertEqual(get_feedback(response), "registration failed: invalid citizen ID")
        self.assertEqual(get_feedback(response2), "registration failed: invalid citizen ID")

    def test_already_registered(self):
        """Test register when already registered"""
        response = requests.post(URL, data=self.user)
        response2 = requests.post(URL, data=self.user)
        self.assertEqual(get_feedback(response), "registration success!")
        self.assertEqual(get_feedback(response2), "registration failed: this person already registered")

    def test_invalid_birth_date_format(self):
        """Test register when birth date is invalid format"""
        test = create_citizen("1101101101102", "Tester2", "Test", "12 1999 04", "Office worker",
                              "123/123 Test, Demo, Bangkok 10230")
        response = requests.post(URL, data=test)
        self.assertEqual(get_feedback(response), "registration failed: invalid birth date format")

    def test_register_with_age_less_than_13(self):
        """Test register when age less than 13"""
        test = create_citizen("1101101101102", "Tester2", "Test", "12-04-2014", "Student",
                              "123/123 Test, Demo, Bangkok 10230")
        response = requests.post(URL, data=test)
        self.assertEqual(get_feedback(response), "registration failed: not archived minimum age")


if __name__ == '__main__':
    unittest.main()
