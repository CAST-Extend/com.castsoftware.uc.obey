"""
Created on 2023-04-20

@author: KFU
"""
import cast_upgrade_1_6_13  # @UnusedImport
import cast.analysers.jee
from cast.analysers import log, CustomObject, Type
from cast.application import open_source_file
import re


class XXXAnalyzerLevel(cast.analysers.jee.Extension):

    def __init__(self):
        # Example use of the intermediate file to transfer content from analyzer level to application level.
        # It requires declaration.
        self.exchange_file = None

    def start_analysis(self, options):
        """
        @type options: cast.analysers.JEEExecutionUnit
        """
        log.info('Starting JEE Analysis for XXX Framework...')

        # Creating the temporary file to exchange data between the analyzer level and the application level
        self.exchange_file = self.get_intermediate_file('com.castsoftware.uc.XXX.txt')
        log.info('Created file com.castsoftware.uc.XXX.txt to store intermediary findings')

        # Example use of the lib folder
        # Adding a classpath for XXX
        options.add_classpath('lib')
        log.info('Added XXX JARs to the classpath')

    def end_analysis(self):
        log.info('Ending JEE Analysis for XXX Framework')

    def start_member(self, member):
        """
        @type member: cast.analysers.Member
        """

        # Example use of a utility method to keep code organized, by passing the member traversed to the utility
        self._my_internal_utility_method(member)

        # Example use of the intermediate file, by writing to it
        # Here there is no selection criteria. You obviously need to add the logic relevant for your use case.
        data_to_store = 'BINDING;' + member.get_fullname() + ';'
        self.exchange_file.write(data_to_store + '\n')

    def _my_internal_utility_method(self, member):
        """
        @type member: cast.analysers.Member
        """
        pass
