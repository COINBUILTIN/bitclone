import os
import unittest
from lib.commons import Utils, logger


class CommonsTestCase(unittest.TestCase):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_process_tpl_str(self):

        logger.info("Testing template string processing...")

        self.assertEqual(Utils.process_tpl_str("Hello ${name}!", {'name': "World"}), "Hello World!")

        self.assertEqual(Utils.process_tpl_str("${name} ${name} ${name}", {'name': "OK"}), "OK OK OK")

        #with self.assertRaises(KeyError) as context:
            #Utils.process_tpl_str("Make my ${something}", {'name': "day"})

    def test_process_tpl(self):

        logger.info("Testing template processing...")

        tpl_path = os.path.join(self.dir_path, "resources", "test_template.tpl")
        output_file_path = os.path.join(self.dir_path, "resources", "test_output_file.txt")

        Utils.process_tpl(tpl_path, output_file_path, {'name': "OK"})

        self.assertEqual(Utils.read_file(output_file_path), "OK OK OK")

    def test_icons(self):

        logger.info("Testing icons...")
        settings = Utils.get_config("settings.ini")
        output_path = os.path.join(settings['output_dir'], settings['build_folder'])

        Utils.create_icons(settings["imagemagick_dir"], os.path.join(settings["images_dir"], "bitclone_logo.png"), output_path, settings["icons"])


if __name__ == '__main__':
    unittest.main()
