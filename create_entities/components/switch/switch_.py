#
# this is a basic switch component.
# it does nothing more then keep an with appdaemon created switch working.
# you can use the switch in other apps with listen state.
#


import appdaemon.plugins.hass.hassapi as hass

class switch_(hass.Hass):

    def initialize(self):
        return

    def triggered(self, entity, entity_settings, service, data):
        if service == "turn_on":
            self.set_state(entity,state = "on", attributes = self.get_attributes(entity))
        elif service == "turn_off":
            self.set_state(entity,state="off", attributes = self.get_attributes(entity))
        elif service == "toggle":
            if self.get_state(entity) == "on":
                self.set_state(entity,state="off", attributes = self.get_attributes(entity))
            else:
                self.set_state(entity,state="on", attributes = self.get_attributes(entity))
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 

    def get_attributes(self, switch):
        if self.entity_exists(switch):
            old_state = self.get_state(switch, attribute = "all")
        else:
            return {}
        return old_state["attributes"]
