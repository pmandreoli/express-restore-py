import os
import argparse
import tarfile
import shutil
import subprocess
import glob

conda_destination='/export/tool_deps/' 
shed_tool_destination='/home/galaxy/galaxy/var/shed_tools/'
cvmfs= "elixir-italy.galaxy.refdata"
cvmfs_path='/cvmfs/'+ cvmfs + '/'
cvmfs_dump= cvmfs_path + '/express-dump/'

def parse_cli_options():
  parser = argparse.ArgumentParser(description='untar flavor packages', formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument( '-f', '--flavor',  dest='flavor', default=None , help='galaxy flavor')
  return parser.parse_args()

def extract_tar_gz(tar_file, destination):
  check_cvmfs()
  tar = tarfile.open(tar_file)
  tar.extractall(destination)
  tar.close()
  done_message= str(tar_file)+ "  was extrated in "+ str(destination)
  print(done_message)


def check_cvmfs():
    if os.path.ismount(cvmfs_path):
        print(cvmfs_path + " is mounted")
    else:
        raise ValueError('THE CVMFS is Not MOUNTED')


def clean_destinations():
    conda = glob.glob(conda_destination + '*')
    shed_tools = glob.glob(shed_tool_destination + '*')
    for f in conda:
      shutil.rmtree(f)
    for f in shed_tools:
      shutil.rmtree(f)
 

def untar_conda_and_shell():
    options = parse_cli_options()
    conda_file = cvmfs_dump + str(options.flavor) + '/'+ str(options.flavor) + '_conda.tar.gz'
    shed_tools_file = cvmfs_dump + str(options.flavor) + '/' + str(options.flavor) +'_shed_tools.tar.gz'
    clean_destinations()
    print("FLAVOR_RESTORE: cleaning")
    extract_tar_gz(shed_tools_file, shed_tool_destination)
    print("FLAVOR_RESTORE: restoring shed_tools")
    extract_tar_gz(conda_file, conda_destination)
    print("FLAVOR_RESTORE: restoring conda dir")

# bash restore postgresql pg_restore -d db_name /path/to/your/file/dump_name.tar -c -U db_user
def manage_services(smd_cmd):
  os.system("sudo systemctl " + smd_cmd + " galaxy")

def restore_dump():
  options = parse_cli_options()
  command_delete = " sudo -H -u postgres bash -c 'dropdb galaxy_tools' " 
  command_create = " sudo -H -u postgres bash -c 'createdb galaxy_tools' " 
  os.system(command_delete)
  os.system(command_create)
  print("old postgres galaxy_tools database deleted")
  restore_file = cvmfs_dump + str(options.flavor) + '/'+ str(options.flavor) + '.sql'
  command_restore = "sudo -H -u postgres bash -c 'psql -U postgres -d galaxy_tools -f " + restore_file + "'" 
  os.system(command_restore)
  print("restore galaxy_tools database flavor")

def main():
    
  manage_services("stop")
  untar_conda_and_shell()
  restore_dump()
  manage_services("start")
  check_cvmfs()

main()
