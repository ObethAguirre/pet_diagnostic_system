# Sistema de Diagnóstico Automático para Mascotas v2.0

Sistema veterinario basado en teoría de la computación con configuración dinámica.

## Novedades en la Versión 2.0
- Configuración centralizada en `rules.json`
- Ponderación por severidad de síntomas
- Detección de patrones complejos
- Interfaz mejorada con información de configuración

## Estructura del Proyecto
pet_diagnostic_system/
├── data/
│ ├── diseases.json
│ └── rules.json
├── src/
│ ├── automata.py
│ ├── grammar.py
│ ├── turing_machine.py
│ ├── diagnostic.py
│ ├── interface.py
│ └── main.py
└── README.md

# Cambios aplicados:
- Pantalla de registro de mascota agregada.
- Diagnóstico con CheckBoxes dinámicos.
- Guardado de diagnóstico en archivo .txt.
- Historial muestra diagnósticos anteriores.
- Configuración de tema e idioma.
- Eliminación de opción de notificaciones.
