#
# this is a basic input_boolean component.
# it does nothing more then keep an with appdaemon created input_boolean working.
# you can use the input_boolean in other apps with listen state.
#

import appdaemon.plugins.hass.hassapi as hass

class input_boolean_(hass.Hass):

    def initialize(self):
        return

    def triggered(self, entity, entity_settings, service, data):
        if service == "turn_on":
            self.set_state(entity,state="on",attributes=entity_settings["attributes"])
        elif service == "turn_off":
            self.set_state(entity,state="off",attributes=entity_settings["attributes"])
        elif service == "toggle":
            if self.get_state(entity) == "on":
                self.set_state(entity,state="off",attributes=entity_settings["attributes"])
            else:
                self.set_state(entity,state="on",attributes=entity_settings["attributes"])
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 