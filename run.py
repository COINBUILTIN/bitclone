import os
import shutil
import subprocess
from lib.commons import Utils

def main():

    print "Running Bitcoin Builder..."

    settings = Utils.get_config("settings.ini")
    templates = settings['templates']
    output_path = os.path.join(settings['output_dir'], "bitcoin")
    zip_dir = settings['zip_dir']

    if os.path.isfile(zip_dir):
        os.remove(zip_dir)

    if os.path.isdir(output_path):
        shutil.rmtree(output_path)

    shutil.copytree(settings['templates_dir'], output_path)

    for template in templates:

        if "*" in template:

            tpl_path = os.path.join(output_path, template.split("*")[0])
            tpl_ext = template.split("*")[1]
            files = os.listdir(tpl_path)

            for file in files:
                tpl_path2 = os.path.join(tpl_path, file)
                if os.path.isfile(tpl_path2) and tpl_path2.endswith(tpl_ext):
                    print "Processing template: " + tpl_path2
                    Utils.process_tpl(tpl_path2, tpl_path2, settings)

        else:

            tpl_path = os.path.join(output_path, template)
            print "Processing template: " + tpl_path
            Utils.process_tpl(tpl_path, tpl_path, settings)

    os.chdir(settings['output_dir'])
    PIPE = subprocess.PIPE
    pd = subprocess.Popen([settings['zip_bin'], '-r', zip_dir, "bitcoin"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = pd.communicate()

    print stdout
    print stderr

if __name__ == '__main__':
    main()
