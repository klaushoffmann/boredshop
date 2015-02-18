"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import FacebookAuth, UserPreferences
import mailchimp

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        list = mailchimp.utils.get_connection().get_list_by_id("f533561106")
        print list


        self.assertEqual(1 + 1, 2)
