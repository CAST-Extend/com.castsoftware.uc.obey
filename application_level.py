"""
Created on 2024-04-18

@author: TAL / KFU
"""
import cast_upgrade_1_6_13
import cast.application
from cast.application import create_link
import logging


class ObeyApplicationLevel(cast.application.ApplicationLevelExtension):

    def end_application_create_objects(self, application):
        pass

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

        # Retrieve the COBOL Programs
        cobol_programs = application.objects().has_type('CAST_COBOL_SavedProgram')
        # for cobol_program in cobol_programs:
        #     log.info('COBOL Program: ' + cobol_program.get_name())
        cobol_file_link = application.objects().has_type('CAST_COBOL_SavedFileDescription')
        # for cobol_file in cobol_file_link:
        #     log.info('COBOL File Link: ' + cobol_file.get_name())
        obey_physical_files = application.objects().has_type('ObeyPhysicalFile')
        # for obey_physical_file in obey_physical_files:
        #     log.info('Obey Physical File: ' + obey_physical_file.get_name())
        obey_jobs = application.objects().has_type('ObeyJob')
        # for obey_job in obey_jobs:
        #     log.info('Obey Job: ' + obey_job.get_name())
        self._log('Opening file com.castsoftware.uc.obey.txt to retrieve intermediary findings')
        exchange_file = self.get_intermediate_file('com.castsoftware.uc.obey.txt')
        # exchange_file = open('com.castsoftware.uc.obey.txt', 'r')
        self._log('Reading file com.castsoftware.uc.obey.txt to retrieve intermediary findings')
        for line in exchange_file:
            # Format is OBEYJobName;cobolProgramName;cobolFileLinkName1;OBEYPhysicalFileNam1e;cobolFileLinkName2;OBEYPhysicalFileName2 ...
            data = line.split(';')
            # Remove last element which is '\n'
            data = data[:-1]
            obey_job_name = data[0]
            cobol_program_name = data[1]

            # link between ObeyJob and the COBOLProgram
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
            if obeyJobObj is not None and COBOLProgramObj is not None:
                l = create_link('useLink', obeyJobObj, COBOLProgramObj)
                self._log('Link created between ' + obey_job_name + ' and ' + cobol_program_name)

            if len(data) > 2:
                for i in range(2, len(data), 2):
                    cobol_file_link_name = data[i]
                    obey_physical_file_name = data[i + 1]
                    # link between the ObeyJob and the ObeyPhysicalFile
                    ObeyPhysicalFileObj = None
                    for obey_physical_file in obey_physical_files:
                        if obey_physical_file.get_name() == obey_physical_file_name:
                            ObeyPhysicalFileObj = obey_physical_file
                            break
                    if obeyJobObj is not None and ObeyPhysicalFileObj is not None:
                        l = create_link('useLink', obeyJobObj, ObeyPhysicalFileObj)
                        self._log('Link created between ' + obey_job_name + ' and ' + obey_physical_file_name)
                        print('Link created between ' + obey_job_name + ' and ' + obey_physical_file_name)

        exchange_file.close()
        self._log('Ending Application level Analysis for Obey files')


def _my_internal_utility_method(self):
    pass

