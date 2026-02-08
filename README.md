# Planificador Inteligente de Eventos - Freddy's Fazbear Pizza

## Descripcion del Proyecto

El **Planificador Inteligente de Eventos** es una aplicacion de software completa disenada para gestionar y planificar eventos que consumen recursos de un inventario limitado en Freddy's Fazbear Pizza. El sistema garantiza que no existan conflictos en la asignacion de recursos respetando un conjunto de reglas y restricciones personalizadas basadas en la tematica de Five Nights at Freddy's.

## Objetivo Principal

Desarrollar un motor de planificacion inteligente que garantice:
1.  **Evitar conflictos de recursos**: Ningun recurso puede asignarse a mas de un evento simultaneamente.
2.  **Respetar restricciones personalizadas**: Cumplir con reglas especificas de co-requisitos y exclusiones mutuas inspiradas en la historia de FNaF.

## Dominio Elegido: Freddy's Fazbear Pizza

El entorno de Freddy's Fazbear Pizza proporciona un escenario rico para modelar restricciones complejas, donde la **seguridad** y la **gestion adecuada de animatronicos** son fundamentales para evitar incidentes.

### Eventos
Actividades principales que requieren planificacion temporal y asignacion de recursos:
-   **Espectaculos musicales** con los animatronicos
-   **Mantenimiento y reparaciones** de equipos y animatronicos
-   **Rondas de seguridad** nocturnas
-   **Actividades especiales** con el traje Springlock

### Recursos (Organizados por Categorias)

#### Animatronicos
-   Freddy Fazbear (cantidad: 1)
-   Bonnie la Guitarra (cantidad: 1)
-   Chica la Pollo (cantidad: 1)
-   Foxy el Pirata (cantidad: 1)
-   Golden Freddy (cantidad: 1)

#### Salas
-   Escenario Principal (cantidad: 1)
-   Sala de Mantenimiento (cantidad: 1)
-   Cocina (cantidad: 1)
-   Pasillo Este (cantidad: 1)
-   Almacen (cantidad: 1)

#### Equipos
-   Traje de Asistente (Springlock) (cantidad: 1)
-   Kit de Herramientas (cantidad: 3)
-   Camara de Seguridad (cantidad: 4)
-   Sistema de Audio (cantidad: 1)

#### Personal
-   Tecnico Nocturno (cantidad: 2)
-   Guardia de Seguridad (cantidad: 1)

## Restricciones Implementadas

### Restricciones de Co-requisito (Inclusion)
1.  **Traje de Asistente (Springlock)** requiere **Tecnico Nocturno**
    *Motivo*: El traje Springlock es extremadamente peligroso y requiere supervision tecnica constante.
2.  **Freddy Fazbear** requiere **Chica la Pollo** y **Bonnie la Guitarra**
    *Motivo*: La banda completa debe estar presente para los espectaculos principales.
3.  **Camara de Seguridad** requiere **Guardia de Seguridad** y **Tecnico Nocturno**
    *Motivo*: Las camaras necesitan monitoreo activo y mantenimiento tecnico.

### Restricciones de Exclusion Mutua
1.  **Golden Freddy** no puede usarse con **Freddy Fazbear**
    *Motivo*: Dos Freddys causan confusion en los sistemas de los animatronicos.
2.  **Traje de Asistente (Springlock)** no puede usarse con **Cocina**
    *Motivo*: La humedad de la cocina activa los resortes del traje (springlock failure).
3.  **Foxy el Pirata** no puede usarse con **Sala de Mantenimiento**
    *Motivo*: Foxy es impredecible en espacios cerrados.
4.  **Traje de Asistente (Springlock)** no puede usarse con **Guardia de Seguridad**
    *Motivo*: Protocolo de seguridad: separar riesgos.
5.  **Cocina** no puede usarse con **Sistema de Audio**
    *Motivo*: El ruido interfiere con los sistemas de audio sensibles.

## Implementacion Tecnica

### Arquitectura del Sistema
```
fazbear_planner/
├── main.py              # Interfaz principal del programa
├── event.py             # Clase Evento con gestion temporal
├── resource.py          # Clase Recurso con tipos y cantidades
├── constraint.py        # Gestor de restricciones personalizadas
├── storage.py           # Sistema de persistencia en JSON
├── planner.py           # Motor de planificacion inteligente
├── fazbear_data.json    # Archivo de datos persistente
└── README.md            # Este documento
```

### Operaciones Principales

#### 1. Planificar un Nuevo Evento
El sistema verifica automaticamente:
-   **Conflictos de recursos**: Disponibilidad temporal de cada recurso solicitado
-   **Disponibilidad por cantidad**: Para recursos con multiples unidades (ej: 4 camaras)
-   **Violacion de restricciones**: Validacion de co-requisitos y exclusiones

#### 2. Busqueda Automatica de Horarios ("Buscar Hueco")
Funcion inteligente que analiza el calendario y sugiere el proximo intervalo disponible donde el evento pueda realizarse sin conflictos.

#### 3. Gestion Completa
-   Listar todos los eventos programados
-   Agregar nuevos eventos con validacion
-   Eliminar eventos existentes liberando recursos
-   Consultar agenda especifica de recursos

### Persistencia de Datos
Todo el estado de la aplicacion se guarda y carga desde un archivo unico `fazbear_data.json` que contiene:
-   Definicion completa de recursos
-   Lista de eventos planificados
-   Conjunto de restricciones activas

## Como Ejecutar el Proyecto

### Requisitos Previos
-   Python 3.8 o superior
-   Modulos estandar de Python (no se requieren librerias externas)

### Instalacion y Ejecucion
```bash
# 1. Clonar o descargar los archivos del proyecto
# 2. Navegar al directorio del proyecto
cd fazbear_planner

# 3. Ejecutar la aplicacion
python main.py
```

### Flujo de Uso Tipico
1.  **Iniciar la aplicacion**: Se cargan automaticamente los datos existentes o se crean los predeterminados
2.  **Planificar evento**: Usar opcion 2 del menu, ingresando nombre, recursos, fecha y duracion
3.  **Validacion automatica**: El sistema verifica disponibilidad y restricciones
4.  **Confirmacion**: Evento se agrega al calendario si pasa todas las validaciones
5.  **Persistencia**: Al salir (opcion 8), todos los datos se guardan automaticamente

## Ejemplos de Uso

### Ejemplo 1: Espectaculo Nocturno
```
Nombre: Gran Espectaculo Musical
Recursos: Freddy Fazbear, Bonnie la Guitarra, Chica la Pollo, Sistema de Audio, Escenario Principal
Fecha: 2025-12-25
Hora: 21:00
Duracion: 2 horas
Resultado: Evento programado exitosamente
```

### Ejemplo 2: Intento Violando Restriccion
```
Nombre: Reparacion Riesgosa
Recursos: Traje de Asistente (Springlock), Cocina
Fecha: 2025-12-26
Hora: 14:00
Duracion: 1 hora
Resultado: Restriccion violada: Los recursos 'Traje de Asistente (Springlock)' y 'Cocina' no pueden usarse juntos
```

## Funcionalidades del Menu
1.  **Ver eventos programados**: Muestra todos los eventos con recursos asignados
2.  **Planificar nuevo evento**: Interfaz guiada para crear eventos validados
3.  **Buscar hueco para evento**: Encuentra automaticamente el proximo horario disponible
4.  **Eliminar evento**: Remueve eventos liberando sus recursos
5.  **Ver agenda de un recurso**: Muestra todos los eventos que usan un recurso especifico
6.  **Ver restricciones**: Lista todas las reglas activas de co-requisitos y exclusiones
7.  **Ver recursos disponibles**: Muestra recursos organizados por categorias
8.  **Guardar y salir**: Persiste datos y cierra la aplicacion

## Testing y Validacion
El sistema incluye validacion exhaustiva para:
-   Formatos de fecha/hora incorrectos
-   Recursos inexistentes
-   Conflictos temporales
-   Violaciones de restricciones
-   Intento de programar en el pasado

## Control de Versiones
El proyecto utiliza Git con commits frecuentes que muestran progreso incremental:
-   Arquitectura modular inicial
-   Implementacion de clases basicas
-   Sistema de restricciones personalizadas
-   Motor de planificacion inteligente
-   Persistencia en JSON
-   Interfaz de usuario en consola
-   Validacion y manejo de errores

## Aprendizajes y Habilidades Desarrolladas
Este proyecto demuestra competencia en:
-   **Diseno orientado a objetos** en Python
-   **Gestion de intervalos temporales** con datetime
-   **Validacion de reglas de negocio** complejas
-   **Persistencia de datos** con JSON
-   **Interfaces de usuario** en consola
-   **Resolucion de problemas** del mundo real (gestion de recursos limitados)
