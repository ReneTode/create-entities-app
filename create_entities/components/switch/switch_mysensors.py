#
# this is a basic switch component with a small addition.
# if the switch is changed then a mysensors switch (set in the settings) is triggered to send a 433mhz signal.
# the on and off code is also set in the settings..
#
 
import appdaemon.plugins.hass.hassapi as hass
import tempfile
import subprocess

class switch_mysensors(hass.Hass):

    def initialize(self):
        return
 

    def triggered(self, entity, entity_settings, service, data):
        if service == "turn_on":
            self.set_state(entity,state="on",attributes=entity_settings["attributes"])
            self.set_state(entity_settings["attributes"]["433_switch"],state="on", attributes = {"V_IR_SEND": entity_settings["attributes"]["on_code"]})
            #self.log("turn on {}".format(entity))
        elif service == "turn_off":
            self.set_state(entity,state="off",attributes=entity_settings["attributes"])
            self.set_state(entity_settings["attributes"]["433_switch"],state="on", attributes = {"V_IR_SEND": entity_settings["attributes"]["off_code"]})
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 