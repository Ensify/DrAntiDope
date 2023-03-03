from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import email_validator


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    topic = StringField('Topic',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')