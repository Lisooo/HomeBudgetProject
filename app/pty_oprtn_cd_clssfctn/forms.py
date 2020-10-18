from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class PtyOprtnCdClssfctnForm(FlaskForm):
    trnsct_ctg = SelectField('Kategoria transakcji', choices=[])
    trnsct_sctg = SelectField('Podkategoria transakcji', choices=[])
    submit = SubmitField('Wykonaj')
