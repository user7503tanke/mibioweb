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
NATHAN_PERFIL = {
    "nombre": "Nathán Pérez",
    "apodo": "El Gato",
    "titulo": "Musico • Poeta • Loco",
    "ubicacion": "Boca de Camarioca, Matanzas, Cuba",
    "email": "nathanperezalejo22@gmail.com",
    "bio": str(calcular_edad("2009-12-22"))+" años. Buscando la perfección en la lógica, la belleza en las matemáticas y el sentido en la filosofía. Autodidacta desde los 10.",
    "edad": calcular_edad("2009-12-22"),
    "nacimiento": "22 de diciembre del 2009",
    "freelance": True
}

# FRASES FILOSÓFICAS Y LÓGICAS (como te gustan)
FRASES_NATHAN = [
    {
        "texto": "La perfección no se alcanza cuando no hay nada más que añadir, sino cuando no hay nada más que quitar.",
        "autor": "Antoine de Saint-Exupéry",
        "categoria": "Perfección"
    },    {
        "texto": "El fin justifica los medios.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Política"
    },
    {
        "texto": "Más vale ser temido que amado, si no se puede ser ambas cosas.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Poder"
    },
    {
        "texto": "Los hombres olvidan antes la muerte de su padre que la pérdida de su patrimonio.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Naturaleza Humana"
    },
    {
        "texto": "Hay que ser zorro para conocer las trampas y león para espantar a los lobos.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Estrategia"
    },
    {
        "texto": "Es más seguro ser temido que ser amado.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Poder"
    },
    {
        "texto": "Todos ven lo que aparentas; pocos advierten lo que eres.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Realismo Político"
    },
    {
        "texto": "Un príncipe debe parecer piadoso, fiel, humano, íntegro, religioso... y serlo, pero con la mente preparada para poder y saber cambiar a lo contrario si es necesario.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Realismo Político"
    },
    {
        "texto": "La promesa dada fue una necesidad del pasado; la palabra rota es una necesidad del presente.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Estrategia"
    },
    {
        "texto": "Los hombres ofenden antes al que aman que al que temen.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Naturaleza Humana"
    },
    {
        "texto": "La crueldad está bien usada cuando se ejecuta de una sola vez, por necesidad de seguridad.",
        "autor": "Nicolás Maquiavelo",
        "categoria": "Poder"
    },
    {
        "texto": "La lógica te llevará de A a B. La imaginación te llevará a cualquier parte.",
        "autor": "Albert Einstein",
        "categoria": "Lógica"
    },
    {
        "texto": "No es lo que miras lo que importa, es lo que ves.",
        "autor": "Henry David Thoreau",
        "categoria": "Perspectiva"
    },
    {
        "texto": "El dinero es un buen sirviente pero un mal amo.",
        "autor": "Francis Bacon",
        "categoria": "Dinero"
    },
    {
        "texto": "La vida es un 10% lo que me pasa y un 90% cómo reacciono ante ello.",
        "autor": "Charles R. Swindoll",
        "categoria": "Actitud"
    },
    {
        "texto": "Si tienes miedo, no lo hagas. Si lo haces, no tengas miedo.",
        "autor": "Gengis Kan",
        "categoria": "Actitud"
    },
    {
        "texto": "La única constante en la vida es el cambio.",
        "autor": "Heráclito",
        "categoria": "Cambio"
    },
    # **Nuevas frases añadidas:**
    {
        "texto": "Pienso, luego existo.",
        "autor": "René Descartes",
        "categoria": "Existencia"
    },
    {
        "texto": "Conócete a ti mismo.",
        "autor": "Inscripción en el Templo de Apolo en Delfos",
        "categoria": "Autoconocimiento"
    },
    {
        "texto": "La virtud está en el término medio.",
        "autor": "Aristóteles",
        "categoria": "Ética"
    },
    {
        "texto": "Lo que no me mata, me hace más fuerte.",
        "autor": "Friedrich Nietzsche",
        "categoria": "Resiliencia"
    },
    {
        "texto": "El hombre está condenado a ser libre.",
        "autor": "Jean-Paul Sartre",
        "categoria": "Libertad"
    },
    {
        "texto": "No hay hechos, sólo interpretaciones.",
        "autor": "Friedrich Nietzsche",
        "categoria": "Perspectiva"
    },
    {
        "texto": "El mayor enemigo del conocimiento no es la ignorancia, sino la ilusión del conocimiento.",
        "autor": "Stephen Hawking",
        "categoria": "Conocimiento"
    },
    {
        "texto": "La verdad se encuentra en la simplicidad, y no en la multiplicidad y confusión de las cosas.",
        "autor": "Isaac Newton",
        "categoria": "Verdad"
    },
    {
        "texto": "Dudar de todo o creerlo todo son dos soluciones igualmente convenientes, pues ambas nos evitan reflexionar.",
        "autor": "Henri Poincaré",
        "categoria": "Pensamiento Crítico"
    },
    {
        "texto": "La ciencia es lo que sabemos; la filosofía es lo que no sabemos.",
        "autor": "Bertrand Russell",
        "categoria": "Ciencia y Filosofía"
    },
    
    {
        "texto": "Es en los juegos donde los hombres se muestran tal como son.",
        "autor": "Blaise Pascal",
        "categoria": "Naturaleza Humana"
    },
    {
        "texto": "Ser es ser percibido.",
        "autor": "George Berkeley",
        "categoria": "Existencia"
    },
    {
        "texto": "La función de la lógica es meramente analítica, no creativa.",
        "autor": "Ludwig Wittgenstein",
        "categoria": "Lógica"
    },
    {
        "texto": "El sabio puede cambiar de opinión. El necio, nunca.",
        "autor": "Immanuel Kant",
        "categoria": "Sabiduría"
    },
    {
        "texto": "La ausencia de prueba no es prueba de ausencia.",
        "autor": "Carl Sagan (atribuida comúnmente)",
        "categoria": "Lógica y Escepticismo"
    },
    {
        "texto": "Para quien sólo tiene un martillo, todo le parece un clavo.",
        "autor": "Abraham Maslow",
        "categoria": "Perspectiva"
    },
    {
        "texto": "La contradicción no es un signo de falsedad, ni la no contradicción lo es de verdad.",
        "autor": "Blaise Pascal",
        "categoria": "Lógica"
    },
    {
        "texto": "La esperanza es un deseo que tiende hacia el futuro; el arrepentimiento, un deseo que tiende hacia el pasado.",
        "autor": "Baruch Spinoza",
        "categoria": "Emoción y Tiempo"
    },
    {
        "texto": "La imaginación gobierna el mundo.",
        "autor": "Napoleón Bonaparte",
        "categoria": "Imaginación"
    },
    {
        "texto": "La belleza perece en la vida, pero es inmortal en el arte.",
        "autor": "Leonardo da Vinci",
        "categoria": "Arte y Belleza"
    },
    {
        "texto": "La libertad es aquella facultad que aumenta la utilidad de todas las demás facultades.",
        "autor": "Immanuel Kant",
        "categoria": "Libertad"
    },
    {
        "texto": "El ignorante afirma, el sabio duda y reflexiona.",
        "autor": "Aristóteles",
        "categoria": "Sabiduría"
    },
    {
        "texto": "La injusticia en cualquier parte es una amenaza para la justicia en todas partes.",
        "autor": "Martin Luther King Jr.",
        "categoria": "Justicia"
    },
    {
        "texto": "La mente es como un paracaídas; sólo funciona si se abre.",
        "autor": "Frank Zappa",
        "categoria": "Mentalidad"
    },
    {
        "texto": "El tiempo es la imagen móvil de la eternidad inmóvil.",
        "autor": "Platón",
        "categoria": "Tiempo"
    },
    {
        "texto": "La primera virtud del conocimiento es la capacidad de enfrentarse a lo que no es evidente.",
        "autor": "Jacques Derrida",
        "categoria": "Conocimiento"
    },
    {
        "texto": "La muerte no nos roba los seres amados. Al contrario, nos los guarda y nos los inmortaliza en el recuerdo.",
        "autor": "Jean-Paul Sartre",
        "categoria": "Muerte y Memoria"
    },
    {
        "texto": "Si no actúas como piensas, terminarás pensando como actúas.",
        "autor": "Blaise Pascal",
        "categoria": "Coherencia"
    },
    {
        "texto": "La casualidad no existe; lo que llamamos casualidad es el efecto de una causa que no conocemos.",
        "autor": "Voltaire",
        "categoria": "Causalidad"
    },
    {
        "texto": "La paciencia es amarga, pero su fruto es dulce.",
        "autor": "Jean-Jacques Rousseau",
        "categoria": "Paciencia"
    },
    {
        "texto": "La envidia es una declaración de inferioridad.",
        "autor": "Napoleón Bonaparte",
        "categoria": "Emoción"
    },
    {
        "texto": "La duda es el principio de la sabiduría.",
        "autor": "Aristóteles",
        "categoria": "Sabiduría"
    },
    {
        "texto": "La verdadera felicidad está en la libertad y en la realización de las propias capacidades.",
        "autor": "Aristóteles",
        "categoria": "Felicidad"
    },
    {
        "texto": "El hombre es la medida de todas las cosas.",
        "autor": "Protágoras",
        "categoria": "Humanismo"
    },
    {
        "texto": "La filosofía es la lucha contra el hechizo de nuestro entendimiento por medio del lenguaje.",
        "autor": "Ludwig Wittgenstein",
        "categoria": "Filosofía"
    }
]
# TUS PELÍCULAS FAVORITAS
TUS_PELICULAS = [
    {"titulo": "El Lobo de Wall Street", "tema": "Ambición, Dinero"},
    {"titulo": "Scarface", "tema": "Poder, Caída"},
    {"titulo": "La Red Social", "tema": "Innovación, Creación"},
    {"titulo": "La Gran Apuesta", "tema": "Finanzas, Riesgo"},
    {"titulo": "En Busca de la Felicidad", "tema": "Perseverancia"},
    {"titulo": "Whiplash", "tema": "Excelencia, Obsesión"},
    {"titulo": "The Founder", "tema": "Emprendimiento"},
    {"titulo": "El Aprendiz", "tema": "Aprendizaje"},
    {"titulo": "Rocky", "tema": "Determinación"},
    {"titulo": "Air", "tema": "Negociación, Visión"}
]

# TU HISTORIA CRONOLÓGICA
TU_HISTORIA = [
    {
        "año": "2009",
        "titulo": "Llegada al Mundo",
        "descripcion": "22 de diciembre - Nathán Pérez nace en Boca de Camarioca",
        "icono": "👶",
        "color": "#3B82F6",
        "tipo": "personal"
    },
    {
        "año": "2019",
        "titulo": "Primer Contacto con el Código",
        "descripcion": "10 años - Reversing de aplicaciones Android, primeros pasos en Smali",
        "icono": "📱",
        "color": "#10B981",
        "tipo": "tecnologia"
    },
    {
        "año": "2020",
        "titulo": "Comunidad Telegram y Python",
        "descripcion": "11 años - Entra a comunidad S3, aprende Python y desarrollo de bots",
        "icono": "🤖",
        "color": "#6366F1",
        "tipo": "comunidad"
    },
    {
        "año": "2021",
        "titulo": "Éxito y Caída de toDus S3",
        "descripcion": "Canal de 2000+ seguidores, fin de una era gratuita",
        "icono": "📉",
        "color": "#EF4444",
        "tipo": "aprendizaje"
    },
    {
        "año": "2021-2022",
        "titulo": "Emprendimiento con Moodles",
        "descripcion": "Bots educativos, primer dinero ganado, inicio del amor por las finanzas",
        "icono": "💰",
        "color": "#F59E0B",
        "tipo": "negocios"
    },
    {
        "año": "2022",
        "titulo": "Reparación de Hardware",
        "descripcion": "12-13 años - Trabajo en taller, habilidades técnicas",
        "icono": "🔧",
        "color": "#8B5CF6",
        "tipo": "tecnologia"
    },
    {
        "año": "2023",
        "titulo": "Experiencia Transformadora",
        "descripcion": "La Esperanza, Villa Clara - Aprendizaje forzado, psicología aplicada",
        "icono": "⚡",
        "color": "#06B6D4",
        "tipo": "crecimiento"
    },
    {
        "año": "2023-2024",
        "titulo": "Renacimiento Digital",
        "descripcion": "Regreso a Boca de Camarioca, aprendizaje con Alejandro y Javier",
        "icono": "🚀",
        "color": "#EC4899",
        "tipo": "renacimiento"
    },
    {
        "año": "Presente",
        "titulo": "Búsqueda de Excelencia",
        "descripcion": "Desarrollo web, aplicaciones Android, constante evolución",
        "icono": "🎯",
        "color": "#84CC16",
        "tipo": "futuro"
    }
]

# TUS HABILIDADES
TUS_HABILIDADES = {
    "lenguajes": [
        {"nombre": "Python", "nivel": 95, "color": "#3776AB", "icono": "🐍", "experiencia": "4 años"},
        {"nombre": "Kotlin", "nivel": 80, "color": "#7F52FF", "icono": "⚡", "experiencia": "2 años"},
        {"nombre": "Java", "nivel": 85, "color": "#007396", "icono": "☕", "experiencia": "3 años"},
        {"nombre": "JavaScript", "nivel": 75, "color": "#F7DF1E", "icono": "📜", "experiencia": "3 años"},
        {"nombre": "Visual Basic", "nivel": 70, "color": "#00599C", "icono": "👁️", "experiencia": "3 años"}
    ],
    "habilidades_personales": [
        {"nombre": "Lógica", "nivel": 90, "color": "#3B82F6"},
        {"nombre": "Fuerza de Voluntad", "nivel": 95, "color": "#10B981"},
        {"nombre": "Aprendizaje Autónomo", "nivel": 92, "color": "#8B5CF6"},
        {"nombre": "Pensamiento Crítico", "nivel": 88, "color": "#EC4899"},
        {"nombre": "Adaptabilidad", "nivel": 85, "color": "#F59E0B"}
    ]
}

# TUS INTERESES
TUS_PASIONES = [
    {"nombre": "Lógica", "desc": "Resolver problemas, patrones, pensamiento estructurado", "icono": "🧠", "color": "#3B82F6"},
    {"nombre": "Filosofía", "desc": "Reflexión, significado, preguntas existenciales", "icono": "📜", "color": "#8B5CF6"},
    {"nombre": "Matemáticas", "desc": "Precisión, belleza numérica, patrones", "icono": "π", "color": "#10B981"},
    {"nombre": "Tecnología", "desc": "Innovación, creación, futuro", "icono": "💻", "color": "#6366F1"},
    {"nombre": "Música", "desc": "Todos los géneros excepto rock", "icono": "🎵", "color": "#EC4899"},
    {"nombre": "Fútbol", "desc": "Jugar, no ver", "icono": "⚽", "color": "#84CC16"},
    {"nombre": "Cine", "desc": "Películas con mensaje", "icono": "🎬", "color": "#F59E0B"},
    {"nombre": "Finanzas", "desc": "Dinero, inversión, negocios", "icono": "💰", "color": "#06B6D4"}
]

# ========== FUNCIONES ==========
def get_theme():
    return session.get('theme', 'light')

def obtener_frase_nathan():
    return random.choice(FRASES_NATHAN)

def load_posts():
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
            # Agregar categorías si no existen
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
    frase = obtener_frase_nathan()
    return render_template('index.html',
                         perfil=NATHAN_PERFIL,
                         frase=frase,
                         habilidades=TUS_HABILIDADES,
                         peliculas=TUS_PELICULAS[:5],
                         theme=theme)

@app.route('/historia')
def historia():
    theme = get_theme()
    return render_template('historia.html',
                         perfil=NATHAN_PERFIL,
                         historia=TU_HISTORIA,
                         habilidades=TUS_HABILIDADES,
                         theme=theme)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    theme = get_theme()
    success = False
    
    if request.method == 'POST':
        # Aquí guardarías el mensaje
        success = True
    
    return render_template('contact.html', success=success, perfil=NATHAN_PERFIL, theme=theme)

@app.route('/api/frase')
def api_frase():
    return jsonify(obtener_frase_nathan())

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
                "fecha": "2024-01-20",
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
                "fecha": "2024-01-18",
                "categoria": "Lógica",
                "etiquetas": ["lógica", "programación", "pensamiento"],
                "tiempo_lectura": "4 min",
                "imagen": "logica.jpg"
            },
            {
                "id": 3,
                "titulo": "De Boca de Camarioca al Mundo Digital",
                "contenido": """<h2>Creciendo entre la playa y el código</h2>
                <p>Ser de un pueblo pequeño no es limitación cuando tienes internet...</p>""",
                "resumen": "Mi experiencia creciendo como desarrollador en Cuba",
                "fecha": "2024-01-15",
                "categoria": "Personal",
                "etiquetas": ["cuba", "crecimiento", "tecnología"],
                "tiempo_lectura": "6 min",
                "imagen": "cuba.jpg"
            }
        ]
        with open('data/posts.json', 'w', encoding='utf-8') as f:
            json.dump(initial_posts, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    init_data()
    app.run(host="0.0.0.0",debug=True, port=5000)