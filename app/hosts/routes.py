from flask import render_template, url_for, flash, redirect, current_app
from app.hosts.forms import (
    AddHostForm, DeleteHostForm, ShowHostForm, UpdateHostForm,
    HostDowntimeForm, ShowOneDowntimeForm
)
from app.clients.checkmk_client import CheckmkClient
from flask_login import login_required
from . import hosts_bp


def get_checkmk_client():
    return CheckmkClient(  
        base_url=current_app.config["CHECKMK_BASE_URL"],
        username=current_app.config["CHECKMK_USERNAME"],
        password=current_app.config["CHECKMK_PASSWORD"],
        verify_ssl=current_app.config["CHECKMK_VERIFY_SSL"],
    )




@hosts_bp.route("/addhost", methods=["GET", "POST"])
@login_required
def addhost_page():
    form = AddHostForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        client.add_host(form.host_name.data, form.ip_address.data, form.folder_name.data)
        flash(f"Host: {form.host_name.data} added successfully", category="success")
        return redirect(url_for("hosts.addhost_page"))
    return render_template("forms/add_host.html", form=form)  


@hosts_bp.route("/deletehost", methods=["GET", "POST"])
@login_required
def deletehost_page():
    form = DeleteHostForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        client.delete_host(form.host_name.data)
        flash(f"Host: {form.host_name.data} deleted successfully", category="success")
        return redirect(url_for("hosts.deletehost_page"))
    return render_template("forms/delete_host.html", form=form) 


@hosts_bp.route("/showhost", methods=["GET", "POST"])
@login_required
def showhost_page():
    form = ShowHostForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        host_data = client.show_host(form.host_name.data)
        details = [
            f"Host: {host_data.get('title', '-')}",
            f"Alias: {host_data.get('extensions', {}).get('attributes', {}).get('alias', '-')}",
            f"Folder: {host_data.get('extensions', {}).get('folder', '-')}",
            f"IP-Address: {host_data.get('extensions', {}).get('attributes', {}).get('ipaddress', '-')}",
        ]
        flash("<br>".join(details), category="success")
        return redirect(url_for("hosts.showhost_page"))
    return render_template("forms/show_host.html", form=form)  


@hosts_bp.route("/updatehost", methods=["GET", "POST"])
@login_required
def updatehost_page():
    form = UpdateHostForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        client.update_host(form.host_name.data, form.ip_address.data, form.alias.data)
        flash(f"Host: {form.host_name.data} updated successfully", category="success")
        return redirect(url_for("hosts.updatehost_page"))
    return render_template("forms/update_host.html", form=form) 


@hosts_bp.route("/hostdowntime", methods=["GET", "POST"])
@login_required
def create_host_downtime_page():
    form = HostDowntimeForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        client.create_downtime_host(
            form.host_name.data,
            form.downtime_start.data,
            form.downtime_end.data,
            form.comment.data
        )
        flash(f"Downtime for Host - {form.host_name.data} successfully created", category="success")
        return redirect(url_for("hosts.create_host_downtime_page"))  
    return render_template("forms/create_downtime_host.html", form=form)  


@hosts_bp.route("/showonedowntime", methods=["GET", "POST"])
@login_required
def show_one_downtime_page():
    form = ShowOneDowntimeForm()
    if form.validate_on_submit():
        client = get_checkmk_client()
        downtime_data = client.get_one_downtime(form.host_name.data)
        for downtime in downtime_data:
            details = [
                f"Host: {downtime.get('extensions', {}).get('host_name', '-')}",
                f"Start time: {downtime.get('extensions', {}).get('start_time', '-')}",
                f"End time: {downtime.get('extensions', {}).get('end_time', '-')}",
                f"Comment: {downtime.get('extensions', {}).get('comment', '-')}",
                f"Downtime ID: {downtime.get('id', '-')}",
            ]
            flash("\n".join(details), category="success")
        return redirect(url_for("hosts.show_one_downtime_page"))
    return render_template("forms/show_one_downtime.html", form=form) 