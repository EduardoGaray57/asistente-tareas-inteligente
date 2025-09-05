import tkinter as tk
from tkinter import messagebox, Toplevel
import time
import threading
import winsound
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class AsistenteTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente de Tareas Inteligente")

        # Lock para operaciones de BD thread-safe (debe ir antes de la conexión)
        self.db_lock = threading.Lock()
        
        # Conectar BD con check_same_thread=False
        self.conn = sqlite3.connect("historial_tareas.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

        # Lista de tareas
        self.tareas = []
        self.tarea_actual = 0
        self.contador_activo = False

        # Entrada de tarea
        tk.Label(root, text="Nombre de tarea:").pack()
        self.entry_tarea = tk.Entry(root, width=40)
        self.entry_tarea.pack()

        # Duración
        tk.Label(root, text="Duración (min):").pack()
        self.entry_duracion = tk.Entry(root, width=10)
        self.entry_duracion.pack()

        # Categoría
        tk.Label(root, text="Categoría:").pack()
        self.categoria_var = tk.StringVar(value="Trabajo")
        opciones = ["Trabajo", "Estudio", "Descanso", "Otro"]
        self.menu_categoria = tk.OptionMenu(root, self.categoria_var, *opciones)
        self.menu_categoria.pack()

        # Botón para agregar
        self.btn_agregar = tk.Button(root, text="Agregar Tarea", command=self.agregar_tarea)
        self.btn_agregar.pack(pady=5)

        # Lista visual
        tk.Label(root, text="Tareas del día:").pack()
        self.lista_tareas = tk.Listbox(root, width=50, height=10)
        self.lista_tareas.pack()

        # Contador
        self.label_contador = tk.Label(root, text="00:00", font=("Arial", 20), fg="blue")
        self.label_contador.pack(pady=10)

        # Botón iniciar
        self.btn_iniciar = tk.Button(root, text="Iniciar Tareas", command=self.iniciar_tareas)
        self.btn_iniciar.pack(pady=5)

        # Botón estadísticas
        self.btn_stats = tk.Button(root, text="Ver Estadísticas", command=self.mostrar_estadisticas)
        self.btn_stats.pack(pady=5)

        # Botón Graficos Torta
        self.btn_analisis = tk.Button(root, text="Análisis Inteligente", command=self.analizar_historial)
        self.btn_analisis.pack(pady=5)

        # Botón Graficos Barra
        self.btn_graf_dias = tk.Button(root, text="Productividad por días", command=self.graficar_por_dias)
        self.btn_graf_dias.pack(pady=5)

    def crear_tabla(self):
        with self.db_lock:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    duracion INTEGER,
                    categoria TEXT,
                    fecha TEXT
                )
            """)
            self.conn.commit()

    def agregar_tarea(self):
        nombre = self.entry_tarea.get()
        duracion = self.entry_duracion.get()
        categoria = self.categoria_var.get()

        if not nombre or not duracion.isdigit():
            messagebox.showwarning("Error", "Completa todos los campos correctamente")
            return
        
        # IA: intentar predecir categoría
        pred = self.predecir_categoria(nombre)
        if pred:
            categoria = pred
            messagebox.showinfo("Clasificación automática", f"La tarea fue clasificada como: {categoria}")

        tarea = {"nombre": nombre, "duracion": int(duracion), "categoria": categoria}
        self.tareas.append(tarea)

        mostrar = f"{nombre} - {duracion} min - {categoria}"
        self.lista_tareas.insert(tk.END, mostrar)

        # limpiar entradas
        self.entry_tarea.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)

    def iniciar_tareas(self):
        if not self.tareas:
            messagebox.showinfo("Sin tareas", "Agrega alguna tarea primero")
            return

        if not self.contador_activo:
            self.tarea_actual = 0
            self.ejecutar_tarea()

    def ejecutar_tarea(self):
        if self.tarea_actual < len(self.tareas):
            tarea = self.tareas[self.tarea_actual]
            duracion = tarea["duracion"] * 60
            nombre = tarea["nombre"]

            messagebox.showinfo("Nueva tarea", f"¡Comenzando: {nombre}!")
            self.contador_activo = True

            hilo = threading.Thread(target=self.contador, args=(duracion,))
            hilo.start()
        else:
            messagebox.showinfo("Completado", "¡Has terminado todas tus tareas!")
            self.contador_activo = False

    def contador(self, segundos):
        while segundos > 0 and self.contador_activo:
            mins, secs = divmod(segundos, 60)
            self.label_contador.config(text=f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            segundos -= 1

        if self.contador_activo:  # terminó el tiempo
            winsound.Beep(1000, 1000)
            tarea = self.tareas[self.tarea_actual]
            self.guardar_historial(tarea)
            messagebox.showinfo("Tarea terminada", f"Finalizó: {tarea['nombre']}")
            self.tarea_actual += 1
            self.ejecutar_tarea()

    def guardar_historial(self, tarea):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.db_lock:
            self.cursor.execute("INSERT INTO historial (nombre, duracion, categoria, fecha) VALUES (?, ?, ?, ?)",
                                (tarea["nombre"], tarea["duracion"], tarea["categoria"], fecha))
            self.conn.commit()

    def mostrar_estadisticas(self):
        ventana = Toplevel(self.root)
        ventana.title("Estadísticas de Productividad")

        with self.db_lock:
            # Tareas totales
            self.cursor.execute("SELECT COUNT(*) FROM historial")
            total = self.cursor.fetchone()[0]

            # Tiempo total
            self.cursor.execute("SELECT SUM(duracion) FROM historial")
            tiempo = self.cursor.fetchone()[0] or 0

            # Categorías
            self.cursor.execute("SELECT categoria, COUNT(*) FROM historial GROUP BY categoria")
            categorias = self.cursor.fetchall()

        tk.Label(ventana, text=f"📌 Tareas completadas: {total}").pack(pady=5)
        tk.Label(ventana, text=f"⏳ Tiempo total: {tiempo} min").pack(pady=5)

        tk.Label(ventana, text="📊 Por categorías:").pack(pady=5)
        for cat, count in categorias:
            tk.Label(ventana, text=f"- {cat}: {count}").pack()

    def analizar_historial(self):
        self.cursor.execute("SELECT categoria, SUM(duracion), COUNT(*) FROM historial GROUP BY categoria")
        resultados = self.cursor.fetchall()

        if not resultados:
            messagebox.showinfo("Análisis", "No hay datos suficientes todavía.")
            return

        categorias = [r[0] for r in resultados]  # categoria
        tiempos    = [r[1] for r in resultados]  # suma duración
        cantidades = [r[2] for r in resultados]  # cantidad

        # Mostrar sugerencia inteligente
        total_tiempo = sum(tiempos)
        recomendacion = ""

        if total_tiempo > 300:  # más de 5 horas
            recomendacion += "⚠ Has trabajado demasiado tiempo hoy, tomate un descanso.\n"
        if "Descanso" not in categorias:
            recomendacion += "💡 Considera programar una tarea de Descanso.\n"

        # Mostrar resultados y recomendación
        texto = "Tareas completadas por categoría:\n"
        for cat, t, c in resultados:
            texto += f"- {cat}: {c} tareas, {t} min\n"

        texto += "\nSugerencia:\n" + (recomendacion if recomendacion else "👌 Buen equilibrio de tareas.")

        messagebox.showinfo("Análisis Inteligente", texto)

        # Gráfico
        self.graficar_categorias(categorias, tiempos)

    def graficar_categorias(self, categorias, tiempos):
        plt.figure(figsize=(6, 6))
        plt.pie(tiempos, labels=categorias, autopct='%1.1f%%', startangle=140)
        plt.title("Distribución de tiempo por categoría")
        plt.show()

    def graficar_por_dias(self):
        self.cursor.execute("SELECT fecha, SUM(duracion) FROM historial GROUP BY DATE(fecha)")
        resultados = self.cursor.fetchall()

        if not resultados:
            messagebox.showinfo("Análisis", "No hay datos suficientes todavía.")
            return

        # Procesar fechas -> convertir a nombre de día
        dias = []
        tiempos = []
        for fecha, duracion in resultados:
            dia_num = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").weekday()
            nombre_dia = calendar.day_name[dia_num]
            dias.append(nombre_dia)
            tiempos.append(duracion)

        # Graficar
        plt.figure(figsize=(8, 5))
        plt.bar(dias, tiempos, color="skyblue")
        plt.xlabel("Día de la semana")
        plt.ylabel("Tiempo trabajado (min)")
        plt.title("Productividad por día de la semana")
        plt.show()

    def entrenar_clasificador(self):
        # Consultar historial
        self.cursor.execute("SELECT nombre, categoria FROM historial")
        datos = self.cursor.fetchall()

        if not datos or len(datos) < 3:
            return None, None
        
        textos = [d[0] for d in datos]
        etiquetas = [d[1] for d in datos]

        # Convertir texto a vectores TF-IDF
        vectorizador = TfidfVectorizer()
        X = vectorizador.fit_transform(textos)

        # Clasificador Naive Bayes
        modelo = MultinomialNB()
        modelo.fit(X, etiquetas)

        return modelo, vectorizador

    def predecir_categoria(self, texto):
        modelo, vectorizador = self.entrenar_clasificador()
        if modelo is None:
            return None
        
        X_nuevo = vectorizador.transform([texto])
        pred = modelo.predict(X_nuevo)[0]
        return pred

if __name__ == "__main__":
    root = tk.Tk()
    app = AsistenteTareas(root)
    root.mainloop()