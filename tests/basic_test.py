"""
Created on 2023-04-20

@author: TAL / KFU
"""
import unittest
import cast.analysers.test
from cast.application.test import run
from cast.application import KnowledgeBase, create_postgres_engine
from application_level import ObeyApplicationLevel


class ObeyTest(unittest.TestCase):

    def test_01(self):
        analysis = run_analyzer_level(['sample_of_code_1'])
        # Print all objects in the KB
        print("Printing analysis results:")
        for obj in analysis.get_objects_by_category('ObeyJob').values():
            print(getattr(obj, 'identification.fullName'))
        for obj in analysis.get_objects_by_category('ObeyPhysicalFile').values():
            print(getattr(obj, 'identification.fullName'))

    def test_02(self):
        run_analyzer_level(['sample_of_code_1'])

    def test_application_init(self):
        engine = create_postgres_engine(port=2284)
        run(kb_name='obeys_local', application_name='OBeys', engine=engine, event='end_application')

    def test_obey_on_KB_already_created(self):
        engine = create_postgres_engine(port=2284)
        kb = KnowledgeBase('obeys_local', engine)
        application = kb.get_application(name='Obeys')

        cobol_programs = application.objects().has_type('CAST_COBOL_SavedProgram')
        for cobol_program in cobol_programs:
            print('COBOL Program: ' + cobol_program.get_name())
        obey_physical_files = application.objects().has_type('ObeyPhysicalFile')
        for obey_physical_file in obey_physical_files:
            print('Obey Physical File: ' + obey_physical_file.get_name())
        obey_jobs = application.objects().has_type('ObeyJob')
        for obey_job in obey_jobs:
            print('Obey Job: ' + obey_job.get_name())
            print(obey_job.get_positions())
    def test_obey_on_KB_already_created_test(self):
        engine = create_postgres_engine(port=2284)
        kb = KnowledgeBase('obeys_local', engine)
        application = kb.get_application(name='Obeys')
        extension = ObeyApplicationLevel()
        extension.end_application(application)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testRegisterPlugin']
    unittest.main()


# very useful line of code do not remove
# log is located in C:\Users\%username%\AppData\Local\Temp\CAST\CAST\8.3\LTSA\log_default.castlog.tmp
def run_analyzer_level(selection_path, verbose=True):
    analysis = cast.analysers.test.UATestAnalysis('Obey')
    analysis.pydev_path = ''
    for item in selection_path:
        analysis.add_selection(item)
    analysis.add_dependency(r"C:\CAST\ProgramData\CAST\CAST\Extensions\com.castsoftware.internal.platform.0.9.23")
    analysis.set_verbose(verbose)
    analysis.run()
    return analysis
