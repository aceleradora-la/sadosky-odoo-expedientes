# Módulo de Expedientes como Proyectos para Odoo

## Descripción

Este módulo extiende el módulo de proyectos de Odoo para gestionar **Expedientes** como **Proyectos** con capacidades avanzadas de relación jerárquica y lateral.

## Características Principales

### 1. Expedientes como Proyectos
- Cada Expediente es un Proyecto completo con todas sus funcionalidades
- Campo `es_expediente` para identificar expedientes
- Número de expediente único y rastreable

### 2. Relaciones Jerárquicas (Padre-Hijo)
- **Expediente Padre**: Cada expediente puede tener un expediente padre
- **Expedientes Hijos**: Visualización y gestión de expedientes hijos
- **Niveles**: Cálculo automático del nivel jerárquico
- **Ruta Completa**: Visualización de la ruta completa en la jerarquía
- **Validación**: Prevención de referencias circulares

### 3. Relaciones Laterales
- **Expedientes Relacionados**: Relaciones entre expedientes sin jerarquía
- Útil para vincular expedientes relacionados sin dependencia padre-hijo

### 4. Estados del Expediente
- **Borrador**: Expediente en creación
- **En Trámite**: Expediente activo
- **Suspendido**: Expediente pausado temporalmente
- **Cerrado**: Expediente finalizado
- **Archivado**: Expediente archivado

### 5. Vistas y Navegación
- **Vista de Árbol**: Visualización jerárquica de expedientes
- **Vista Kanban**: Por estado del expediente
- **Vista de Formulario**: Con pestañas para relaciones
- **Acciones Rápidas**: Ver padre, ver hijos, ver árbol completo

## Instalación

1. Copiar el módulo en la carpeta `addons` de Odoo
2. Actualizar la lista de aplicaciones en Odoo
3. Instalar el módulo "Expedientes como Proyectos"

## Dependencias

- `project`: Módulo de proyectos de Odoo
- `base`: Módulo base de Odoo

## Uso

### Crear un Expediente

1. Ir a **Expedientes > Todos los Expedientes**
2. Click en **Crear**
3. Completar:
   - **Número de Expediente**: Identificador único (ej: EXP-2024-001)
   - **Nombre**: Nombre descriptivo del expediente
   - **Expediente Padre**: (Opcional) Si pertenece a otro expediente
   - **Fecha de Apertura**: Fecha de inicio
   - **Estado**: Estado inicial del expediente

### Relacionar Expedientes

#### Relación Padre-Hijo
- Al crear un expediente, seleccionar un **Expediente Padre**
- Los expedientes hijos se mostrarán automáticamente en la pestaña "Expedientes Relacionados"
- La jerarquía se calcula automáticamente

#### Relaciones Laterales
- En la pestaña "Expedientes Relacionados" del formulario
- Agregar expedientes en el campo "Expedientes Relacionados"
- Útil para vincular expedientes sin jerarquía

### Navegar la Jerarquía

- **Ver Expediente Padre**: Botón en el header del formulario
- **Ver Expedientes Hijos**: Botón que muestra todos los hijos
- **Ver Árbol Completo**: Muestra toda la jerarquía desde la raíz

## Campos del Modelo

### Campos Principales
- `es_expediente`: Boolean que indica si es un expediente
- `expediente_numero`: Número único del expediente
- `expediente_padre_id`: Referencia al expediente padre
- `expediente_hijos_ids`: Lista de expedientes hijos
- `expediente_relacionados_ids`: Expedientes relacionados (sin jerarquía)

### Campos Calculados
- `expediente_nivel`: Nivel en la jerarquía (0 = raíz)
- `expediente_ruta_completa`: Ruta completa en la jerarquía
- `expediente_cantidad_hijos`: Cantidad total de hijos (recursivo)

### Campos de Estado
- `expediente_estado`: Estado actual del expediente
- `expediente_fecha_apertura`: Fecha de apertura
- `expediente_fecha_cierre`: Fecha de cierre

## Validaciones

1. **Número Único**: El número de expediente debe ser único
2. **Sin Ciclos**: No se permiten referencias circulares en la jerarquía
3. **Dominio**: Los expedientes solo pueden relacionarse con otros expedientes

## Permisos

- **Usuario de Proyectos**: Puede crear y gestionar expedientes
- **Administrador de Proyectos**: Acceso completo a expedientes

## Estructura del Módulo

```
expedientes/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── project_expediente.py
├── views/
│   ├── project_expediente_views.xml
│   └── project_expediente_menus.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

## Versión

- **Versión**: 17.0.1.0.0
- **Compatible con**: Odoo 17.0

## Autor

Sadosky

## Licencia

LGPL-3
