from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField
from wtforms.validators import URL,NumberRange,DataRequired

class CricketForm(FlaskForm):

    url = StringField('Cricbuzz Url : ',validators=[URL(),DataRequired()])
    innings = IntegerField('Innings',validators=[NumberRange(min=1,max=4),DataRequired()],default=2)
    submit = SubmitField('Find Scores!')