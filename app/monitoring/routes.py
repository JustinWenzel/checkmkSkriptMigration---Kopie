from flask import render_template, request, url_for, flash, redirect, current_app
from app.clients.checkmk_client import CheckmkClient
from app.monitoring.forms import AckExpireForm
from flask_login import login_required
from . import monitor_bp


def get_checkmk_client():
    return CheckmkClient(  
        base_url=current_app.config["CHECKMK_BASE_URL"],
        username=current_app.config["CHECKMK_USERNAME"],
        password=current_app.config["CHECKMK_PASSWORD"],
        verify_ssl=current_app.config["CHECKMK_VERIFY_SSL"],
    )


@monitor_bp.route("/currentproblems", methods=["GET"])
@login_required
def current_problems_page():
    client = get_checkmk_client()
    service_data = client.get_current_problems()
    
    services = []
    warning_count = 0
    critical_count = 0
    
    if service_data and 'value' in service_data:
        services = service_data['value']
        
        for service in services:
            state = service.get('extensions', {}).get('state')
            if state == 1:
                warning_count += 1
            elif state == 2:
                critical_count += 1
    
    return render_template(
        "dashboards/current_problems.html",  
        services=services,
        warning_count=warning_count,
        critical_count=critical_count,
        total_count=len(services)
    )


@monitor_bp.route("/currentproblemsnetops", methods=["GET"])
@login_required
def current_problems_is_netops_page():
    client = get_checkmk_client()
    service_data = client.get_current_problems_is_netops()
    
    services = []
    warning_count = 0
    critical_count = 0
    
    if service_data and 'value' in service_data:
        services = service_data['value']
        
        for service in services:
            state = service.get('extensions', {}).get('state')
            if state == 1:
                warning_count += 1
            elif state == 2:
                critical_count += 1
    
    return render_template(
        "dashboards/current_problems_is_netops.html",  
        services=services,
        warning_count=warning_count,
        critical_count=critical_count,
        total_count=len(services)
    )


@monitor_bp.route("/currentwarnings", methods=["GET"])
@login_required
def current_warnings_page():
    client = get_checkmk_client()
    service_data = client.get_current_problems()
    
    services = []
    warning_count = 0
    critical_count = 0
    
    if service_data and 'value' in service_data:
        services = service_data['value']
        
        for service in services:
            state = service.get('extensions', {}).get('state')
            if state == 1:
                warning_count += 1
            elif state == 2:
                critical_count += 1
    
    return render_template(
        "dashboards/current_warnings.html",  
        services=services,
        warning_count=warning_count,
        critical_count=critical_count,
        total_count=len(services)
    )


@monitor_bp.route("/currentcriticals", methods=["GET"])
@login_required
def current_criticals_page():
    client = get_checkmk_client()
    service_data = client.get_current_problems()
    
    services = []
    warning_count = 0
    critical_count = 0
    
    if service_data and 'value' in service_data:
        services = service_data['value']
        
        for service in services:
            state = service.get('extensions', {}).get('state')
            if state == 1:
                warning_count += 1
            elif state == 2:
                critical_count += 1
    
    return render_template(
        "dashboards/current_criticals.html",  
        services=services,
        warning_count=warning_count,
        critical_count=critical_count,
        total_count=len(services)
    )


@monitor_bp.route('/ackexpire/<host_name>/<service>/<state>', methods=["GET", "POST"])
@login_required
def ack_expire_page(host_name, service, state):
    form = AckExpireForm()
    
    if not form.is_submitted():
        form.host_name.data = host_name
        form.service.data = service
    
    if form.validate_on_submit():
        
        expire_date = request.form.get('expire_date')
        
        
        client = get_checkmk_client()  
        client.acknowledge_problem_service(
            form.host_name.data,
            form.service.data,
            expire_date,
            form.comment.data
        )
        
        
        if state == "1":
            return redirect(url_for('monitor.current_warnings_page'))
        elif state == "2": 
            return redirect(url_for('monitor.current_criticals_page'))
        return redirect(url_for('monitor.current_problems_page'))
         
    return render_template("forms/acknowledge.html", form=form)


@monitor_bp.route("/showalldowntimes", methods=["GET", "POST"])
@login_required
def show_all_downtimes_page():
    client = get_checkmk_client()
    downtime_data = client.get_all_downtimes()

    all_downtimes = []
    if downtime_data and 'value' in downtime_data:
        all_downtimes = downtime_data['value']
        
    return render_template("dashboards/show_all_downtimes.html", all_downtimes=all_downtimes, total_downtimes=len(all_downtimes), client=client )  