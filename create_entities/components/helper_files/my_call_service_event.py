#
# this app listens to all call_service events
# when it gets triggered it fires a custom event with the entity on base level in the data
# this is needed for the entity creation app
#

import appdaemon.plugins.hass.hassapi as hass

class my_call_service_event(hass.Hass):

    def initialize(self):
        self.listen_event(self.create_event, event="call_service")

    def create_event(self,event_name,data, kwargs):
        if "entity_id" in data["service_data"]:
            self.fire_event("my_call_service",service = data["service"],entity_id = data["service_data"]["entity_id"],service_data = data["service_data"])
          

