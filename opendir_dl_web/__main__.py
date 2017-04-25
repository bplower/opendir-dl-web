import os
import sys

# This will take and insert the parent directory
PAR_DIR_LIST = os.path.realpath(__file__).split('/')[:-2]
PAR_DIR = "/" + os.path.join(*PAR_DIR_LIST)
sys.path.insert(0, PAR_DIR)

# Import the package from the path we just inserted
import opendir_dl_web

# Now call the main function of the library, providing any values we were provided with
opendir_dl_web.main(sys.argv[1:])
