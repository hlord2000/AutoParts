import requests
import os
import json

class AutoParts:
    def __init__(self, book_id=None, cookie=None): 
        self.find_chapters_link = "https://learning.oreilly.com/api/v2/epubs/urn:orm:book:%s/files/"
        self.book_id = book_id
        self.cookies = None 
        self.headers = None 
      
        self.directories = ["./books", "./chapters"]
        for directory in self.directories:
            try:
                os.mkdir(directory)
            except FileExistsError:
                pass

    def get_chapter_dict(self):
        response = requests.get(self.find_chapters_link % self.book_id, cookies=self.cookies)
        with open("./books/%s.json" % self.book_id, "w") as chapter_dir_file:
            chapter_dir_file.write(response.text) 

    def collect_html_files(self):
        with open("./books/%s.json" % self.book_id, "r") as chapter_dir_file:
            jsonify = json.loads(chapter_dir_file.read())             
            for item in jsonify["results"]:
                chapter_html = item["url"]
                response = requests.get(chapter_html, cookies=self.cookies, headers=self.headers)
                with open("./chapters/%s" % item["filename"], "w") as chapter:
                    chapter.write(response.text) 
                    
if __name__ == "__main__":
    pog = AutoParts("0596006101" ,'507284bf-5790-432d-8a26-de901b964800')
    pog.get_chapter_dict()
    pog.collect_html_files()
