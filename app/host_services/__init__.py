from flask import Blueprint

host_services_bp = Blueprint(
    "host_services",             
    __name__,           
    template_folder="templates"
    
)