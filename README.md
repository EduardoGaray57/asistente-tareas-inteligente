# 🧑‍💻 Asistente Personal de Tareas Inteligente

![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

Un asistente de escritorio escrito en **Python** que combina **automatización + IA ligera** para ayudarte a organizar tu día, gestionar tareas y analizar tu productividad.


## ✨ Características

✅ Gestión de tareas con duración y categoría  
✅ Temporizador automático (tipo Pomodoro)  
✅ Historial de tareas en **SQLite**  
✅ Estadísticas de productividad (tiempo total, categorías, número de tareas)  
✅ **Análisis inteligente** con recomendaciones  
✅ Gráficos con **matplotlib**:
   - Distribución de tiempo por categoría (pastel)  
   - Productividad por día de la semana (barras)  
✅ Clasificación automática de nuevas tareas con **IA (TF-IDF + Naive Bayes)**  

---

## 🛠️ Tecnologías utilizadas

- **Python 3.13**  
- **Tkinter** (interfaz gráfica)  
- **SQLite3** (base de datos local)  
- **Matplotlib** (gráficos)  
- **Scikit-learn** (IA ligera para clasificación de tareas)  

---

## 📦 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/asistente-tareas-inteligente.git
   cd asistente-tareas-inteligente
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Uso

Ejecuta el programa:
```bash
python main.py
```

1. Agrega tareas con nombre, duración (minutos) y categoría.  
2. Inicia la lista → se activa el temporizador automáticamente.  
3. Consulta estadísticas y análisis inteligente.  

---

## 🧠 IA integrada

El asistente utiliza un modelo de **Naive Bayes** entrenado con tu historial para **clasificar automáticamente las nuevas tareas** en:  
- Trabajo  
- Estudio  
- Descanso  
- Otro  

> Cuanto más uses el asistente, mejor aprende a categorizar tus tareas.  

---

## 📂 Estructura del proyecto

```
asistente-tareas-inteligente/
│── main.py              # Código principal
│── historial_tareas.db  # Base de datos SQLite (se genera automáticamente)
│── requirements.txt     # Dependencias del proyecto
│── README.md            # Documentación
│── LICENSE              # Licencia MIT
│── .gitignore           # Archivos a ignorar en Git

```

---

## 📋 Requisitos

- Python 3.10+ (probado en 3.13)
- Librerías indicadas en `requirements.txt`

Ejemplo de `requirements.txt`:
```
matplotlib
scikit-learn
```
*(Tkinter y sqlite3 ya vienen incluidos con Python)*

---

## 🚀 Futuras mejoras

- Exportar estadísticas a **PDF/Excel**  
- Dashboard web con **Streamlit**  
- Modelos de IA más avanzados para sugerencias personalizadas  

---

## 👨‍💻 Autor

- **Eduardo Garay**  
  - 📍 Quilicura, Región Metropolitana, Chile  
  - [GitHub](https://github.com/EduardoGaray57)  
  - [LinkedIn](https://www.linkedin.com/in/eduardo-garay-9b067b16b)  

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
