import os
import json
import ConfigParser
from datetime import date
import subprocess
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import config.app_cfg

class Utils:

    @staticmethod
    def get_logger():

        logging.RotatingFileHandler = RotatingFileHandler
        logging.config.fileConfig(config.app_cfg.log_config_path)

        return logging


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

        logger = Utils.get_logger()

        section = "settings"
        settings = {}
        Config = ConfigParser.SafeConfigParser()
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
                logger.info("exception on %s %s!" % (option, str(e)))
                settings[option] = None
        return settings

    @staticmethod
    def exec_cmd(cmd):

        logger = Utils.get_logger()

        try:
            logger.info(cmd)
            logger.info('stdout: {}'.format(subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)))
        except subprocess.CalledProcessError as e:
            logger.error(e)
            logger.error(e.output)

    @staticmethod
    def create_icons(img_magick_path, logo_path, output_path, icons):

        logger = Utils.get_logger()

        for icon in icons:
            logger.info("Creating icon: " + icon)
            icon = json.loads(icon)
            cmd = img_magick_path + " " + logo_path + " -bordercolor white -border 0 "
            for size in icon["sizes"]:
                cmd += "\( -clone 0 -scale %dx%d -gravity center -extent %dx%d \) " % (int(size), int(size), int(size), int(size))

            cmd += "-delete 0 -alpha off -colors 256 " + os.path.join(output_path, icon["path"])
            logger.info("Icon creation CMD: " + cmd)

            Utils.exec_cmd(cmd)

    @staticmethod
    def create_splash(img_magick_path, coin_name, version, splash_path, logo_path, logo_text_path, show_bitclone, output_path, output_file):

        logger = Utils.get_logger()
        output_file_path = os.path.join(output_path, output_file)
        resized_logo_path = os.path.join(output_path, "resized_logo.png")
        resized_logo_text_path = os.path.join(output_path, "resized_logo_text.png")

        # resize logo image to be placed on top of splash image
        cmd = img_magick_path + " " + logo_path + " -scale 45x45 -gravity center -extent 45x45 " + resized_logo_path
        logger.info("Splash creation CMD: " + cmd)
        Utils.exec_cmd(cmd)

        # resize bitclone text logo
        if show_bitclone:
            cmd = img_magick_path + " " + logo_text_path + " -scale 140x40 -gravity center -extent 140x40 " + resized_logo_text_path
            logger.info("Splash creation CMD: " + cmd)
            Utils.exec_cmd(cmd)

        # put logo on top of splash image
        cmd = img_magick_path + " " + splash_path + " " + resized_logo_path + " -gravity center -geometry +0-20 -compose over -composite " + output_file_path
        logger.info("Splash creation CMD: " + cmd)
        Utils.exec_cmd(cmd)

        # put coin name
        cmd = img_magick_path + " " + output_file_path + " -pointsize 30 -gravity center -draw \"text 0,25 '" + coin_name + "'\" " + output_file_path
        logger.info("Splash creation CMD: " + cmd)
        Utils.exec_cmd(cmd)

        # put version
        cmd = img_magick_path + " " + output_file_path + " -pointsize 12 -annotate 0x0+390+290 'Version " + version + "' " + output_file_path
        logger.info("Splash creation CMD: " + cmd)
        Utils.exec_cmd(cmd)

        # put copyright
        cmd = img_magick_path + " " + output_file_path + " -pointsize 12 -annotate 0x0+227+302 'Copyright " + str(date.today().year) + " Bitcoin/Litecoin Developers' " + output_file_path
        logger.info("Splash creation CMD: " + cmd)
        Utils.exec_cmd(cmd)

        # put bitclone logo
        if show_bitclone:
            cmd = img_magick_path + " " + output_file_path + " " + resized_logo_text_path + " -gravity west -geometry +10+110 -compose over -composite " + output_file_path
            logger.info("Splash creation CMD: " + cmd)
            Utils.exec_cmd(cmd)

            # put bitclone copyright
            cmd = img_magick_path + " " + output_file_path + " -pointsize 12 -annotate 0x0+12+302 'Created with www.bitclone.net' " + output_file_path
            logger.info("Splash creation CMD: " + cmd)
            Utils.exec_cmd(cmd)

    @staticmethod
    def create_images(img_magick_path, images_list, logo_path, output_path):

        logger = Utils.get_logger()

        header_path = os.path.join(output_path, images_list['nsis_header_image'])
        wizard_path = os.path.join(output_path, images_list['nsis_wizard_image'])

        # create nsis header image
        cmd = cmd = img_magick_path + " " + logo_path + " -resize 140x47\\> -size 150x57 xc:white +swap -gravity east -geometry +5+0  -composite " + header_path
        Utils.exec_cmd(cmd)

        # create wizard header image
        cmd = cmd = img_magick_path + " " + logo_path + " -resize 154x304\\> -size 164x314 xc:white +swap -gravity center -composite " + wizard_path
        Utils.exec_cmd(cmd)