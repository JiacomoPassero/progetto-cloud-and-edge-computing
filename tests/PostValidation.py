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
def extract_field_value(post_path, separator,field):
    #extract the jeader
    header_text = extract_header_text(post_path, separator)
    #build abd apply the regex
    regex = f'^{field}: .+'
    field_pattern = re.compile(regex, re.MULTILINE)
    field_line = field_pattern.findall(header_text)
    #return only the value of the line stripped from excessive spaces
    return field_line[0].split(":")[1].strip()

"""The methond validates just the sintaxt of the date, not the semantic"""
def check_date(date):
    #extract the component of the date
    date = date.split(" ")

    month = date[0].strip().lower()
    day = int(date[1].replace(",",""))
    year = int(date[2])

    #chack the month and the day number
    if month in ["january", "march", "may", "july", "august", "october", "december"]:
        if day <= 31:
            return True
    elif month in ["november", "april", "june", "september"]:
        if day <= 30:
            return True
    elif month == "february":
        if day <= 29:
            return True #non considera anni bisestili
    else:
        return False
    
    #chack that year is positive
    if year < 1:
        return False
    
    return True

"""Controls that the image extension is one valid"""
def check_image_extention(image_name):
    extension = image_name.split(".")[-1].strip()
    return extension in ["jpg", "jpeg", "png", "gif", "svg"]

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
            date = extract_field_value(post_path, self.separator, "date")
            self.assertTrue(check_date(date), f"date of post {post} is non valid")
            #check autor_image format
            author_image = extract_field_value(post_path, self.separator, "author_image")
            self.assertTrue(check_image_extention(author_image), f"author_image of post {post} is non valid")
            #chack image format
            image = extract_field_value(post_path, self.separator, "image")
            self.assertTrue(check_image_extention(image), f"image of post {post} is non valid")
