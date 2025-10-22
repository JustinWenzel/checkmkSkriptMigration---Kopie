from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class AddHostForm(FlaskForm):
    host_name = StringField(label="Host name:*", validators=[DataRequired()])
    ip_address = StringField(
        label="Host IP address:*",
        validators=[IPAddress(ipv4=True, ipv6=True, message="Please enter a valid IPv4 or IPv6 Address"), DataRequired()])
    folder_name = StringField(label="Folder name/path:")
    submit = SubmitField(label="Create host")


class DeleteHostForm(FlaskForm):
    host_name = StringField(label="Host name:*", validators=[DataRequired()])
    submit = SubmitField(label="Delete host")


class ShowHostForm(FlaskForm):
    host_name = StringField(label="Host name:*", validators=[DataRequired()])
    submit = SubmitField(label="Show host")


class UpdateHostForm(FlaskForm):
    host_name = StringField(label="Host to update:*", validators=[DataRequired()])
    ip_address = StringField(
        label="New IP address:*",
        validators=[IPAddress(ipv4=True, ipv6=True, message="Please enter a valid IPv4 or IPv6 Address")])
    alias = StringField(label="New alias:*", validators=[DataRequired()])
    submit = SubmitField(label="Update host")


class HostDowntimeForm(FlaskForm):
    host_name = StringField(label="Host for downtime:*", validators=[DataRequired()])
    downtime_start = StringField('Start time:*', validators=[DataRequired()])
    downtime_end = StringField('End time:*', validators=[DataRequired()])
    comment = StringField(label="Comment for downtime:*", validators=[DataRequired()])
    submit = SubmitField(label="Create downtime")


class ShowOneDowntimeForm(FlaskForm):
    host_name = StringField(label="Host name:*", validators=[DataRequired()])
    submit = SubmitField(label="Show downtime")