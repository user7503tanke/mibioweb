from flask import Flask, render_template, jsonify, request, session
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-nathan-gato'
app.config['PERMANENT_SESSION_LIFETIME'] = 604800

# ========== DATOS DE NATHÁN ==========
def calcular_edad(fecha_nacimiento):
    from datetime import datetime
    nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()
    edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
    return edad

# ========== DATOS SIMPLIFICADOS ==========
NATHAN_PERFIL = {
    "nombre": "Nathán Pérez",
    "apodo": "El Gato",
    "titulo": "Técnico en Reparación • Desarrollador",
    "ubicacion": "Boca de Camarioca, Matanzas, Cuba",
    "email": "nathanperezalejo22@gmail.com",
    "edad": calcular_edad("2009-12-22"),
    "bio": f"{calcular_edad('2009-12-22')} años. Especialista en reparación de dispositivos móviles y desarrollo de software. Soluciones técnicas confiables y personalizadas.",
    "telefono": "+53 59642359"
}

# Elimina FRASES_NATHAN completamente

# Datos simplificados para el index
DATOS_INDEX = {
    "servicios_destacados": [
        {
            "icono": "📱",
            "titulo": "Reparación Móvil",
            "desc": "Pantallas, puertos, baterías, mantenimiento",
            "color": "#f59e0b",  # Amarillo
            "categoria": "reparacion"
        },
        {
            "icono": "💻",
            "titulo": "Apps Multiplataforma",
            "desc": "Desarrollo de aplicaciones compatibles en android, windows y Mac",
            "color": "#3b82f6",  # Azul
            "categoria": "programacion"
        },
        {
            "icono": "🌐",
            "titulo": "Páginas Web",
            "desc": "Sitios web responsivos y modernos.",
            "color": "#10b981",  # Verde
            "categoria": "programacion"
        }
    ],
    "estadisticas": [
        {"numero": "200+", "texto": "Dispositivos Reparados"},
        {"numero": "20+", "texto": "Proyectos de Software"},
        {"numero": "89%", "texto": "Clientes Satisfechos"},
        {"numero": "3+", "texto": "Años de Experiencia"}
    ]
}
# ========== SERVICIOS ==========

TUS_SERVICIOS_CATALOGO = {
    "programacion": [
        {
            "id": "android_app",
            "nombre": "Apps Multiplataforma",
            "icono": "📱",
            "descripcion": "Aplicaciones para Android, Windows y MacOS. Desde apps simples hasta sistemas completos.",
            "herramientas": ["Kotlin", "Java", "C++"],
            "destacado": True,
            "color_borde": "#3b82f6"
        },
        {
            "id": "web_app",
            "nombre": "Páginas Web",
            "icono": "🌐",
            "descripcion": "Sitios web y aplicaciones web responsivas con Python, Flask y tecnologías modernas.",
            "herramientas": ["Python", "Flask", "HTML/CSS", "JavaScript"],
            "destacado": True,
            "color_borde": "#10b981"
        },
        {
            "id": "bots",
            "nombre": "Bots Automáticos",
            "icono": "🤖",
            "descripcion": "Bots para Telegram, automatización de tareas, scraping de datos y procesos repetitivos.",
            "herramientas": ["Python", "Pyrogram", "Selenium"],
            "destacado": False,
            "color_borde": "#8b5cf6"
        },
        {
            "id": "scripts",
            "nombre": "Scripts Personalizados",
            "icono": "⚙️",
            "descripcion": "Programas a medida para resolver problemas específicos de tu negocio o flujo de trabajo.",
            "herramientas": ["Python", "Visual Basic", "Bash"],
            "destacado": False,
            "color_borde": "#6366f1"
        }
    ],
    "reparacion": [
        {
            "id": "pantallas",
            "nombre": "Cambio de Pantallas",
            "icono": "📱",
            "descripcion": "Reemplazo profesional de pantallas rotas o dañadas. Garantía en la instalación.",
            "marcas": ["iPhone", "Samsung", "Xiaomi", "Huawei"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "puertos",
            "nombre": "Cambio de Puerto de Carga",
            "icono": "🔌",
            "descripcion": "Reparación de puertos de carga defectuosos. Recupera la carga rápida de tu dispositivo.",
            "marcas": ["Todas las marcas"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "unred",
            "nombre": "Desbloqueo de Red(Compañia)",
            "icono": "🔓",
            "descripcion": "Desbloquea tu dispositivo para poder usar cualquier operador por ejemplo Cubacel.",
            "marcas": ["Todas las marcas"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "baterias",
            "nombre": "Cambio de Baterías",
            "icono": "🔋",
            "descripcion": "Reemplazo de baterías hinchadas o con poca duración. Baterías de calidad original.",
            "marcas": ["iPhone", "Samsung", "Android en general"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "unfrp",
            "nombre": "Desbloqueo de Frp (Cuenta google)",
            "icono": "🔓",
            "descripcion": "Desbloquea tu dispositivo para poder usar todas sus funciones.",
            "marcas": ["Todas las marcas"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "mantenimiento",
            "nombre": "Mantenimiento General",
            "icono": "🔧",
            "descripcion": "Limpieza interna, diagnóstico completo, solución de problemas de software y hardware.",
            "servicios": ["Limpieza", "Diagnóstico", "Optimización"],
            "destacado": False,
            "color_borde": "#ef4444"
        },
        {
            "id": "unmdm",
            "nombre": "Desbloqueo de MDM, PayJoy o KG lock(Falta de pagos)",
            "icono": "🔓",
            "descripcion": "Desbloquea tu dispositivo para poder usar todas sus funciones.",
            "marcas": ["Todas las marcas"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "unicloud",
            "nombre": "Desbloqueo (bypass) iCloud sin Señal",
            "icono": "🔓",
            "descripcion": "Desbloquea tu iphone del XS en adelante para poder usar todas sus funciones excepto red celular.",
            "marcas": ["Todas las marcas"],
            "destacado": True,
            "color_borde": "#f59e0b"
        },
        {
            "id": "unmicloud",
            "nombre": "Desbloqueo (bypass) Cuenta MI Xiaomi",
            "icono": "🔓",
            "descripcion": "Desbloqueo sin ataduras.",
            "marcas": ["Todas las marcas"],
            "destacado": True,
            "color_borde": "#f59e0b"
        }
    ]
}

# Añade esto después de las importaciones existentes
import re
from datetime import datetime

# ========== DATOS DE RESEÑAS CON BASE DE DATOS SIMULADA ==========
RESENAS_FILE = 'data/resenas.json'

def cargar_resenas():
    """Cargar reseñas desde el archivo JSON"""
    try:
        os.makedirs('data', exist_ok=True)
        if os.path.exists(RESENAS_FILE):
            with open(RESENAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error cargando reseñas: {e}")
    return []

def guardar_resenas(resenas):
    """Guardar reseñas en el archivo JSON"""
    try:
        with open(RESENAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(resenas, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando reseñas: {e}")
        return False

def agregar_resena(cliente, lugar, servicio, descripcion, valoracion):
    """Agregar una nueva reseña"""
    try:
        resenas = cargar_resenas()
        
        # Crear ID único
        nuevo_id = max([r.get('id', 0) for r in resenas], default=0) + 1
        
        # Formatear el nombre con lugar
        if lugar and lugar.strip():
            cliente_formateado = f"{cliente} ({lugar})"
        else:
            cliente_formateado = cliente
        
        nueva_resena = {
            "id": nuevo_id,
            "cliente": cliente_formateado,
            "servicio": servicio,
            "fecha": datetime.now().strftime("%B %Y"),
            "descripcion": descripcion,
            "imagen": "default_resena.jpg",
            "categoria": "reparacion",  # Por defecto, puedes ajustar si necesitas categorías
            "valoracion": int(valoracion),
            "aprobada": False  # Para moderación
        }
        
        resenas.append(nueva_resena)
        guardar_resenas(resenas)
        return True, "Reseña enviada para aprobación. ¡Gracias!"
    except Exception as e:
        return False, f"Error: {str(e)}"

# ========== TRABAJOS_RECIENTES actualizado ==========
# Reemplaza el TRABAJOS_RECIENTES existente con este:
TRABAJOS_RECIENTES = [
   
]

# ========== AÑADIR ESTA NUEVA RUTA ==========
@app.route('/agregar-resena', methods=['GET', 'POST'])
def agregar_resena_view():
    theme = get_theme()
    mensaje = None
    tipo_mensaje = None  # 'success' o 'error'
    
    if request.method == 'POST':
        cliente = request.form.get('cliente', '').strip()
        lugar = request.form.get('lugar', '').strip()
        servicio = request.form.get('servicio', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        valoracion = request.form.get('valoracion', '5')
        
        # Validaciones básicas
        if not cliente:
            mensaje = "Por favor, escribe tu nombre."
            tipo_mensaje = 'error'
        elif not servicio:
            mensaje = "Por favor, indica qué servicio recibiste."
            tipo_mensaje = 'error'
        elif not descripcion or len(descripcion) < 10:
            mensaje = "Por favor, escribe una descripción más detallada (mínimo 10 caracteres)."
            tipo_mensaje = 'error'
        else:
            success, msg = agregar_resena(cliente, lugar, servicio, descripcion, valoracion)
            mensaje = msg
            tipo_mensaje = 'success' if success else 'error'
            
            if success:
                # Limpiar el formulario después de éxito
                cliente = lugar = servicio = descripcion = ""
    
    return render_template('agregar_resena.html',
                         perfil=NATHAN_PERFIL,
                         theme=theme,
                         mensaje=mensaje,
                         tipo_mensaje=tipo_mensaje)

# ========== MODIFICAR LA RUTA DE TRABAJOS ==========
@app.route('/trabajos')
def trabajos():
    theme = get_theme()
    categoria = request.args.get('categoria', 'todos')
    
    # Cargar reseñas aprobadas
    resenas_aprobadas = [r for r in cargar_resenas() if r.get('aprobada', False)]
    
    # Combinar trabajos fijos con reseñas aprobadas
    todos_trabajos = TRABAJOS_RECIENTES + resenas_aprobadas
    
    if categoria == 'todos':
        trabajos_filtrados = todos_trabajos
    else:
        trabajos_filtrados = [t for t in todos_trabajos if t['categoria'] == categoria]
    
    return render_template('trabajos.html',
                         perfil=NATHAN_PERFIL,
                         trabajos=trabajos_filtrados,
                         categoria_activa=categoria,
                         theme=theme)

# ========== RUTA PARA ADMIN (APROBAR RESEÑAS) ==========
@app.route('/admin/resenas')
def admin_resenas():
    theme = get_theme()
    # Aquí podrías agregar autenticación simple si quieres
    resenas = cargar_resenas()
    resenas_pendientes = [r for r in resenas if not r.get('aprobada', False)]
    resenas_aprobadas = [r for r in resenas if r.get('aprobada', False)]
    
    return render_template('admin_resenas.html',
                         perfil=NATHAN_PERFIL,
                         theme=theme,
                         pendientes=resenas_pendientes,
                         aprobadas=resenas_aprobadas)

@app.route('/admin/aprobar-resena/<int:resena_id>')
def aprobar_resena(resena_id):
    resenas = cargar_resenas()
    for resena in resenas:
        if resena['id'] == resena_id:
            resena['aprobada'] = True
            guardar_resenas(resenas)
            break
    return jsonify({'success': True})

@app.route('/admin/eliminar-resena/<int:resena_id>')
def eliminar_resena(resena_id):
    resenas = cargar_resenas()
    resenas = [r for r in resenas if r['id'] != resena_id]
    guardar_resenas(resenas)
    return jsonify({'success': True})

# ========== INICIALIZACIÓN actualizada ==========
def init_data():
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists('data/posts.json'):
        initial_posts = [
            {
                "id": 1,
                "titulo": "Lecciones del Dinero",
                "contenido": """<h2>Lo que aprendí ganando y perdiendo</h2>
                <p>El dinero es curioso. Te persigues cuando no lo tienes, y cuando lo consigues, descubres que no era la respuesta...</p>""",
                "resumen": "Reflexiones sobre finanzas desde los 11 años",
                "fecha": "2026-01-20",
                "categoria": "Finanzas",
                "etiquetas": ["dinero", "aprendizaje", "negocios"],
                "tiempo_lectura": "5 min",
                "imagen": "dinero.jpg"
            }
        ]
        with open('data/posts.json', 'w', encoding='utf-8') as f:
            json.dump(initial_posts, f, indent=2, ensure_ascii=False)
    
    # Inicializar archivo de reseñas si no existe
    if not os.path.exists(RESENAS_FILE):
        with open(RESENAS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)

# ========== FUNCIONES ==========
def get_theme():
    return session.get('theme', 'light')

def load_posts():
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
            for post in posts:
                if 'categoria' not in post:
                    post['categoria'] = 'Reflexión'
            return posts
    except FileNotFoundError:
        return []

def get_posts_by_category(category):
    posts = load_posts()
    if category == 'todas':
        return posts
    return [p for p in posts if p.get('categoria', '').lower() == category.lower()]

# ========== RUTAS ==========
@app.route('/')
def index():
    theme = get_theme()
  
    return render_template('index.html',
                         perfil=NATHAN_PERFIL,
                         datos_index=DATOS_INDEX,
                         theme=theme)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    theme = get_theme()
    success = False
    
    if request.method == 'POST':
        success = True
    
    return render_template('contact.html', success=success, perfil=NATHAN_PERFIL, theme=theme)

@app.route('/servicios')
def servicios():
    theme = get_theme()
    categoria = request.args.get('categoria', 'reparacion')
    return render_template('servicios.html',
                         perfil=NATHAN_PERFIL,
                         servicios=TUS_SERVICIOS_CATALOGO,
                         categoria_activa=categoria,
                         theme=theme)





@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    current_theme = get_theme()
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    return jsonify({'theme': new_theme})

# ========== INICIALIZACIÓN ==========
def init_data():
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists('data/posts.json'):
        initial_posts = [
            {
                "id": 1,
                "titulo": "Lecciones del Dinero",
                "contenido": """<h2>Lo que aprendí ganando y perdiendo</h2>
                <p>El dinero es curioso. Te persigues cuando no lo tienes, y cuando lo consigues, descubres que no era la respuesta...</p>""",
                "resumen": "Reflexiones sobre finanzas desde los 11 años",
                "fecha": "2026-01-20",
                "categoria": "Finanzas",
                "etiquetas": ["dinero", "aprendizaje", "negocios"],
                "tiempo_lectura": "5 min",
                "imagen": "dinero.jpg"
            },
            {
                "id": 2,
                "titulo": "La Lógica como Superpoder",
                "contenido": """<h2>Resolver problemas como un juego</h2>
                <p>La programación me enseñó que todo problema tiene solución...</p>""",
                "resumen": "Cómo la lógica transformó mi forma de pensar",
                "fecha": "2026-01-18",
                "categoria": "Lógica",
                "etiquetas": ["lógica", "programación", "pensamiento"],
                "tiempo_lectura": "4 min",
                "imagen": "logica.jpg"
            }
        ]
        with open('data/posts.json', 'w', encoding='utf-8') as f:
            json.dump(initial_posts, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    init_data()
    app.run(host="0.0.0.0", debug=True, port=5000)