#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)

def call_command_api(api, header, device, cmd):
    from requests import put
    import json
    url = api.encode("utf-8") + '/device/' + device.encode("utf-8") + '/command/' + cmd.encode("utf-8"))
    response = put(url, headers=header)

def call_attribute_api(api, header, device, cmd):
    from requests import get
    import json
    url = api.encode("utf-8") + '/device/' + device.encode("utf-8") + '/attribute/' + cmd.encode("utf-8"))
    response = get(url, headers=header)
    return response

def action_wrapper(hermes, intentMessage, conf):
    from requests import put, get
    import json

    current_session_id = intentMessage.session_id
    try:
     if len(intentMessage.slots.state) > 0:
        myState = intentMessage.slots.state.first().value
        theIntent = intentMessage.slots.state.first().value
     if len(intentMessage.slots.device_name) > 0:
        myDeviceId = intentMessage.slots.device_name.first().value
     mytoken = conf['secret']['bearer-auth-token']
     myapi = conf['secret']['rest-api-url']
     auth = 'Bearer ' + key.encode("utf-8")
     header = {'Authorization': auth, 'Content-Type': 'application/json'}
     DeviceIDs = ['09b0803c-cfe3-4b8a-8fc0-e8161701ade4', '2537cac5-2c28-454f-bdc2-5741ae4c44c4',  '7c792f42-a018-4664-af72-d41cf93b49df', '1d9b3329-4d6f-493d-baac-1ee84cec75e8', '5d5a7635-f1a5-40ac-ad1f-d75967545824']
     print header
     print myState
     print myDeviceId
#     hermes.publish_end_session(current_session_id, myDeviceId)
     if myDeviceId == "lights":
       theTarget = "all_lights"
     if myDeviceId == "lamps":
       theTarget = "lamps"
     else:
       theTarget = "one_light"
     if theTarget == "all_lights":
       if myState == "on" or myState == "off":
         for index in range(len(DeviceIDs)):
           call_command_api(myapi.encode("utf-8"), header.encode("utf-8"), DeviceIDs[index], myState.encode("utf-8"))
         hermes.publish_end_session(current_session_id, "Turning " + myState.encode("utf-8") + " " + myDeviceId.encode("utf-8"))
#     if myState != "query":
#       url = 'http://'+ myip.encode("utf-8") + ':' + myport.encode("utf-8") + '/api/states/' + theDevice
#       response = get(url, headers=header)
#       if response.json()['state'] != myState:
#         payload = json.dumps({"entity_id": theDevice})
#         url = 'http://'+ myip.encode("utf-8") + ':' + myport.encode("utf-8") + '/api/services/homeassistant/turn_' + myState.encode("utf-8")
#         response = post(url, headers=header, data=payload)
#         hermes.publish_end_session(current_session_id, "Turning " + myState.encode("utf-8") + " " + myDeviceId.encode("utf-8"))
#       else:
#         hermes.publish_end_session(current_session_id, "Be Boop Beep. Um, " + myDeviceId.encode("utf-8") + " is already turned " + myState.encode("utf-8"))
     else:
#       url = 'http://'+ myip.encode("utf-8") + ':' + myport.encode("utf-8") + '/api/states/' + theDevice
#       response = get(url, headers=header)
#       hermes.publish_end_session(current_session_id, myDeviceId.encode("utf-8") + " is " + response.json()['state'])
       hermes.publish_end_session(current_session_id, "Be boop be be boop, something has gone terribly wrong")
    except:
#       print 'http://'+ myip.encode("utf-8") + ':' + myport.encode("utf-8") + '/api/states/' + myDeviceId.encode("utf-8")
#       print myDeviceName.encode("utf-8")
#       print myDeviceId.encode("utf-8")
      hermes.publish_end_session(current_session_id, "Be boop be be boop, something has gone terribly wrong")


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
#    with Hermes("localhost:1883") as h:
        h.subscribe_intent("hooray4me:control_devices", subscribe_intent_callback) \
         .start()
