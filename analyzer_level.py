"""
Created on 2024-04-18

@author: TAL / KFU
"""
import re

import cast_upgrade_1_6_13
import cast.analysers.ua
from cast.analysers import log, CustomObject, Bookmark


class ObeyPhysicalFile:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def save(self):
        physicalFile = CustomObject()
        physicalFile.set_name(self.name)
        physicalFile.set_type('ObeyPhysicalFile')
        physicalFile.set_parent(self.parent)
        physicalFile.set_fullname(self.name)
        physicalFile.save()

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, ObeyPhysicalFile):
            return self.name == other.name
        return False

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(self.name)


class ObeyAnalyzerLevel(cast.analysers.ua.Extension):

    def __init__(self):
        # Example use of the intermediate file to transfer content from analyzer level to application level.
        # It requires declaration.
        self.exchange_file = None
        self.obeyPhysicalFiles = set()
        self.dataDict = {}


    def start_analysis(self):
        log.info('Starting UA Analysis for Obey files...')

        # Creating the temporary file to exchange data between the analyzer level and the application level
        self.exchange_file = self.get_intermediate_file('com.castsoftware.uc.obey.txt')
        log.info('Created file com.castsoftware.uc.obey.txt to store intermediary findings')

    def end_analysis(self):
        # For each element in the obeyPhysicalFiles set, save the object in the KB
        for obeyPhysicalFile in self.obeyPhysicalFiles:
            obeyPhysicalFile.save()
        for key in self.dataDict:
            for subKey in self.dataDict[key]:
                self.exchange_file.write(key + ';' + subKey + ';')
                for dataTuple in self.dataDict[key][subKey]:
                    self.exchange_file.write(dataTuple[0] + ';' + dataTuple[1] + ';')
                self.exchange_file.write('\n')
        log.info('Ending UA Analysis for Obey files')

    def start_file(self, file):
        """
        @type file: cast.analysers.File
        """
        # If the extension is not .obey or .obey, we skip the file
        if not file.get_path().lower().endswith('.obey'):
            log.info('Skipping file: ' + file.get_path())
            print('Skipping file: ' + file.get_path())
            return

        # Open the file and read the content
        # Store the number of lines in the file
        with open(file.get_path(), 'r') as f:
            file_lines = f.readlines()
            file_line_count = len(file_lines)
            if file_line_count == 0:
                return  # Empty file
            print('File line -1: ' + str(file_lines))
            file_last_column_length = len(file_lines[-1])

        # Create a new object of type 'Obey_FILE in the KB
        obeyJob = CustomObject()
        # Set the name of the object to the name of the file without the extension
        obeyJobName = file.get_name().split('.')[0]
        obeyJob.set_name(obeyJobName)
        obeyJob.set_type('ObeyJob')
        obeyJob.set_parent(file)
        obeyJob.save()

        # Create a bookmark for the object
        obeyJobBookMark = Bookmark(file, 0, 0, file_line_count, file_last_column_length)
        obeyJob.save_position(obeyJobBookMark)

        currentFileTuples = []

        with open(file.get_path(), 'r') as f:
            for line in f:

                #TODO: Modify ReGex
                clearResults = re.search(r"CLEAR  ALL", line)
                if clearResults:
                    # Clear the currentFileTuples list
                    currentFileTuples.clear()

                # TODO: Modify RegEx to handle comments within the code
                assignResults = re.search(r"ASSIGN +([A-Z\-0-9]+), +(.*)", line)
                if assignResults and assignResults.group(1) and assignResults.group(2):
                    currentFileTuples.append((assignResults.group(1), assignResults.group(2)))

                    obeyPhysicalFile = ObeyPhysicalFile(assignResults.group(2), file)
                    self.obeyPhysicalFiles.add(obeyPhysicalFile)

                # TODO: Modify RegEx to handle comments within the code
                runResults = re.search(r"\s+RUN\s+(?:\S+\.)*(\S+)", line)
                if runResults and runResults.group(1):
                    # If dataDict does not contain the name of the file, add it
                    if obeyJobName not in self.dataDict:
                        self.dataDict[obeyJobName] = {}

                    # If runResults.group(1) is not in the dataDict, add it
                    if runResults.group(1) not in self.dataDict[obeyJobName]:
                        self.dataDict[obeyJobName][runResults.group(1)] = []

                    # Add the currentFileTuples to the dataDict
                    for currentFileTuple in currentFileTuples:
                        self.dataDict[obeyJobName][runResults.group(1)].append(currentFileTuple)
