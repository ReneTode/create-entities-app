#
# this is a basic input_text component.
# it does nothing more then keep an with appdaemon created input_text working.
# you can use the input_text in other apps with listen state.
#

import appdaemon.plugins.hass.hassapi as hass

class input_text_(hass.Hass):

    def initialize(self):
        return

    def triggered(self, entity, entity_settings, service, data):
        service_data=data["service_data"]
        if service == "set_value":
            self.set_state(entity,state=service_data["value"],attributes=entity_settings["attributes"])
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 