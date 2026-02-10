# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectExpediente(models.Model):
    _inherit = 'project.project'

    # Campos específicos para Expedientes
    es_expediente = fields.Boolean(
        string='Es Expediente',
        default=True,
        help='Indica si este proyecto es un Expediente'
    )
    
    expediente_numero = fields.Char(
        string='Número de Expediente',
        help='Número único del expediente',
        index=True,
    )
    
    expediente_fecha_apertura = fields.Date(
        string='Fecha de Apertura',
        default=fields.Date.today,
    )
    
    expediente_fecha_cierre = fields.Date(
        string='Fecha de Cierre',
    )
    
    # Relaciones entre Expedientes
    expediente_padre_id = fields.Many2one(
        'project.project',
        string='Expediente Padre',
        domain="[('es_expediente', '=', True), ('id', '!=', id)]",
        help='Expediente padre al que pertenece este expediente',
        ondelete='restrict',
    )
    
    expediente_hijos_ids = fields.One2many(
        'project.project',
        'expediente_padre_id',
        string='Expedientes Hijos',
        domain=[('es_expediente', '=', True)],
        help='Expedientes hijos relacionados',
    )
    
    expediente_relacionados_ids = fields.Many2many(
        'project.project',
        'project_expediente_relacion',
        'expediente_id',
        'expediente_relacionado_id',
        string='Expedientes Relacionados',
        domain="[('es_expediente', '=', True), ('id', '!=', id)]",
        help='Expedientes relacionados (sin relación padre/hijo)',
    )
    
    expediente_nivel = fields.Integer(
        string='Nivel',
        compute='_compute_expediente_nivel',
        store=True,
        help='Nivel de jerarquía del expediente (0 = raíz)',
    )
    
    expediente_ruta_completa = fields.Char(
        string='Ruta Completa',
        compute='_compute_expediente_ruta',
        help='Ruta completa del expediente en la jerarquía',
    )
    
    expediente_cantidad_hijos = fields.Integer(
        string='Cantidad de Hijos',
        compute='_compute_expediente_cantidad_hijos',
        help='Cantidad total de expedientes hijos',
    )
    
    expediente_estado = fields.Selection(
        [
            ('borrador', 'Borrador'),
            ('en_tramite', 'En Trámite'),
            ('suspendido', 'Suspendido'),
            ('cerrado', 'Cerrado'),
            ('archivado', 'Archivado'),
        ],
        string='Estado del Expediente',
        default='borrador',
        help='Estado actual del expediente',
    )

    @api.depends('expediente_padre_id', 'expediente_padre_id.expediente_nivel')
    def _compute_expediente_nivel(self):
        """Calcula el nivel jerárquico del expediente"""
        for record in self:
            if record.expediente_padre_id:
                record.expediente_nivel = record.expediente_padre_id.expediente_nivel + 1
            else:
                record.expediente_nivel = 0

    @api.depends('expediente_padre_id', 'name', 'expediente_numero')
    def _compute_expediente_ruta(self):
        """Calcula la ruta completa del expediente en la jerarquía"""
        for record in self:
            if record.expediente_padre_id:
                padre_ruta = record.expediente_padre_id.expediente_ruta_completa or ''
                numero = record.expediente_numero or record.name or ''
                record.expediente_ruta_completa = f"{padre_ruta} / {numero}" if padre_ruta else numero
            else:
                record.expediente_ruta_completa = record.expediente_numero or record.name or ''

    @api.depends('expediente_hijos_ids')
    def _compute_expediente_cantidad_hijos(self):
        """Calcula la cantidad total de expedientes hijos (recursivo)"""
        for record in self:
            def contar_hijos(expediente):
                count = len(expediente.expediente_hijos_ids)
                for hijo in expediente.expediente_hijos_ids:
                    count += contar_hijos(hijo)
                return count
            record.expediente_cantidad_hijos = contar_hijos(record)

    @api.constrains('expediente_padre_id')
    def _check_expediente_padre(self):
        """Evita referencias circulares en la jerarquía"""
        for record in self:
            if record.expediente_padre_id:
                # Verificar que no se cree un ciclo
                padre = record.expediente_padre_id
                while padre:
                    if padre == record:
                        raise ValidationError(
                            _('No se puede crear una referencia circular. '
                              'El expediente no puede ser padre de sí mismo o de sus ancestros.')
                        )
                    padre = padre.expediente_padre_id

    @api.constrains('expediente_numero')
    def _check_expediente_numero_unico(self):
        """Valida que el número de expediente sea único"""
        for record in self:
            if record.expediente_numero and record.es_expediente:
                duplicados = self.search([
                    ('expediente_numero', '=', record.expediente_numero),
                    ('id', '!=', record.id),
                    ('es_expediente', '=', True),
                ])
                if duplicados:
                    raise ValidationError(
                        _('El número de expediente %s ya existe. Debe ser único.') % record.expediente_numero
                    )

    def action_ver_expedientes_hijos(self):
        """Acción para ver todos los expedientes hijos"""
        self.ensure_one()
        return {
            'name': _('Expedientes Hijos de %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'tree,form',
            'domain': [('expediente_padre_id', '=', self.id), ('es_expediente', '=', True)],
            'context': {
                'default_expediente_padre_id': self.id,
                'default_es_expediente': True,
                'search_default_expediente_padre_id': self.id,
            },
        }

    def action_ver_expediente_padre(self):
        """Acción para ver el expediente padre"""
        self.ensure_one()
        if not self.expediente_padre_id:
            return False
        return {
            'name': _('Expediente Padre'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'form',
            'res_id': self.expediente_padre_id.id,
            'target': 'current',
        }

    def action_ver_arbol_expedientes(self):
        """Acción para ver el árbol completo de expedientes"""
        self.ensure_one()
        # Encontrar la raíz del árbol
        raiz = self
        while raiz.expediente_padre_id:
            raiz = raiz.expediente_padre_id
        
        return {
            'name': _('Árbol de Expedientes - %s') % raiz.name,
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'tree,form',
            'domain': [('es_expediente', '=', True)],
            'context': {
                'default_es_expediente': True,
                'search_default_expediente_padre_id': False,
            },
        }
