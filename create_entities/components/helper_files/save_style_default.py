#
# this app is the default save style
# if you want to use another way to get the last saved state then copy it and name it: save_style_YOUR_TYPE
# after that rename also the class name accordingly
#
# but you also need to create another yaml file that will look like:
# save_style_YOUR_TYPE:
#   module: save_style_YOUR_TYPE
#   class: save_style_YOUR_TYPE
#
# after that you can use YOUR_TYPE in the yaml from the entity creation.
#
# this app only provides 1 function called get_saved_value which has to have the same arguments as the function you find here
# and it should return the state you found or the default state
#

import appdaemon.plugins.hass.hassapi as hass

class save_style_default(hass.Hass):

    def initialize(self):
        return

    def get_saved_value(self,entity,defaultvalue):
        platform, entityname = self.split_entity(entity)
        ######################################################################################
        # this style of state retrieving can be used when you have an app that saves the
        # state after every change like: timestamp,state
        # the file needs to have a name according to the entity (without platform) and an
        # extention txt
        # the directory where all the states are saved can be set in the yaml file
        ######################################################################################
        try:
            log = open(self.args["logfiledirname"] + entityname + ".txt", 'r')
            lines = log.readlines()
            last_line = lines[-1]
            log.close()    
            value = last_line.split(",")
            value[1] = value[1].strip()
            if "." in value[1]:
                try:
                    new_value = float(value[1])
                except:
                    new_value = value[1]
            else:
                try:
                    new_value = int(value[1])
                except:
                    new_value = value[1]
            return new_value
        except:
            return defaultvalue

