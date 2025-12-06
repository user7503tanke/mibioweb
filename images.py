#!/usr/bin/env python3
"""
Script para generar imágenes de placeholder para el portafolio
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import json

# Colores para los placeholders
COLOR_PALETTES = {
    "primary": ["#667EEA", "#764BA2", "#F093FB", "#F5576C"],
    "tech": ["#3776AB", "#007396", "#7F52FF", "#F7DF1E", "#000000", "#E34F26"],
    "gradients": [
        ("#667EEA", "#764BA2"),
        ("#F093FB", "#F5576C"),
        ("#4CAF50", "#8BC34A"),
        ("#FF9800", "#FFC107"),
        ("#2196F3", "#21CBF3")
    ]
}

# Textos para las imágenes
TECH_TEXTS = [
    "Python", "Java", "Kotlin", "Flask", "Android", "Web",
    "API", "Database", "Frontend", "Backend", "Mobile", "Cloud"
]

ICONS = ["💻", "📱", "🌐", "🔧", "⚡", "🎨", "📊", "🗄️", "🤖", "🔒"]

def create_gradient(width, height, colors):
    """Crear una imagen con gradiente"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    for i in range(height):
        ratio = i / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    return image

def hex_to_rgb(hex_color):
    """Convertir hex a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_tech_image(width, height, text, icon=None):
    """Crear imagen para tecnología"""
    # Elegir colores aleatorios
    bg_gradient = random.choice(COLOR_PALETTES["gradients"])
    bg_colors = [hex_to_rgb(bg_gradient[0]), hex_to_rgb(bg_gradient[1])]
    
    image = create_gradient(width, height, bg_colors)
    draw = ImageDraw.Draw(image)
    
    try:
        # Intentar cargar fuente
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        # Fuente por defecto si no hay arial
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Dibujar icono si existe
    if icon:
        # Para emojis necesitarías una fuente que los soporte
        # Por ahora usamos texto simple
        draw.text((width//2, height//2 - 30), icon, font=font_large, 
                  fill=(255, 255, 255), anchor="mm")
    
    # Dibujar texto
    draw.text((width//2, height//2 + 30), text, font=font_small, 
              fill=(255, 255, 255), anchor="mm")
    
    return image

def create_project_image(width, height, project_name):
    """Crear imagen para proyecto"""
    # Gradiente de fondo
    bg_gradient = random.choice(COLOR_PALETTES["gradients"])
    bg_colors = [hex_to_rgb(bg_gradient[0]), hex_to_rgb(bg_gradient[1])]
    
    image = create_gradient(width, height, bg_colors)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    # Dibujar líneas de "código"
    for i in range(5):
        y = 50 + i * 40
        line_length = random.randint(100, width - 200)
        draw.rectangle([100, y, 100 + line_length, y + 20], 
                      fill=(255, 255, 255, 50))
    
    # Dibujar nombre del proyecto
    draw.text((width//2, height - 100), project_name, font=font, 
              fill=(255, 255, 255), anchor="mm")
    
    # Dibujar decoración
    draw.rectangle([50, 50, width - 50, height - 150], 
                  outline=(255, 255, 255, 100), width=2)
    
    return image

def create_avatar(size):
    """Crear avatar placeholder"""
    image = Image.new('RGB', (size, size), color=hex_to_rgb("#667EEA"))
    draw = ImageDraw.Draw(image)
    
    # Dibujar círculo para la cabeza
    margin = size // 10
    draw.ellipse([margin, margin, size - margin, size - margin], 
                fill=(255, 255, 255))
    
    # Dibujar cuerpo
    body_top = size // 2 + margin
    body_points = [
        (size//2, body_top),
        (size//4, size - margin),
        (3*size//4, size - margin)
    ]
    draw.polygon(body_points, fill=(255, 255, 255))
    
    # Dibujar iniciales
    try:
        font = ImageFont.truetype("arial.ttf", size//3)
    except:
        font = ImageFont.load_default()
    
    draw.text((size//2, size//3), "TN", font=font, 
              fill=hex_to_rgb("#667EEA"), anchor="mm")
    
    return image

def generate_all_images():
    """Generar todas las imágenes necesarias"""
    
    # Crear directorios
    os.makedirs("static/images/projects", exist_ok=True)
    os.makedirs("static/images/blog", exist_ok=True)
    os.makedirs("static/images/tech", exist_ok=True)
    
    print("Generando imágenes...")
    
    # 1. Avatar
    avatar = create_avatar(400)
    avatar.save("static/images/avatar.jpg", quality=95)
    print("✓ Avatar generado")
    
    # 2. Imágenes de proyectos
    projects = [
        "Sistema de Bots Telegram",
        "App de Gestión para Taller", 
        "Portafolio Personal",
        "Plataforma Educativa",
        "Android Reversing Tool",
        "API de Servicios"
    ]
    
    for i, project in enumerate(projects, 1):
        img = create_project_image(800, 400, project)
        img.save(f"static/images/projects/project{i}.jpg", quality=90)
        print(f"✓ Imagen proyecto {i}: {project}")
    
    # 3. Imágenes de blog
    blog_posts = [
        "Mi Viaje en Android",
        "Python: Mi Lenguaje Favorito",
        "Lecciones de Emprendimiento",
        "Desarrollo Web Moderno",
        "Seguridad en Aplicaciones"
    ]
    
    for i, post in enumerate(blog_posts, 1):
        img = create_project_image(800, 400, post)
        img.save(f"static/images/blog/post{i}.jpg", quality=90)
        print(f"✓ Imagen blog {i}: {post}")
    
    # 4. Imágenes de tecnologías
    for i, tech in enumerate(TECH_TEXTS[:10], 1):
        icon = ICONS[i % len(ICONS)] if i <= len(ICONS) else None
        img = create_tech_image(400, 300, tech, icon)
        img.save(f"static/images/tech/tech{i}.jpg", quality=90)
        print(f"✓ Imagen tecnología {i}: {tech}")
    
    # 5. Imágenes de fondo
    for i in range(3):
        colors = random.choice(COLOR_PALETTES["gradients"])
        bg_colors = [hex_to_rgb(colors[0]), hex_to_rgb(colors[1])]
        img = create_gradient(1200, 600, bg_colors)
        img.save(f"static/images/background{i}.jpg", quality=90)
        print(f"✓ Fondo {i} generado")
    
    print("\n✅ Todas las imágenes han sido generadas exitosamente!")
    print("📁 Directorios creados:")
    print("   static/images/avatar.jpg")
    print("   static/images/projects/ (6 imágenes)")
    print("   static/images/blog/ (5 imágenes)")
    print("   static/images/tech/ (10 imágenes)")
    print("   static/images/background*.jpg (3 imágenes)")

def create_simple_placeholders():
    """Crear placeholders SVG simples si no se puede usar PIL"""
    
    os.makedirs("static/images", exist_ok=True)
    
    # Avatar SVG
    avatar_svg = '''<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="avatarGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#667EEA"/>
                <stop offset="100%" stop-color="#764BA2"/>
            </linearGradient>
        </defs>
        <rect width="400" height="400" fill="url(#avatarGrad)" rx="20"/>
        <circle cx="200" cy="150" r="60" fill="white"/>
        <path d="M200 230 Q140 350 260 350 Q380 350 200 230Z" fill="white"/>
        <text x="200" y="140" text-anchor="middle" font-family="Arial" font-size="48" font-weight="bold" fill="#667EEA">TN</text>
    </svg>'''
    
    with open("static/images/avatar.svg", "w") as f:
        f.write(avatar_svg)
    
    print("✓ Placeholders SVG creados")
    print("⚠️  Nota: Para mejores imágenes, instala Pillow: pip install Pillow")
    print("   y ejecuta: python generate_images.py")

if __name__ == "__main__":
    try:
        from PIL import Image
        generate_all_images()
    except ImportError:
        print("Pillow no está instalado. Creando placeholders SVG...")
        create_simple_placeholders()
    except Exception as e:
        print(f"Error: {e}")
        create_simple_placeholders()