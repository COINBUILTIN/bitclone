import os
import ConfigParser
from string import Template

class Utils:

    @staticmethod
    def process_tpl_str(str, kws):

        dict = {}
        for v in kws:
            if not type(kws[v]) is list:
                dict[v] = kws[v]

        tpl = Template(str)

        return tpl.safe_substitute(kws)

    @staticmethod
    def process_tpl(tpl_file_path, output_file_path, kws):

        Utils.write_file(output_file_path, Utils.process_tpl_str(Utils.read_file(tpl_file_path), kws))

    @staticmethod
    def read_file(file_path):

        data = ""
        with open(file_path, "r") as myfile:
            data = myfile.read()

        return data

    @staticmethod
    def write_file(file_path, str):

        data = ""
        with open(file_path, "w") as myfile:
            data = myfile.write(str)

        return data

    @staticmethod
    def get_config(file_path):

        section = "settings"
        settings = {}
        Config = ConfigParser.ConfigParser()
        Config.read(file_path)
        options = Config.options(section)
        for option in options:
            try:
                settings[option] = Config.get(section, option)
                if settings[option] == -1:
                    print("skip: %s" % option)
                elif "\n" in settings[option]:
                    parts = settings[option].split("\n")
                    new_parts = []
                    for part in parts:
                        if len(part.strip()) > 0:
                            new_parts.append(part)

                    settings[option] = new_parts

            except Exception, e:
                print("exception on %s %s!" % (option, str(e)))
                settings[option] = None
        return settings
