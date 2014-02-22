import os
import shutil
import subprocess
from lib.commons import Utils

logger = Utils.get_logger()


def main():

    logger.info("Running Bitcoin Builder...")

    settings = Utils.get_config("settings.ini")
    templates = settings['templates']
    output_path = os.path.join(settings['output_dir'], settings['build_folder'])
    zip_dir = settings['zip_dir']

    if os.path.isfile(zip_dir):
        os.remove(zip_dir)

    if os.path.isdir(output_path):
        shutil.rmtree(output_path)

    shutil.copytree(settings['templates_dir'], output_path)
    shutil.copytree(settings['git_dir'], os.path.join(output_path, ".git"))

    for template in templates:
        if "*" in template:

            tpl_path = os.path.join(output_path, template.split("*")[0])
            tpl_ext = template.split("*")[1]
            files = os.listdir(tpl_path)

            for file in files:
                tpl_path2 = os.path.join(tpl_path, file)
                if os.path.isfile(tpl_path2) and tpl_path2.endswith(tpl_ext):
                    logger.info("Processing template: " + tpl_path2)
                    Utils.process_tpl(tpl_path2, tpl_path2, settings)
        else:

            tpl_path = os.path.join(output_path, template)
            logger.info("Processing template: " + tpl_path)
            Utils.process_tpl(tpl_path, tpl_path, settings)

    # rename build file to coin name
    os.rename(os.path.join(output_path, settings['build_file']), os.path.join(output_path, settings['bcl_name'] + ".pro"))

    # generate icons
    Utils.create_icons(settings['imagemagick_dir'], os.path.join(settings["images_dir"], settings["bitclone_logo"]), output_path, settings["icons"])

    # generate splash screen
    logger.info("Testing splash...")

    splash_path = os.path.join(settings["images_dir"], settings["bitclone_splash"])
    logo_path = os.path.join(settings["images_dir"], settings["bitclone_logo"])
    logo_text_path = os.path.join(settings["images_dir"], settings["bitclone_logo_text"])
    show_bitclone = True if settings["show_bitclone"] == "true" else False

    Utils.create_splash(
        img_magick_path=settings["imagemagick_dir"],
        coin_name=str(settings['bcl_name']).upper(),
        version=settings["version"],
        splash_path=splash_path,
        logo_path=logo_path,
        logo_text_path=logo_text_path,
        show_bitclone=show_bitclone,
        output_path=output_path,
        output_file=settings['splash_image']
    )

    Utils.create_images(settings["imagemagick_dir"], settings, logo_path, output_path)

    os.chdir(settings['output_dir'])

    Utils.exec_cmd(settings['zip_bin'] + " -r " + zip_dir + " bitcoin")

if __name__ == '__main__':
    main()
