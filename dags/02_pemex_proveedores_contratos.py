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
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='02_pemex_proveedores_contratos', default_args=args,
    schedule_interval='@monthly')


def extraer_proveedores():
    """
    Obtiene archivo en excel del portal Sistema de información pública de
    proveedores y contratistas y lo guarda en el sistema de archivos
    """
    # TODO Guardar en S3
    logging.info("extraer_proveedores")
    pass


def extraer_contratos():
    """
    Obtiene archivo en excel del portal Sistema de información pública de
    proveedores y contratistas y lo guarda en el sistema de archivos
    """
    # TODO Guardar en S3
    pass


def cargar_proveedores():
    """
    Carga en la base de datos los archivos descargados del portal de
    Sistema de información pública de proveedores y contratistas
    """
    pass


def cargar_contratos():
    """
    Carga en la base de datos los archivos descargados del portal de
    Sistema de información pública de proveedores y contratistas
    """
    pass


e_proveedores = PythonOperator(
    task_id='extraer_proveedores',
    provide_context=True,
    python_callable=extraer_proveedores,
    dag=dag)

c_proveedores = PythonOperator(
    task_id='cargar_proveedores',
    provide_context=True,
    python_callable=cargar_proveedores,
    dag=dag)

e_contratos = PythonOperator(
    task_id='extraer_contratos',
    provide_context=True,
    python_callable=extraer_contratos,
    dag=dag)

c_contratos = PythonOperator(
    task_id='cargar_contratos',
    provide_context=True,
    python_callable=cargar_contratos,
    dag=dag)

e_proveedores >> c_proveedores

e_contratos >> c_contratos
