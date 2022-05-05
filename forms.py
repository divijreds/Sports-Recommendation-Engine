from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

class MatchConditionsForm(FlaskForm):
    pitch = SelectField('Pitch Type', choices=[('Green', 'Green Top'), ('Dead', 'Dead (Flat Track)'), ('Dusty', 'Dusty (Turner)')])
    algorithm = SelectField('Method of Recommendation', choices=[('m1', 'Normal Recommendation'), ('m2', 'K-Means Recommendation')])
    #, validators=[DataRequired()], validate_choice=True
    submit = SubmitField('Submit')