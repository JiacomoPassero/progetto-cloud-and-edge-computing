import unittest
import re
import os

"""Support Function to extract the text of the header"""
def extract_header_text(post_path, separator):
    with open(post_path, 'r') as template_file:
        header_text = ""
        #Extract lines unitl "---" that marks the end of the header
        for line in template_file:
            if separator in line:
                break
            else:
                header_text += line
    return header_text

"""Functuon to extract the template from an header file"""
def extract_fields(post_path, separator):
    #Extract post structure from template file
    header_text = extract_header_text(post_path, separator)

    #Using regex to extract only the fileds name
    field_pattern = re.compile(r'^(\w+): .+', re.MULTILINE)
    required_fields = field_pattern.findall(header_text)
    return required_fields

"""Check if the post contains the separator line between the header and the body"""
def contains_separator(post_path, separator):
    #iter over file line
    with open(post_path, 'r') as template_file:
        header_text = ""
        #check if the separator line is present
        for line in template_file:
            #separator is a single line
            if separator + "\n" == line:
                return True
    return False

"""Extraxt the string value of a field to be checked inside the test"""
def extract_field_value(post_path, field):
    #extract the jeader
    header_text = extract_header_text(post_path, separator)
    #build abd apply the regex
    regex = f'^{field}: .+'
    field_pattern = re.compile(regex, re.MULTILINE)
    field_line = field_pattern.findall(header_text)
    #return only the value of the line stripped from excessive spaces
    return field_line[0].split(":")[1].strip()

class PostValidator(unittest.TestCase):
    def setUp(self):
        self.template_path = "./posts/template.md.tmpl"
        self.posts_path = "./posts/en/"
        self.separator = "---"

    def testStructure(self):
        #if file not present than the setup fails
        template_fields = extract_fields(self.template_path, self.separator)
        if len(template_fields) == 0:
            self.fail("Failed to extract the post template fields, check template indentation")
        
        #every post must have the same header fields of the template 
        for post in os.listdir(self.posts_path):
            post_path = os.path.join(self.posts_path, post)

            #check if separator between content and header is present
            self.assertTrue(contains_separator(post_path, self.separator), f"Post {post} does not contains header separator")

            #extract and compare the post header
            post_fields = extract_fields(os.path.join(self.posts_path, post), self.separator) 
            self.assertEqual(post_fields, template_fields, f"Post {post} does not match the template header structure")
            
            #check date format
            date = extract_field_value(post_path, "date")



            




