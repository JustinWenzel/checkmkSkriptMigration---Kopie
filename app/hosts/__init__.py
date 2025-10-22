from flask import Blueprint

hosts_bp = Blueprint(
    "hosts",             
    __name__,           
    template_folder="templates"
    
)