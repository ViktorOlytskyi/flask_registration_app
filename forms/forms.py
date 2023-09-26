from flask_wtf import FlaskForm, file
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Product')
    image = FileField('Image')