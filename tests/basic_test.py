"""
Created on 2023-04-20

@author: KFU
"""
import unittest
import cast.analysers.test
from cast.application.test import TestKnowledgeBase
from cast.application import KnowledgeBase, create_postgres_engine
from application_level import XXXApplicationLevel


class XXXTest(unittest.TestCase):

    def test_01(self):
        analysis = run_analyzer_level(['sample_of_code_1'])
        obj_expected = analysis.get_object_by_name('XXX_YYY')
        print('Found: ' + str(obj_expected))
        i = 0
        for o in analysis.get_objects_by_category('XXX_YYY').values():
            print('Match ' + str(i) + ' : ' + str(o))
            i += 1
        # self.assertTrue(obj_interface)

    def test_application_init(self):
        analysis = TestKnowledgeBase()

        extension = XXXApplicationLevel()
        application = analysis.run(extension.end_application)

    def test_XXX_on_KB_already_created(self):
        engine = create_postgres_engine(port=2284)
        kb = KnowledgeBase('XXX_sample_local', engine)
        app = kb.get_application(name='XXX-sample')
        objects = app.objects()
        count = 0
        for object in objects.is_executable().has_type('JV_METHOD'):

            if object.get_fullname().find('com.example.') > -1:
                count += 1
                print(object.get_fullname())
                try:
                    for annotation in object.get_annotations():
                        print('     ' + str(annotation))
                except AttributeError:
                    pass

        print(str(count))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testRegisterPlugin']
    unittest.main()


# very useful line of code do not remove
# log is located in C:\Users\%username%\AppData\Local\Temp\CAST\CAST\8.3\LTSA\log_default.castlog.tmp
def run_analyzer_level(selectionPath, verbose=False):
    analysis = cast.analysers.test.JEETestAnalysis()
    analysis.pydev_path = '';
    for item in selectionPath:
        analysis.add_selection(item)
    # analysis.add_dependency(r"C:\CAST\ProgramData\CAST\CAST\Extensions\com.castsoftware.jee.1.3.8-funcrel")
    analysis.add_dependency(r"C:\CAST\ProgramData\CAST\CAST\Extensions\com.castsoftware.internal.platform.0.9.12")
    analysis.set_verbose(verbose)
    analysis.run()
    return analysis

