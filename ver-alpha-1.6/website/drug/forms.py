from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField ,SelectField
from wtforms.validators import DataRequired

class DrugSearchForm(FlaskForm):
    search = StringField('Search',validators=[DataRequired()])
    searchby = SelectField('Search By',choices=[('1','Drug'),('2','Condition'),('3','Brand List')])
    submit = SubmitField('Search')