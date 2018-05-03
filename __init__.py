# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
from os.path import dirname

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger


import requests

__author__ = 'Rahul Kumar Shandilya'

LOGGER = getLogger(__name__)


class ItsmUserSkill(MycroftSkill):
    def __init__(self):
        super(ItsmUserSkill, self).__init__(name="ItsmUserSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))
        
        
        itsm_user_intent = IntentBuilder("itsmuserintent"). \
            require("ItsmUserKeyword").build()
        self.register_intent(itsm_user_intent, self.handle_itsm_user_intent)

        #how_are_you_intent = IntentBuilder("HowAreYouIntent"). \
        #    require("HowAreYouKeyword").build()
        #self.register_intent(how_are_you_intent,
        #                     self.handle_how_are_you_intent)

        #hello_world_intent = IntentBuilder("HelloWorldIntent"). \
        #    require("HelloWorldKeyword").build()
        #self.register_intent(hello_world_intent,
        #                     self.handle_hello_world_intent)

    def handle_itsm_user_intent(self, message):
        url = 'https://dev22921.service-now.com/api/now/table/v_transaction?sysparm_query=foreground%3Dtrue&sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_fields=user%2Curl%2Ctype%2Cage'
        user = '531834'
        pwd = 'Welcome!2345'
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )
        # Check for HTTP codes other than 200
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()
        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        r = data['result']
        x = 0
        length = len(data['result'])
        detail = ""
        for x in range(0, length):
            if r[x]['age'].find("Minute") != -1:
                detail += "A transaction run by {} of type {} is running on the table {} for more than 30 seconds ".format(r[x]['user'], r[x]['type'], r[x]['url'])
            x += 1

        self.speak("Hello")
        #self.speak(detail)
        self.speak("Please look into the issue as it may become serious")
        

    def stop(self):
        pass


def create_skill():
    return ItsmUserSkill()
