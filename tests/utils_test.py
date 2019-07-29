import unittest

from utils import *
from test_helper import gradebook, membership


class MyTestCase(unittest.TestCase):
    def test_ordered_unique_list_empty_list(self):
        input_list = []

        actual = ordered_unique_list(input_list)
        self.assertTrue(len(actual) == 0)

    def test_ordered_unique_list_number(self):
        input_list = [1, 3, 2, 1]

        actual = ordered_unique_list(input_list)
        expected = [1, 3, 2]

        for x in range(3):
            self.assertEqual(actual[x], expected[x])

    def test_ordered_unique_list_text(self):
        input_list = ["d", "c", "a", "a"]

        actual = ordered_unique_list(input_list)
        expected = ["d", "c", "a"]

        for x in range(3):
            self.assertEqual(actual[x], expected[x])

    def test_do_all_data_sources_exist_existing_smaller_than_required(self):
        existing = []
        required = [1]

        exist = do_all_data_sources_exist(existing, required)
        self.assertFalse(exist)

    def test_do_all_data_sources_exist_exists(self):
        existing = [{'name': 'cilt'}]
        required = ['cilt']

        exist = do_all_data_sources_exist(existing, required)
        self.assertTrue(exist)

    def test_do_all_data_sources_exist_does_not_exist(self):
        existing = [{'name': 'cilt'}]
        required = ['test']

        exist = do_all_data_sources_exist(existing, required)
        self.assertFalse(exist)

    def test_create_table_empty_gradebook(self):
        row_headers = ["head1, head2"]

        table = create_table([], row_headers)
        self.assertTrue(len(table) == 0)

    def test_create_table_empty_headers(self):
        table = create_table(gradebook, [])
        self.assertTrue(len(table) == 0)

    def test_create_table_empty_headers(self):
        row_headers = ["1"]

        table = create_table(gradebook, row_headers)
        self.assertTrue(table[0][0] == "35")
        self.assertTrue(table[0][1] == "50")

    def test_delete_unwanted_keys(self):
        data = delete_unwanted_keys(membership)
        self.assertTrue(len(data) == 3)
        self.assertEqual(data['test'], 'successful')

    def test_delete_unwanted_keys_empty_membership(self):
        data = delete_unwanted_keys({})
        self.assertTrue(len(data) == 0)

    def test_update_student_number(self):
        data = update_student_number(membership)
        self.assertEqual(data['userEid'], 'ABCXYZ001')
        self.assertNotEqual(data['userEid'], 'abcxyz001')

    def test_update_student_number_empty_membership(self):
        data = update_student_number({})
        self.assertTrue(not data)

    def test_update_name(self):
        data = update_name(membership)
        self.assertEqual(data['firstname'], 'Cilt')
        self.assertEqual(data['lastname'], 'Team')

    def test_update_name_empty_membership(self):
        data = update_name({})
        self.assertTrue(not data)


if __name__ == '__main__':
    unittest.main()
