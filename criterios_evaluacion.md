# Criterios de Evaluación - PI M0 Accenture

## Categorías de Evaluación

### 1. Construcción de la estructura básica del sistema

**Requerimiento:** Configurar entorno virtual, gestionar dependencias y organizar carpetas siguiendo buenas prácticas

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Entorno virtual creado, requirements.txt completo, carpetas bien organizadas (data/, sql/, src/, tests/), archivos clave presentes (README.md, .env, .gitignore) y justificación clara en la documentación. |
| **Satisfactorio** | Estructura y entorno funcionales, pero con detalles menores faltantes o desorganizados. |
| **Insuficiente** | Entorno o estructura incompleta, mala organización o errores en la gestión de dependencias. |

### 2. Carga en MySQL de los archivos CSV

**Requerimiento:** Carga completa de los archivos usando el script load_data.sql

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Carga completa de los archivos usando el script load_data.sql. Documentación clara de proceso. |
| **Satisfactorio** | Carga completa de los archivos usando el script load_data.sql, pero sin documentación clara del proceso realizado. |
| **Insuficiente** | Carga incompleta, sin documentación o con errores. |

### 3. Utilización de POO y patrones de diseño

#### 3.1 Crear clases para representar productos, clientes, transacciones y sucursales usando POO

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Clases completas, bien estructuradas, utilizando encapsulamiento y pruebas unitarias. |
| **Satisfactorio** | Clases implementadas correctamente, pero con limitaciones en encapsulamiento o pruebas. |
| **Insuficiente** | Clases incompletas, mal estructuradas o sin aplicar principios de POO. |

#### 3.2 Aplicar y justificar patrones de diseño para modularizar el sistema

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Patrón aplicado adecuadamente, con justificación clara y beneficios evidentes en modularidad. |
| **Satisfactorio** | Patrón aplicado, pero justificación limitada o modularidad mejorable. |
| **Insuficiente** | No se aplica ningún patrón de diseño o su aplicación es incorrecta. |

### 4. Implementación de SQL Avanzado

#### 4.1 Consultas SQL Avanzadas desde Python

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Al menos dos consultas SQL avanzadas (CTEs, funciones ventana), ejecutadas desde Python con salida en pandas, y bien documentadas. |
| **Satisfactorio** | Consultas correctas pero sin gran complejidad o sin ejecución desde Python. |
| **Insuficiente** | Consultas incompletas o incorrectas. |

#### 4.2 Implementación de objetos SQL

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Al menos dos objetos SQL creados y ejecutados (triggers, vistas, procedimientos, funciones), integrados y documentados. |
| **Satisfactorio** | Objetos creados pero sin ejecución integrada o documentación clara. |
| **Insuficiente** | Sin implementación o ejecución funcional. |

#### 4.3 Optimización de rendimiento

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Aplicación de índices, vistas materializadas u otros mecanismos con análisis de rendimiento justificado. |
| **Satisfactorio** | Optimización tentativa o sin análisis detallado. |
| **Insuficiente** | No se evidencia ninguna optimización. |

### 5. Optimización del entregable final

#### 5.1 Explicar decisiones, procesos y resultados en README o equivalente

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Documentación completa, clara y justificada para cada decisión técnica. |
| **Satisfactorio** | Documentación general, pero con falta de detalle o justificación en algunos apartados. |
| **Insuficiente** | Documentación pobre o ausente. |

#### 5.2 Mantener un código limpio, organizado, con estilo consistente y buenas prácticas

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Código limpio, bien estructurado, comentado y respetando estándares de la industria. |
| **Satisfactorio** | Código funcional pero con problemas menores de estilo o estructura. |
| **Insuficiente** | Código desorganizado o difícil de mantener. |

#### 5.3 Estructurar el repositorio adecuadamente y mantener un historial de cambios claro

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Estructura del repositorio clara, commits descriptivos y consistentes, README detallado. |
| **Satisfactorio** | Repositorio funcional, pero con desorganización menor o commits poco claros. |
| **Insuficiente** | Repositorio desorganizado, sin documentación o historial de cambios incompleto. |

## Extra Credits

> **Nota:** 0pts. - Valoración cualitativa: Se trata de un aspecto sobresaliente

### 1. Implementación de pruebas y aplicación justificada de otros patrones

**Requerimiento:** Crear una suite de pruebas unitarias que cubra al menos el 80% del código usando pytest y generar reportes de cobertura

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Pruebas extensas y cobertura demostrada (≥80%) con documentación de resultados. |
| **Satisfactorio** | Pruebas básicas con cobertura parcial (<80%) o sin reporte claro. |
| **Insuficiente** | Sin pruebas unitarias adicionales o cobertura irrelevante. |

### 2. Explorar y aplicar otros patrones de diseño adecuados

**Requerimiento:** Explorar y aplicar otros patrones de diseño adecuados que no hayan sido vistos obligatoriamente en clase

| Nivel | Descripción |
|-------|-------------|
| **Excelente** | Aplicación acertada y justificada de nuevos patrones, mejorando modularidad y escalabilidad. |
| **Satisfactorio** | Aplicación tentativa de nuevos patrones, sin gran impacto o justificaciones limitadas. |
| **Insuficiente** | No se exploran ni aplican patrones de diseño adicionales. |