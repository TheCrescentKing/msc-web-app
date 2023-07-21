import os
from jinja2 import Environment, FileSystemLoader

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader = FileSystemLoader(template_dir),autoescape = True)

def makeGranuleHtml(granuleData):
    template = jinja_env.get_template("granulePopup.html")
    variables = {"granuleName": granuleData['asset_name'], 
                 "granuleUrl": granuleData['asset_url'], 
                 "granuleClouds": granuleData['cloud_cover']}
    return template.render(variables)