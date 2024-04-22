"""
Created on 2023-04-20

@author: TAL / KFU
"""
import unittest
import cast.analysers.test


class OBEYTest(unittest.TestCase):

    def test_01(self):
        analysis = run_analyzer_level(['sample_of_code_1'])
        # self.assertTrue(obj_interface)
        # Print all objects in the KB
        print("Printing analysis results:")
        for obj in analysis.get_objects_by_category('OBEYJob').values():
            print(getattr(obj, 'identification.fullName'))
        for obj in analysis.get_objects_by_category('OBEYPhysicalFile').values():
            print(getattr(obj, 'identification.fullName'))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testRegisterPlugin']
    unittest.main()

# very useful line of code do not remove
# log is located in C:\Users\%username%\AppData\Local\Temp\CAST\CAST\8.3\LTSA\log_default.castlog.tmp
def run_analyzer_level(selectionPath, verbose=True):
    analysis = cast.analysers.test.UATestAnalysis('OBEY')
    analysis.pydev_path = '';
    for item in selectionPath:
        analysis.add_selection(item)
    analysis.add_dependency(r"C:\CAST\ProgramData\CAST\CAST\Extensions\com.castsoftware.internal.platform.0.9.23")
    analysis.set_verbose(verbose)
    analysis.run()
    return analysis
