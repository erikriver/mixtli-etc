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
from airflow.operators.dummy_operator import DummyOperator

from utils.slugify import slugify

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

categorias = [
    {'actividad_id' : 11,
     'actividad' : "Agricultura, ganaderia, aprovechamiento forestal, pesca y caza"},
    {'actividad_id' : 21,
     'actividad' : "Mineria"},
    {'actividad_id' : 22,
     'actividad' : "Electricidad, agua y suministro de gas por ductos al consumidor final"},
    {'actividad_id' : 23,
     'actividad' : "Construccion"},
    {'actividad_id': 31,
     'actividad' : "Industrias manufactureras"},
    {'actividad_id' : 43,
     'actividad' : "Comercio al por mayor"},
    {'actividad_id' : 46,
     'actividad' : "Comercio al por menor"},
    {'actividad_id' : 48,
     'actividad' : "Transporte, correos y almacenamiento"},
    {'actividad_id' : 51,
     'actividad' : "Informacion en medios masivos"},
    {'actividad_id' : 52,
     'actividad' : "Servicios financieros y de seguros"},
    {'actividad_id' : 53,
     'actividad' : "Servicios inmobiliarios y de alquiler de bienes muebles e intangibles"},
    {'actividad_id' : 54,
     'actividad' : "Servicios profesionales, cientificos y tecnicos"},
    {'actividad_id' : 55,
     'actividad' : "Direccion de corporativos y empresas"},
    {'actividad_id' : 56,
     'actividad' : "Apoyo a los negocios y manejo de desechos y serv. de remediacion"},
    {'actividad_id' : 61,
     'actividad' : "Servicios educativos"},
    {'actividad_id' : 62,
     'actividad' : "Servicios de salud y de asistencia social"},
    {'actividad_id' : 71,
     'actividad' : "Serv. de esparcimiento culturales y deportivos, y otros serv. recreativos"},
    {'actividad_id' : 72,
     'actividad' : "Servicios de alojamiento temporal y de preparacion de alimentos y bebidas"},
    {'actividad_id' : 81,
     'actividad' : "Otros servicios excepto actividades del gobierno"},
    {'actividad_id' : 93,
     'actividad' : "Actividades del gobierno y organismos internacionales extraterritoriales"},
]

dag = DAG(
    dag_id='03_siem_informacion_empresarial', default_args=args,
    schedule_interval='@monthly')


start_node = DummyOperator(task_id='inicio',
                        dag=dag)


end_node = DummyOperator(task_id='fin',
                        dag=dag)


def tareas_categorias(categorias):
    previous_task = None
    for i in categorias:

        task = DummyOperator(task_id=slugify(i['actividad'])[:20],
                             dag=dag)

        if previous_task:
            previous_task.set_downstream(task)
        else:
            start_node.set_downstream(task)

        previous_task = task

    task.set_downstream(end_node)

tareas_categorias(categorias)
