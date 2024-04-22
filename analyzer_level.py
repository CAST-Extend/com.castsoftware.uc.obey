"""
Created on 2024-04-18

@author: TAL / KFU
"""
import cast.analysers.ua
from cast.analysers import log, CustomObject


class OBEYAnalyzerLevel(cast.analysers.ua.Extension):

    def __init__(self):
        # Example use of the intermediate file to transfer content from analyzer level to application level.
        # It requires declaration.
        self.exchange_file = None

    def start_analysis(self):
        log.info('Starting UA Analysis for Mainframe OBEYs...')

        # Creating the temporary file to exchange data between the analyzer level and the application level
        # self.exchange_file = self.get_intermediate_file('com.castsoftware.uc.XXX.txt')
        # log.info('Created file com.castsoftware.uc.XXX.txt to store intermediary findings')

        # Example use of the lib folder
        # Adding a classpath for XXX
        # options.add_classpath('../template-sdk-extension/lib')
        # log.info('Added XXX JARs to the classpath')

    def end_analysis(self):
        log.info('Ending UA Analysis for Mainframe OBEYs')

    def start_file(self, file):
        """
        @type file: cast.analysers.File
        """
        log.info('Starting file: ' + file.get_path())
        print('Starting file: ' + file.get_path())
        # If the extension is not .OBEY, we skip the file
        if not file.get_path().endswith('.obey'):
            return

        # Create a new object of type 'OBEY_FILE in the KB
        obeyObj = CustomObject()
        # Set the name of the object to the name of the file without the extension
        obeyObj.set_name(file.get_name())
        obeyObj.set_type('OBEY_FILE')
        obeyObj.set_parent(file)
        obeyObj.save()

    def _my_internal_utility_method(self, member):
        """
        @type member: cast.analysers.Member
        """
        pass
