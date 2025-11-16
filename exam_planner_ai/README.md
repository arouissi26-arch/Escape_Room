# 📚 Planificador de Exámenes con IA

Aplicación web inteligente para generar tarjetas de estudio automáticamente usando **Inteligencia Artificial** y **Procesamiento de Lenguaje Natural (NLP)**.

## 🚀 Características

- **🤖 IA Propia**: Motor de IA desarrollado en Python desde cero
- **📝 Generación Automática**: Crea preguntas y respuestas de forma inteligente
- **🎯 Múltiples Tipos**: Genera preguntas de definición, completar, características y causales
- **📅 Planificador**: Organiza tu calendario de exámenes
- **💾 Guardado Automático**: Datos guardados localmente
- **✨ 100% Gratis**: Sin APIs externas ni costos

## 🛠️ Tecnologías

- **Backend**: Python 3 + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **IA**: Procesamiento de Lenguaje Natural (NLP) personalizado
- **Base de datos**: LocalStorage + JSON

## 📋 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio o navegar a la carpeta

```bash
cd exam_planner_ai
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install Flask flask-cors
```

### 3. Iniciar el servidor

```bash
python app.py
```

O en Linux/Mac:

```bash
python3 app.py
```

### 4. Abrir en el navegador

Abre tu navegador y visita:

```
http://localhost:5000
```

## 📖 Cómo Usar

### Generar Tarjetas de Estudio

1. **Pega tu contenido**: Copia tus apuntes en el área de texto
2. **O sube un archivo**: Arrastra un archivo TXT
3. **Haz clic en "Generar Tarjetas con IA"**
4. **¡Listo!**: La IA creará automáticamente preguntas y respuestas

### Ejemplo de Contenido

```
La fotosíntesis es el proceso por el cual las plantas convierten
la luz solar en energía química. Este proceso ocurre en los
cloroplastos.

Las mitocondrias son las centrales energéticas de la célula
porque producen ATP mediante la respiración celular.

El ADN contiene la información genética de todos los seres vivos.
Está formado por nucleótidos que se organizan en una doble hélice.
```

### Tipos de Preguntas Generadas

La IA genera **4 tipos diferentes** de preguntas:

1. **Definición**: "¿Qué es la fotosíntesis?"
2. **Completar**: "Completa: Las ______ son las centrales energéticas"
3. **Características**: "¿Qué contiene el ADN?"
4. **Causales**: "¿Por qué las mitocondrias son centrales energéticas?"

### Planificar Exámenes

1. Haz clic en "+ Añadir Examen"
2. Completa la información:
   - Asignatura
   - Fecha
   - Hora
3. La app calculará los días restantes automáticamente

## 🧠 Cómo Funciona la IA

El motor de IA utiliza:

- **Análisis sintáctico**: Identifica estructura de oraciones
- **Extracción de palabras clave**: Detecta conceptos importantes
- **Reconocimiento de patrones**: Encuentra definiciones y relaciones
- **Filtrado de stopwords**: Elimina palabras comunes
- **Generación de preguntas**: Crea preguntas basadas en patrones

### Algoritmos Implementados

```python
- Tokenización de texto
- Análisis de frecuencia de palabras
- Reconocimiento de verbos clave
- Extracción de relaciones sujeto-predicado
- Generación de preguntas por patrones regex
```

## 📁 Estructura del Proyecto

```
exam_planner_ai/
│
├── app.py                  # Servidor Flask
├── ai_engine.py            # Motor de IA (NLP)
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
│
├── templates/
│   └── index.html         # Frontend HTML
│
├── static/
│   ├── css/
│   │   └── styles.css     # Estilos
│   └── js/
│       └── app.js         # Lógica frontend
│
└── data/                  # Datos guardados (auto-creado)
```

## 🔌 API Endpoints

### POST /api/generate
Genera tarjetas de estudio

**Request:**
```json
{
  "content": "Tu texto aquí..."
}
```

**Response:**
```json
{
  "success": true,
  "flashcards": [...],
  "count": 10
}
```

### POST /api/analyze
Analiza texto y extrae conceptos

### GET /health
Verifica estado del servidor

## 🎨 Personalización

### Cambiar el tema de colores

Edita `static/css/styles.css`:

```css
:root {
    --accent-gold: #d4af37;  /* Color principal */
    --primary-bg: #0f0f0f;   /* Fondo */
    ...
}
```

### Agregar más tipos de preguntas

Edita `ai_engine.py` y añade nuevos métodos en la clase `StudyAI`.

## 🐛 Solución de Problemas

### El servidor no inicia

```bash
# Verifica que Flask esté instalado
pip install Flask

# Verifica la versión de Python
python --version  # Debe ser 3.7+
```

### No se generan tarjetas

- Asegúrate de que el texto tenga oraciones completas
- Usa puntos (.) para separar ideas
- Escribe definiciones claras: "X es Y"

### Error de conexión

- Verifica que el servidor esté corriendo
- Comprueba que estés en `http://localhost:5000`
- Revisa la consola del navegador (F12)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Creado con ❤️ para ayudarte a estudiar mejor

## 🙏 Agradecimientos

- Inspirado en técnicas de estudio activo
- Basado en principios de aprendizaje espaciado
- Motor de IA desarrollado desde cero

---

**¿Preguntas? ¿Sugerencias?**

Abre un issue en GitHub o contáctanos directamente.

¡Buena suerte en tus exámenes! 🎓✨
