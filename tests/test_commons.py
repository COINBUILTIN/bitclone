import os
import unittest
from lib.commons import Utils

class CommonsTestCase(unittest.TestCase):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_process_tpl_str(self):

        self.assertEqual(Utils.process_tpl_str("Hello ${name}!", {'name': "World"}), "Hello World!")

        self.assertEqual(Utils.process_tpl_str("${name} ${name} ${name}", {'name': "OK"}), "OK OK OK")

        with self.assertRaises(KeyError) as context:
            Utils.process_tpl_str("Make my ${something}", {'name': "day"})

    def test_process_tpl(self):

        tpl_path = os.path.join(self.dir_path, "resources", "test_template.tpl")
        output_file_path = os.path.join(self.dir_path, "resources", "test_output_file.txt")

        Utils.process_tpl(tpl_path, output_file_path, {'name': "OK"})

        self.assertEqual(Utils.read_file(output_file_path), "OK OK OK")


if __name__ == '__main__':
    unittest.main()
