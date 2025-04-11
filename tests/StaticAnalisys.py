import unittest
import re

'''Simple static analysis of the code that checks that the code is not in debug mode in production'''
class StaticAnalysis(unittest.TestCase):
    
    #check if somewhere in the code there are parameters such as debug=true
    def test_mode(self):
        app_code = ""
        with open("./app.py", 'r') as app_file:
            app_code = app_file.read()    
            #serach the pattern using a regex
        field_pattern = re.compile(r'^.+debug=.+', re.MULTILINE)
        faulty_lines = field_pattern.findall(app_code)
        #for every line that assign a debug variable check if the assigment is true
        for line in faulty_lines:
            if ("debug=True" in line.strip()) or ("debut=1" in line.strip()):
                self.fail(f'Debug mode is enabled in production: {line.strip()}')


    