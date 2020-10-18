from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class DictForm(FlaskForm):
    dict_id = StringField('ID słownika')
    dict_nm = StringField('Nazwa slownika', validators=[DataRequired(), Length(min=1, max=100)])
    dict_desc = StringField('Opis slownika', validators=[DataRequired(), Length(min=1, max=500)])
    dict_tp = StringField('Typ slownika')
    dict_crt_dt = StringField('Data utworzenia')
    submit = SubmitField('Wykonaj')


class ConvsDictForm(FlaskForm):
    dict_val_id = StringField('ID wpisu')
    dict_id = StringField('ID słownika')
    dict_val_val = StringField('Wartość', validators=[DataRequired(), Length(min=1, max=200)])
    rltd_dict_nm_1 = SelectField('Słownik powiązany 1', choices=[])
    rltd_dict_val_1 = SelectField('Wartosc powiązana 1', choices=[])
    rltd_dict_nm_2 = SelectField('Słownik powiązany 2', choices=[])
    rltd_dict_val_2 = SelectField('Wartosc powiązana 2', choices=[])
    rltd_dict_nm_3 = SelectField('Słownik powiązany 3', choices=[])
    rltd_dict_val_3 = SelectField('Wartosc powiązana 3', choices=[])
    dict_val_crt_dt = StringField('Data utworzenia')
    submit = SubmitField('Wykonaj')


class SmplDictForm(FlaskForm):
    dict_val_id = StringField('ID wpisu')
    dict_id = StringField('ID słownika')
    dict_val_val = StringField('Wartość', validators=[DataRequired(), Length(min=1, max=200)])
    dict_val_crt_dt = StringField('Data utworzenia')
    submit = SubmitField('Wykonaj')
