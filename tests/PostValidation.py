import unittest
import re
import os
"""Fnctuon to extract the template from an header file"""
def extract_fields(post_path):
    #Extract post structure from template file
    with open(post_path, 'r') as template_file:
        header_text = ""
        #Extract lines unitl "---" that marks the end of the header
        for line in template_file:
            if "---" in line:
                break
            else:
                header_text += line

        #Using regex to extract only the fileds name
        field_pattern = re.compile(r'^(\w+): .+', re.MULTILINE)
        required_fields = field_pattern.findall(header_text)
        return required_fields


class PostValidator(unittest.TestCase):
    def setUp(self):
        self.template_path = "./posts/template.md.tmpl"
        self.posts_path = "./posts/en/"

    def testStructure(self):
        #if file not present than the setup fails
        template_fields = extract_fields(self.template_path)
        if len(template_fields) == 0:
            self.fail("Failed to extract the post template fields, check template indentation")
        
        #every post must have the same header fields of the template 
        for post in os.listdir(self.posts_path):
            #extract and compare the post header
            post_fields = extract_fields(os.path.join(self.posts_path, post)) 
            self.assertEqual(post_fields, template_fields, f"Post {post} does not match the template header structure")



            




