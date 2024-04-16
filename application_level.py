"""
Created on 2023-04-20

@author: KFU
"""
import cast_upgrade_1_6_13  # @UnusedImport
import cast.application
from cast.analysers import log


class XXXApplicationLevel(cast.application.ApplicationLevelExtension):

    def end_application_create_objects(self, application):
        pass

    def end_application(self, application):
        log.info('Starting Application level Analysis for XXX Framework...')

        # Example use of the intermediate file to transfer content from analyzer level to application level
        exchange_file = self.get_intermediate_file('com.castsoftware.uc.XXX.txt')

        # Example use of a utility method to keep code organized
        self._my_internal_utility_method(exchange_file)

    def _my_internal_utility_method(self, exchange_file):
        pass
