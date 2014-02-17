import os
import json
import ConfigParser
import subprocess
import logging
import logging.config
from logging.handlers import RotatingFileHandler


class Utils:

    @staticmethod
    def process_tpl_str(str, kws):

        dict = {}
        for v in kws:
            if not type(kws[v]) is list:
                dict[v] = kws[v]

        #tpl = Template(str)
        #return tpl.safe_substitute(kws)

        return Utils.replace_str(str, dict)

    @staticmethod
    def replace_str(s, kws):

        for v in kws:
            s = s.replace("${" + str(v) + "}", kws[v])

        return s


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
                    logger.info("skip: %s" % option)
                elif "\n" in settings[option]:
                    parts = settings[option].split("\n")
                    new_parts = []
                    for part in parts:
                        if len(part.strip()) > 0:
                            new_parts.append(part)

                    settings[option] = new_parts

            except Exception, e:
                logger.error("exception on %s %s!" % (option, str(e)))
                settings[option] = None
        return settings

    @staticmethod
    def exec_cmd(cmd):

        try:
            logger.info(cmd)
            logger.info('stdout: {}'.format(subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)))
        except subprocess.CalledProcessError as e:
            logger.error(e)
            logger.error(e.output)

    @staticmethod
    def create_icons(img_magick_path, logo_path, output_path, icons):

        for icon in icons:
            logger.info(icon)
            icon = json.loads(icon)
            cmd = img_magick_path + " " + logo_path + " -bordercolor white -border 0"
            for size in icon["sizes"]:
                cmd += "\( -clone 0 -resize %dx%d \) " % (int(size), int(size))

            cmd += "-delete 0 -alpha off -colors 256 " + os.path.join(output_path, icon["path"])
            logger.info("Icon creation CMD: " + cmd)

            Utils.exec_cmd(cmd)

try:
    settings = Utils.get_config("settings.ini")
except:
    settings = Utils.get_config("../settings.ini")

logging.RotatingFileHandler = RotatingFileHandler
logging.config.fileConfig(settings['log_config_path'])
logger = logging