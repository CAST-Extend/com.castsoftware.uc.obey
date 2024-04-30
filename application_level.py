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

    def __init__(self):
        super().__init__()
        self.unknown_cobol_map = {}
        self._log("Constructor called")
        self._log(self.unknown_cobol_map)

    def end_application_create_objects(self, application):
        self._log('Starting Application level object creation for Obey files...')
        obey_jobs = application.objects().has_type('ObeyJob')

        # iterate on all the self.unknown_cobol_map keys
        for obeyJobName in self.unknown_cobol_map.keys():
            found = False
            for obeyJob in obey_jobs:
                if obeyJob.get_name() == obeyJobName:
                    found = True
                    break
            if not found:
                # skip the creation of the unknown COBOL Program if the ObeyJob is not found
                continue

            # create a CAST_COBOL_ProgramPrototype object (Unknown COBOL Program)
            for cobol_program_name in self.unknown_cobol_map[obeyJobName]:
                unknown_cobol_program = CustomObject()
                unknown_cobol_program.set_type('CAST_COBOL_ProgramPrototype')
                unknown_cobol_program.set_name(cobol_program_name)
                unknown_cobol_program.set_external()
                unknown_cobol_program.save()
                self._log('Unknown COBOL Program: ' + cobol_program_name + ' created')

                create_link('callLink', obeyJobName, unknown_cobol_program)
                self._log('Link created between ' + obeyJobName + ' and ' + cobol_program_name)

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
        cobol_file_link = application.objects().has_type('CAST_COBOL_SavedFileDescription')
        obey_physical_files = application.objects().has_type('ObeyPhysicalFile')
        obey_jobs = application.objects().has_type('ObeyJob')
        links = application.links().has_caller(cobol_programs)
        for link in links:
            print(link.get_caller().get_name() + ' calls ' + link.get_callee().get_name())
            self._log(link.get_caller().get_name() + ' calls ' + link.get_callee().get_name())

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
            elif obeyJobObj is not None:
                # keep reference to obeyJobObj link to COBOLProgramObj in order to create a CAST_COBOL_ProgramPrototype object (Unknown COBOL Program)
                if self.unknown_cobol_map[obey_job_name]:
                    self.unknown_cobol_map[obey_job_name].append(cobol_program_name)
                else:
                    self.unknown_cobol_map[obey_job_name] = [cobol_program_name]


            if len(data) > 2:
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

        exchange_file.close()
        self._log('Ending Application level Analysis for Obey files')


def _my_internal_utility_method(self):
    pass

