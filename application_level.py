"""
Created on 2024-04-18

@author: TAL / KFU
"""
import cast_upgrade_1_6_13
import cast.application
from cast.analysers import log


class OBEYApplicationLevel(cast.application.ApplicationLevelExtension):

    def end_application_create_objects(self, application):
        pass

    def end_application(self, application):
        log.info('Starting Application level Analysis for OBEY files...')
    def _my_internal_utility_method(self):
        pass
