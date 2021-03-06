# Components app

## Introduction

Lots of times i need a new entity in Home assistant when i am creating new apps.
And every time when i added a new input_boolean or an input_slider i needed to restart home assistant.
And thats annoying because settings are not always the same, and it takes up way to much time.
To create sensors there was already an option default in Appdaemon. set_state!
That works great, for a few sensors and after a while i did create an app that creates all my sensors at startup.
It checks if the entity exists and if not it creates the sensor.

Not that long ago i got a conversation on the forum about the disability to create other entities then sensors.
And then i found out that it IS possible to create other entities.
But it is a little more complicated then just the set_state function.
I created an app to create some switches and that was satifying for a while.
But i saw more potential, so i created this appsystem to create all kind of entities.
Just by putting some YAML in the apps directory and directly the entity is live.
at this moment this app can create several entity types:

- sensor
- default input_boolean
- default input_text
- default input_number
- default switch

and i added a few switch types that show how to create your own personal switches.

## Installation

I expect that you already have appdaemon setup.
Then all you need to do is download the complete directory structure here and place it in your apps directory.
As soon as that is done i would advise to restart Appdaemon. (it might not be neccesary, but to be save)
then you can start creating entities.

## Setting up entities

There is an example YAML file in the main directory showing all possibilities, but ill explain it also here.

There are 2 ways you can make an app that creates entities:
1) Use 1 app for each entity (this can be a preffered way if you have an entity that is heavy used)
2) Use 1 app for all entities that belong to a certain platform
and of course you can use any kind of combination.

in the example YAML file there are examples for type 2 apps and 1 for a single entity type.

- Priority: needs to be set to 2 because the other parts from the entity creation are loaded before this.
- initial: will default to "off" when not set and when not retrieved from saved state (see saving state part)
- state_save_type: YOUR_STYLE uses the app save_style_YOUR_STYLE that is placed in the helper_files directory
 a default file is given. This doesnt SAVE the state it is used to retrieve saved states when appdaemon/HA is restarted.
- platform: is the same as on home assistant, only platforms can be used that have a component file (see components dir, at this moment the above mentioned entities)

- In attributes you can provide every valid attribute for that type of entity
(see the homeassistant components page what you can use) https://www.home-assistant.io/components/
 
- component_type: if not given it uses the default platform, if given it uses the custom component (see custom components)


## Retrieving already saved states

If you want the entities to pickup their last state, you need to create an app that saves the state
If you have the last saved state somewhere you can retrieve it with a special app to make sure that value is used when you restart HA. 
The last saved state overrides the initial state value.
That special app must be placed in the helper_files directory and it must be named like: save_style_YOUR_STYLE
make sure that you create both the py script and the YAML file (there is a default file that describes what to do)

## Creating and using new components

Every platform type has its own directory (switch, input_text,etc)
To create a new switch type just copy and rename the files switch_.py and switch_.yaml to something like:
switch_YOUR_TYPE.py and switch_YOUR_TYPE.yaml and adapt the settings in the yaml file and change the class name accordingly.
Now you can use the new component type you created by adding component_type: YOUR_TYPE to the entity settings.
You can take a look at the component types i created for myself as an example.
 

have fun, creating new entities.

greetz

Rene Tode

for support ask me on discord in our appdaemon section https://discord.gg/pHsjADY

(and please feel free to share and adapt this code, but keep this readme.md file included so that i can get some credit)

 
