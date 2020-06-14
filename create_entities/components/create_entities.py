import appdaemon.plugins.hass.hassapi as hass
import time
import string
import datetime
import copy

class create_entities(hass.Hass):
 
  
  
    def initialize(self):
        ##################################################################################
        # check if in yaml the structure is used for more then 1 entity
        # and if all needed args are given
        ##################################################################################
        if "entity_settings" in self.args:
            if not "platform" in self.args["entity_settings"]:
                self.error("Platform must be given to create entities")
                return
            if not "entities" in self.args["entity_settings"]:
                self.error("a list of entities, with at least 1 entity must be given to create entities")
                return
            platform = self.args["entity_settings"]["platform"]
            ##############################################################################
            # entities are found and can be created
            ##############################################################################
            #all_settings = copy.deepcopy(self.args["entity_settings"]["entities"])
            #for entityID, entity_settings in all_settings.items():
            for entityID, entity_settings in self.args["entity_settings"]["entities"].items():
                if not isinstance(entityID,str) or not isinstance(entity_settings,dict):
                    self.error("an entity is given in the wrong format, i cant create it")
                else:
                    ######################################################################
                    # all setting for an entity are correct.
                    # check if the name has characters that need to be changed to
                    # be conform homeassistant entity naming, and then create the entity
                    ###################################################################### 
                    entity = self.sanetize(platform,entityID)
                    #if "stop" in self.args:
                    #  return
                    self.build_entity(entity,entity_settings)
        else:
            ##############################################################################
            # only a single entity is setup in this app
            # check if all needed args are there and create an entity_settings dict
            ##############################################################################
            entity_settings = {}
            if not "name" in self.args:
                self.error("i cant create an entity without a name")
                return
            if not "platform" in self.args:
                self.error("Platform must be given to create entities")
                return
            entityID = self.args["name"]
            platform = self.args["platform"]
            if "attributes" in self.args:
                entity_settings["attributes"] = self.args["attributes"]
            if "initial_state" in self.args:
                entity_settings["initial"] = self.args["initial_state"]
            if "component_type" in self.args:
                entity_settings["component_type"] = self.args["component_type"]

            ######################################################################
            # all setting for an entity are correct.
            # check if the name has characters that need to be changed to
            # be conform homeassistant entity naming, and then create the entity
            ###################################################################### 
            entity = self.sanetize(platform,entityID)
            #if "stop" in self.args:
            #  return
            self.build_entity(entity,entity_settings)


    def build_entity(self, entityID, entity_settings):
        ##########################################################################
        # create a dict for attributes, if attributes are given in the args
        # then use that dict, and if assumed_state is not provided set it to True
        ##########################################################################
        #if "stop" in self.args:
        #  return
        _attributes = {}
        if "attributes" in entity_settings:
            _attributes = entity_settings["attributes"]
        else:
            entity_settings["attributes"] = {}
        if not "assumed_state" in _attributes:
            _attributes["assumed_state"] = True
            entity_settings["attributes"]["assumed_state"] = True

        ##########################################################################
        # if initial state isnt provided, set it to off
        ##########################################################################
        if "initial" in entity_settings:
            initial_state = entity_settings["initial"]
        else:
            initial_state = "off"

        ##########################################################################
        # check if a value is saved, if so then use that as initial state
        ########################################################################## 
        initial_state = self.get_saved_value(entityID,initial_state)

        if not self.entity_exists(entityID):
            ######################################################################
            # only if the entity doesnt exist in home assistant we need to create
            # it
            ######################################################################
            self.set_state(entityID, state = initial_state, attributes = _attributes)
            self.log("Created {} in HASS".format(entityID))
        else:
            if "re_initialise" in entity_settings:
                if entity_settings["re_initialise"]:
                    ##############################################################
                    # the entity already exists, but re_initialise is in the
                    # settings and set to True, so we do reset the state from the
                    # entity, based on the settings that are given in the yaml
                    # but we keep the state that is set in homeassistant
                    ##############################################################
                    entity_state = self.get_state(entityID)
                    self.set_state(entityID, state = entity_state, attributes = _attributes)
                    self.log("{} was already created in HASS, just listening, and set attributes".format(entityID))
                else:
                    self.log("{} was already created in HASS, just listening".format(entityID))
            else:
                self.log("{} was already created in HASS, just listening".format(entityID))

        if not "component_type" in entity_settings:
            ######################################################################
            # if no component type was given, create the empty setting
            ######################################################################
            entity_settings["component_type"] = ""

        platform,entityname = self.split_entity(entityID)
        if platform == "sensor" or platform == "binary_sensor":
            ######################################################################
            # a sensor doesnt need to listen to service calls, all other
            # components need that
            ######################################################################
            return
        else:
            self.listen_event(self.change_state, event = "my_call_service", entity_id = entityID, entity_settings = entity_settings)
            runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            try:
                numberslog = open("/mnt/usbdrive/pi/HAlogs/created entities.csv", 'a')
                numberslog.write(runtime + "     ;" + entityID +  "\n")
                numberslog.close()
            except:
                self.log("LOGFILE /mnt/usbdrive/pi/HAlogs/test.csv NIET BEREIKBAAR!!",level = "WARNING")
 
    def change_state(self,event_name,data, kwargs):
        ##########################################################################
        # a service has been called get the platform from the entity
        # and trigger the component app that belongs to the platform and component
        ##########################################################################
        platform, entityname = self.split_entity(data["entity_id"])
        app = "{}_{}".format(platform,kwargs["entity_settings"]["component_type"])
        #self.log("{} triggered for {}".format(app,data["service_data"]["entity_id"]))
        if kwargs["entity_settings"]["component_type"] != "grapje":
            func = self.get_app(app)
            func.triggered(data["entity_id"], kwargs["entity_settings"], data["service"], data )
        else:
            new_data = {"entity_id": data["entity_id"],"entity_settings": kwargs["entity_settings"], "data": data}
            self.call_service("ad_{}_{}/{}".format(platform, kwargs["entity_settings"]["component_type"], data["service"]), namespace="ad_entities", **new_data)
  
    def sanetize(self,platform,entity_name):
        ##########################################################################
        # make sure that the entityname is correct, replace all not wanted
        # characters and make it completely lowercase, return the entity name 
        ##########################################################################
        platform = platform.lower()
        entity_name = entity_name.lower()
        bad_characters = list(string.punctuation)
        bad_characters.extend([" ","____","___","__"])
        for character in bad_characters:
            entity_name = entity_name.replace(character,"_")
        if entity_name[0] == "_":
            entity_name = entity_name[1:]
        if entity_name[-1] == "_":
            entity_name = entity_name[:-1]        
        return "{}.{}".format(platform,entity_name)
     
    def get_saved_value(self,entity,defaultvalue):
        ##########################################################################
        # if a save type is set in the yaml, then we use that type, else we
        # use the default save type
        ##########################################################################
        if "state_save_type" in self.args:
            saved_value_app = "save_style_" + self.args["state_save_type"]
        else:
            saved_value_app = "save_style_default"
        func = self.get_app(saved_value_app)
        return func.get_saved_value(entity,defaultvalue)

