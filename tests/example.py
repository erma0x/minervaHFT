import unittest

# This is the class we want to test. So, we need to import it
import Person as PersonClass


class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    person = PersonClass.Person()  # instantiate the Person Class
    user_id = []  # variable that stores obtained user_id
    user_name = []  # variable that stores person name

    def test_0_set_name(self):
        self.assertIsNotNone(self.user_id)  

    def test_1_get_name(self):
        for i in range(10):
            self.assertEqual(self.user_name[i], self.person.get_name(self.user_id[i]))


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()