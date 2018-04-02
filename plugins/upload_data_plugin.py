# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Erik Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

import airflow
from airflow import configuration
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.db import provide_session
from airflow import models

from flask import flash, request, Blueprint, redirect
from flask_admin import BaseView, expose
from flask_wtf import FlaskForm
from flask_admin.babel import lazy_gettext as _
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    BooleanField, IntegerField, SelectField, StringField, TextField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange, Optional


class FileDataForm(FlaskForm):
    # pylint: disable=E0211

    @provide_session
    def all_db_items(session=None):
        dbs = session.query(models.Connection).order_by(
            models.Connection.conn_id).all()
        session.expunge_all()
        db_choices = list(
            ((db.conn_id, db.conn_id) for db in dbs if db.get_hook()))
        return db_choices


    name = StringField(
        _('Table Name'),
        description=_('Name of table to be created from csv data.'),
        validators=[DataRequired()])
    csv_file = FileField(
        _('CSV File'),
        description=_('Select a CSV file to be uploaded to a database.'),
        validators=[
            FileRequired(), FileAllowed(['csv'], _('CSV Files Only!'))])
    con = SelectField(_('Connection'), choices=all_db_items())
    sep = StringField(
        _('Delimiter'),
        description=_('Delimiter used by CSV file.'),
        validators=[DataRequired()])
    if_exists = SelectField(
        _('Table Exists'),
        description=_(
            'If table exists do one of the following: '
            'Fail (do nothing), Replace (drop and recreate table) '
            'or Append (insert data).'),
        choices=[
            ('fail', _('Fail')), ('replace', _('Replace')),
            ('append', _('Append'))],
        validators=[DataRequired()])
    schema = StringField(
        _('Schema'),
        description=_('Specify a schema (if database flavour supports this).'),
        validators=[Optional()],
        filters=[lambda x: x or None])
    header = IntegerField(
        _('Header Row'),
        description=_(
            'Row containing the headers to use as '
            'column names (0 is first line of data). '
            'Leave empty if there is no header row.'),
        validators=[Optional()],
        filters=[lambda x: x or None])
    index_col = IntegerField(
        _('Index Column'),
        description=_(
            'Column to use as the row labels of the '
            'dataframe. Leave empty if no index column.'),
        validators=[Optional(), NumberRange(0, 1E+20)],
        filters=[lambda x: x or None])
    # mangle_dupe_cols = BooleanField(
    #     _('Mangle Duplicate Columns'),
    #     description=_('Specify duplicate columns as "X.0, X.1".'))
    # skipinitialspace = BooleanField(
    #     _('Skip Initial Space'),
    #     description=_('Skip spaces after delimiter.'))
    skiprows = IntegerField(
        _('Skip Rows'),
        description=_('Number of rows to skip at start of file.'),
        validators=[Optional(), NumberRange(0, 1E+20)],
        filters=[lambda x: x or None])
    # nrows = IntegerField(
    #     _('Rows to Read'),
    #     description=_('Number of rows of file to read.'),
    #     validators=[Optional(), NumberRange(0, 1E+20)],
    #     filters=[lambda x: x or None])
    skip_blank_lines = BooleanField(
        _('Skip Blank Lines'),
        description=_(
            'Skip blank lines rather than interpreting them '
            'as NaN values.'))
    # parse_dates = BooleanField(
    #     _('Parse Dates'),
    #     description=_('Parse date values.'))
    # infer_datetime_format = BooleanField(
    #     _('Infer Datetime Format'),
    #     description=_(
    #         'Use Pandas to interpret the datetime format '
    #         'automatically.'))
    # decimal = StringField(
    #     _('Decimal Character'),
    #     description=_('Character to interpret as decimal point.'),
    #     validators=[Optional()],
    #     filters=[lambda x: x or '.'])
    index = BooleanField(
        _('Dataframe Index'),
        description=_('Write dataframe index as a column.'))
    index_label = StringField(
        _('Column Label(s)'),
        description=_(
            'Column label for index column(s). If None is given '
            'and Dataframe Index is True, Index Names are used.'),
        validators=[Optional()],
        filters=[lambda x: x or None])



# class UploadData(BaseView):
#     form = FileDataForm
#     form_title = _('CSV to Database configuration')
#     add_columns = ['database', 'schema', 'table_name']

#     def form_get(self, form):
#         form.sep.data = ','
#         form.header.data = 0
#         form.mangle_dupe_cols.data = True
#         form.skipinitialspace.data = False
#         form.skip_blank_lines.data = True
#         form.parse_dates.data = True
#         form.infer_datetime_format.data = True
#         form.decimal.data = '.'
#         form.if_exists.data = 'append'

#     def form_post(self, form):
#         csv_file = form.csv_file.data
#         form.csv_file.data.filename = secure_filename(form.csv_file.data.filename)
#         csv_filename = form.csv_file.data.filename
#         try:
#             csv_file.save(os.path.join(config['UPLOAD_FOLDER'], csv_filename))
#             table = SqlaTable(table_name=form.name.data)
#             table.database = form.data.get('con')
#             table.database_id = table.database.id
#             table.database.db_engine_spec.create_table_from_csv(form, table)
#         except Exception as e:
#             try:
#                 os.remove(os.path.join(config['UPLOAD_FOLDER'], csv_filename))
#             except OSError:
#                 pass
#             message = 'Table name {} already exists. Please pick another'.format(
#                 form.name.data) if isinstance(e, IntegrityError) else text_type(e)
#             flash(
#                 message,
#                 'danger')
#             return redirect('/csvtodatabaseview/form')

#         os.remove(os.path.join(config['UPLOAD_FOLDER'], csv_filename))
#         # Go back to welcome page / splash screen
#         db_name = table.database.database_name
#         message = _('CSV file "{0}" uploaded to table "{1}" in '
#                     'database "{2}"'.format(csv_filename,
#                                             form.name.data,
#                                             db_name))
#         flash(message, 'info')
#         return redirect('/tablemodelview/list/')




class UploadData(BaseView):

    @expose('/', methods=['POST', 'GET'])
    def index(self):
        ""
        form = FileDataForm(request.form)

        text = dir(form)
        return self.render("upload_data_plugin/index.html", form=form, text=text)

view = UploadData(category="Admin", name="Upload Data")

upload_data_bp = Blueprint(
    "upload_data",
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/'
)


class UploadDataPlugin(AirflowPlugin):
    name = "upload_data_plugin"
    operators = []
    flask_blueprints = [upload_data_bp]
    hooks = []
    executors = []
    admin_views = [view]
    menu_links = []
