"""
Created on 2024-04-18

@author: TAL / KFU
"""
import re

import cast_upgrade_1_6_13
import cast.analysers.ua
from cast.analysers import log, CustomObject, Bookmark

class OBEYPhysicalFile():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def save(self):
        physicalFile = CustomObject()
        physicalFile.set_name(self.name)
        physicalFile.set_type('OBEYPhysicalFile')
        physicalFile.set_parent(self.parent)
        physicalFile.set_fullname(self.name)
        physicalFile.save()

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, OBEYPhysicalFile):
            return self.name == other.name
        return False

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

class OBEYAnalyzerLevel(cast.analysers.ua.Extension):

    def __init__(self):
        # Example use of the intermediate file to transfer content from analyzer level to application level.
        # It requires declaration.
        self.exchange_file = None
        self.obeyPhysicalFiles = set()


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
        # For each element in the obeyPhysicalFiles set, save the object in the KB
        for obeyPhysicalFile in self.obeyPhysicalFiles:
            obeyPhysicalFile.save()
        log.info('Ending UA Analysis for Mainframe OBEYs')

    def start_file(self, file):
        """
        @type file: cast.analysers.File
        """
        # If the extension is not .OBEY or .obey, we skip the file
        if not file.get_path().lower().endswith('.obey'):
            log.info('Skipping file: ' + file.get_path())
            print('Skipping file: ' + file.get_path())
            return

        # Open the file and read the content
        # Store the number of lines in the file
        file_line_count = 0
        column_count_last_line = 0
        with open(file.get_path(), 'r') as f:
            file_lines = f.readlines()
            file_line_count = len(file_lines)
            if file_line_count == 0:
                return  # Empty file
            print('File line -1: ' + str(file_lines))
            file_last_column_length = len(file_lines[-1])

        # Create a new object of type 'OBEY_FILE in the KB
        obeyJob = CustomObject()
        # Set the name of the object to the name of the file without the extension
        obeyJob.set_name(file.get_name())
        obeyJob.set_type('OBEYJob')
        obeyJob.set_parent(file)
        obeyJob.save()

        # Create a bookmark for the object
        obeyJobBookMark = Bookmark(file, 0, 0, file_line_count, file_last_column_length)
        obeyJob.save_position(obeyJobBookMark)
        with open(file.get_path(), 'r') as f:
            for line in f:
                # Check for RegEx pattern in the line
                # If found, create a new object of type 'OBEYPhysicalFile' in the KB
                results = re.search(r"ASSIGN +([A-Z\-0-9]+), +(.*)", line)
                if results:
                    obeyPhysicalFile = OBEYPhysicalFile(results.group(2), file)
                    self.obeyPhysicalFiles.add(obeyPhysicalFile)