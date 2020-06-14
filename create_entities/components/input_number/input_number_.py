#
# this is a basic input_number component.
# it does nothing more then keep an with appdaemon created input_number working.
# you can use the input_number in other apps with listen state.
#
 
import appdaemon.plugins.hass.hassapi as hass

class input_number_(hass.Hass):

    def initialize(self):
        return

    def triggered(self, entity, entity_settings, service, data):
        service_data=data["service_data"]
        if "step" in entity_settings["attributes"]:
            step = float(entity_settings["attributes"]["step"])
        else:
            step = 1
        min = float(entity_settings["attributes"]["min"])
        max = float(entity_settings["attributes"]["max"])

        if service == "set_value":
            state = service_data["value"]
        elif service == "decrement":
            state = float(self.get_state(entity)) - step
            if state < min:
                state = min
        elif service == "increment":
            state = float(self.get_state(entity)) + step
            if state > max:
                state = max
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 
            return
        self.set_state(entity,state=state,attributes=entity_settings["attributes"])
