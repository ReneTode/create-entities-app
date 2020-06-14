#
# this is a basic switch component with a small addition
# if the switch is triggered it starts the radio station that is set in the settings
# on the alexa device that is set in the settings
#
 
import appdaemon.plugins.hass.hassapi as hass
import tempfile
import subprocess

class switch_radio(hass.Hass):

    def initialize(self):
        return

    def triggered(self, entity, entity_settings, service, data):
        if service == "turn_on":
            self.radio_on(entity_settings)
            self.set_state(entity,state="on",attributes=entity_settings["attributes"])
        elif service == "turn_off":
            self.radio_off(entity_settings)
            self.set_state(entity,state="off",attributes=entity_settings["attributes"])
        elif service == "toggle":
            if self.get_state(entity) == "on":
                self.radio_off(entity_settings)
                self.set_state(entity,state="off",attributes=entity_settings["attributes"])
            else:
                self.radio_on(entity_settings)
                self.set_state(entity,state="on",attributes=entity_settings["attributes"])
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 


    def radio_on(self,entity_settings):
        alexa_ad = self.get_app("alexa_ad")
        alexa_ad.play_music(entity_settings["attributes"]["device_name"], entity_settings["attributes"]["provider"], entity_settings["attributes"]["station"])
 

    def radio_off(self,entity_settings):
        alexa_ad = self.get_app("alexa_ad")
        alexa_ad.pause(entity_settings["attributes"]["device_name"])