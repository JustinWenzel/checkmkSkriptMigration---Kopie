from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ServiceDowntimeForm(FlaskForm):
    host_name = StringField(label="Host for downtime:*", validators=[DataRequired()])
    service_name = StringField(label="Service for downtime:*", validators=[DataRequired()])
    downtime_start = StringField('Start time:*', validators=[DataRequired()])
    downtime_end = StringField('End time:*', validators=[DataRequired()])
    comment = StringField(label="Comment for downtime:*", validators=[DataRequired()])
    submit = SubmitField(label="Create downtime")