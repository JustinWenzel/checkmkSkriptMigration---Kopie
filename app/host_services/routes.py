from flask import render_template, url_for, flash, redirect, current_app
from app.host_services.forms import ServiceDowntimeForm
from app.clients.checkmk_client import CheckmkClient 
from flask_login import login_required
from . import host_services_bp


def get_checkmk_client():
    return CheckmkClient(  
        base_url=current_app.config["CHECKMK_BASE_URL"],
        username=current_app.config["CHECKMK_USERNAME"],
        password=current_app.config["CHECKMK_PASSWORD"],
        verify_ssl=current_app.config["CHECKMK_VERIFY_SSL"],
    )



    
@host_services_bp.route("/servicedowntime", methods=["GET", "POST"])
@login_required
def create_service_downtime_page():
    form = ServiceDowntimeForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        client.create_downtime_service(
            form.host_name.data,
            form.service_name.data,
            form.downtime_start.data,
            form.downtime_end.data,
            form.comment.data
        )
        flash(f"Downtime for Service - {form.service_name.data} from Host - {form.host_name.data} successfully created", category="success")
        return redirect(url_for("host_services.create_service_downtime_page"))  
    return render_template("forms/create_downtime_service.html", form=form)  


