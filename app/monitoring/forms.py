from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class AckExpireForm(FlaskForm):
    host_name = StringField(label='Host name:*', validators=[DataRequired()])
    service = StringField(label='Service name:*', validators=[DataRequired()])
    comment = StringField(label='Comment:*', validators=[DataRequired()])
    submit = SubmitField('Submit')