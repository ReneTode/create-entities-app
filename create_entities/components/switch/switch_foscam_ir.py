#
# this is a basic switch component.
# it does nothing more then keep an with appdaemon created switch working.
# you can use the switch in other apps with listen state.
#

import appdaemon.plugins.hass.hassapi as hass
import requests

class switch_foscam_ir(hass.Hass):

    def initialize(self):
        return

    def triggered(self, entity, entity_settings, service, data):
        cam_name = entity_settings["attributes"]["cam_name"]
        ipnr = self.app_config["settings"]["foscam"][cam_name]["host"]
        ip = "{}{}".format(self.app_config["settings"]["ip_group"], ipnr)
        portnr = self.app_config["settings"]["foscam"][cam_name]["port"]
        user = self.app_config["settings"]["foscam"][cam_name]["user"]
        password = self.app_config["settings"]["foscam"][cam_name]["password"]
        url = "http://{}:{}/cgi-bin/CGIProxy.fcgi?&usr={}&pwd={}&cmd=".format(ip, portnr, user, password)
        if service == "turn_on":
            cmd = requests.get(url + "openInfraLed")
            self.set_state(entity,state="on",attributes=entity_settings["attributes"])
        elif service == "turn_off":
            cmd = requests.get(url + "closeInfraLed")
            self.set_state(entity,state="off",attributes=entity_settings["attributes"])
        elif service == "toggle":
            if self.get_state(entity) == "on":
                cmd = requests.get(url + "openInfraLed")
                self.set_state(entity,state="off",attributes=entity_settings["attributes"])
            else:
                cmd = requests.get(url + "closeInfraLed")
                self.set_state(entity,state="on",attributes=entity_settings["attributes"])
        else:
            self.log("entity: {} got service: {} which isnt supported by the switch component.".format(entity,service)) 


