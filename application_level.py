"""
Created on 2024-04-18

@author: TAL / KFU
"""

import cast_upgrade_1_6_13
import cast.application
from cast.application import create_link
from cast.application import CustomObject
import logging


class ObeyApplicationLevel(cast.application.ApplicationLevelExtension):
    def end_application_create_objects(self, application):
        self._log('Starting Application level object creation for Obey files...')
        obey_jobs = application.objects().has_type('ObeyJob')
        cobol_programs = application.objects().has_type('CAST_COBOL_SavedProgram')
        self._log('Opening file com.castsoftware.uc.obey.txt to retrieve intermediary findings')
        exchange_file = self.get_intermediate_file('com.castsoftware.uc.obey.txt')
        # exchange_file = open('com.castsoftware.uc.obey.txt', 'r')
        self._log('Reading file com.castsoftware.uc.obey.txt to retrieve intermediary findings')
        for line in exchange_file:
            data = line.split(';')
            # remove last element which is '\n'
            data = data[:-1]
            obey_job_name = data[0]
            cobol_program_name = data[1]

            obeyJobObj = None
            COBOLProgramObj = None
            for obey_job in obey_jobs:
                if obey_job.get_name() == obey_job_name:
                    obeyJobObj = obey_job
                    break
            for cobol_program in cobol_programs:
                if cobol_program.get_name() == cobol_program_name:
                    COBOLProgramObj = cobol_program
                    break

            # link between ObeyJob and the COBOLProgram
            if obeyJobObj is not None and COBOLProgramObj is None:
                unknown_cobol_program = CustomObject()
                unknown_cobol_program.set_type('CAST_COBOL_ProgramPrototype')
                unknown_cobol_program.set_name(cobol_program_name)
                unknown_cobol_program.set_external()
                unknown_cobol_program.set_parent(obeyJobObj)
                unknown_cobol_program.save()
                self._log('Unknown COBOL Program: ' + cobol_program_name + ' created')

                create_link('callLink', obeyJobObj, unknown_cobol_program)
                self._log('Link created between ' + obey_job_name + ' and ' + cobol_program_name)
        exchange_file.close()

    def _log(self, msg, level='info'):
        msg = '[com.castsoftware.uc.obey] ' + msg
        if level == 'info':
            logging.info(msg)
        elif level == 'debug':
            logging.debug(msg)
        elif level == 'warning':
            logging.warning(msg)
        elif level == 'error':
            logging.error(msg)
        else:
            logging.info(msg)

    def end_application(self, application):
        self._log('Starting Application level Analysis for Obey files...')

        cobol_programs = application.objects().has_type('CAST_COBOL_SavedProgram')
        cobol_file_links = application.objects().has_type('CAST_COBOL_SavedFileDescription')
        for cobol_file_link in cobol_file_links:
            self._log('COBOL File Link: ' + cobol_file_link.get_name())
        obey_physical_files = application.objects().has_type('ObeyPhysicalFile')
        obey_jobs = application.objects().has_type('ObeyJob')

        self._log('Opening file com.castsoftware.uc.obey.txt to retrieve intermediary findings')
        exchange_file = self.get_intermediate_file('com.castsoftware.uc.obey.txt')
        # exchange_file = open('com.castsoftware.uc.obey.txt', 'r')
        self._log('Reading file com.castsoftware.uc.obey.txt to retrieve intermediary findings')
        for line in exchange_file:
            data = line.split(';')
            # remove last element which is '\n'
            data = data[:-1]
            obey_job_name = data[0]
            cobol_program_name = data[1]

            obeyJobObj = None
            COBOLProgramObj = None
            for obey_job in obey_jobs:
                if obey_job.get_name() == obey_job_name:
                    obeyJobObj = obey_job
                    break
            for cobol_program in cobol_programs:
                if cobol_program.get_name() == cobol_program_name:
                    COBOLProgramObj = cobol_program
                    break

            # link between ObeyJob and the COBOLProgram
            if obeyJobObj is not None and COBOLProgramObj is not None:
                create_link('callLink', obeyJobObj, COBOLProgramObj)
                self._log('Link created between ' + obey_job_name + ' and ' + cobol_program_name)
            if len(data) > 2:
                dataFileLink = []
                if COBOLProgramObj is not None:
                    COBOLProgramObj.load_children() # load children to access them
                    childrens = COBOLProgramObj.get_children()
                    links = application.links().has_callee(cobol_file_links)
                    for link in links:
                        for child in childrens:
                            # if the child of the COBOLProgram is the caller of the link, so if the COBOL Paragraph calling the Cobol
                            # Data File Link is a child of the COBOL Program then we add the Cobol Data File Link to the Cobol Program
                            if child.id == link.get_caller().id:
                                self._log('Caller: ' + link.get_caller().get_name() + ' Callee: ' + link.get_callee().get_name())
                                dataFileLink.append(link.get_callee())

                self._log('DataFileLink: ' + str(dataFileLink))

                for i in range(2, len(data), 2):
                    cobol_file_link_name = data[i]
                    obey_physical_file_name = data[i + 1]

                    ObeyPhysicalFileObj = None
                    for obey_physical_file in obey_physical_files:
                        if obey_physical_file.get_name() == obey_physical_file_name:
                            ObeyPhysicalFileObj = obey_physical_file
                            break

                    # link between the ObeyJob and the ObeyPhysicalFile
                    if obeyJobObj is not None and ObeyPhysicalFileObj is not None:
                        create_link('useLink', obeyJobObj, ObeyPhysicalFileObj)
                        self._log('Link created between ' + obey_job_name + ' and ' + obey_physical_file_name)
                        print('Link created between ' + obey_job_name + ' and ' + obey_physical_file_name)

                    # link between the COBOLDataFileLink and the ObeyPhysicalFile
                    if len(dataFileLink) > 0 and ObeyPhysicalFileObj is not None:
                        for cobol_file_link in dataFileLink:
                            if cobol_file_link_name == cobol_file_link.get_name():
                                create_link('useLink', cobol_file_link, ObeyPhysicalFileObj)
                                self._log('Link created between ' + cobol_file_link.get_name() + ' and ' + obey_physical_file_name)
                                print('Link created between ' + cobol_file_link.get_name() + ' and ' + obey_physical_file_name)
                                break
                            else:
                                self._log('No link created between ' + cobol_file_link_name + ' and ' + obey_physical_file_name + ' because ' + cobol_file_link_name + 'is different from ' + cobol_file_link.get_name())

        exchange_file.close()
        self._log('Ending Application level Analysis for Obey files')


def _my_internal_utility_method(self):
    pass
