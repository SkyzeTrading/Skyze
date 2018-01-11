#----------------------------------------------------------------------------------------------------------
#
#   CLASS DataAccess
#
#----------------------------------------------------------------------------------------------------------

import os
import Skyze_Standard_Library.settings_skyze as settings_skyze


class DataAccess:


    def __init__(self):
        Data = []
        
    
    # creates the full path and file name
    
    def fileName(self, p_market_name, p_extension):
        return os.path.join(settings_skyze.data_file_path, "%(name)s.%(extension)s" % {"name":p_market_name, "extension":p_extension})
    
    
       