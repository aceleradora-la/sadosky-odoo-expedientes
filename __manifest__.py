# -*- coding: utf-8 -*-
{
    'name': 'Expedientes como Proyectos',
    'version': '18.0.1.0',
    'category': 'Project',
    'summary': 'Extiende el módulo de proyectos para gestionar Expedientes como Proyectos con relaciones entre sí',
    'description': """
        Módulo de Expedientes como Proyectos
        =====================================
        
        Este módulo extiende el módulo de proyectos de Odoo para:
        - Convertir cada Expediente en un Proyecto
        - Permitir relaciones entre Expedientes (padre/hijo)
        - Visualizar la jerarquía de Expedientes
        - Gestionar dependencias entre Expedientes
    """,
    'author': 'Sadosky',
    'website': 'https://www.sadosky.org.ar',
    'depends': [
        'project',
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_expediente_views.xml',
        'views/project_expediente_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
