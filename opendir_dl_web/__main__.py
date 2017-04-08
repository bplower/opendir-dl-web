import os
import sys

# This will take and insert the parent directory
par_dir_list = os.path.realpath(__file__).split('/')[:-2]
par_dir = "/" + os.path.join(*par_dir_list)
sys.path.insert(0, par_dir)

# Import the package from the path we just inserted
import opendir_dl_web

# Now call the main function of the library, providing any values we were provided with
opendir_dl_web.main(sys.argv[1:])
