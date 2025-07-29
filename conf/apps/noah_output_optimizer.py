import hassapi as hass
import adbase as ad

#
# Hello World App
#
# Args:
#


class Manager(ad.ADBase):
    def initialize(self):
        self.adapi = self.get_ad_api()
        my_entity = self.adapi.get_entity("sensor.noah_2000_bat0_soc")
        state = my_entity.get_state("state")
        self.adapi.log(my_entity)
        self.adapi.log(state)
        self.adapi.log("Hello from AppDaemon")
        self.adapi.log("You are now ready to run Apps!")
