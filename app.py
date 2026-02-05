from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Datos del negocio (puedes cambiar estos valores)
BUSINESS_INFO = {
    "nombre": "CellFix Santa Marta",
    "telefono": "59642359",
    "whatsapp": "5359642359",  # código de Cuba +53
    "horario": "Lunes a Sábado: 9:00 AM - 5:00 PM",
    "ubicacion": "Santa Marta, Matanzas, Cuba",
    "slogan": "Tu celular en las mejores manos",
    "garantia": "7 días de garantía en todos nuestros servicios"
}

SERVICIOS = [
    {
        "titulo": "Cambio de Pantallas",
        "descripcion": "Reparamos pantallas de todas las marcas: iPhone, Samsung, Xiaomi, Huawei, LG, Motorola y más. Pantallas originales y de alta calidad.",
        "tiempo": "1-2 horas",
        "icono": "📱"
    },
    {
        "titulo": "Reparación de Pines de Carga",
        "descripcion": "Solucionamos problemas de carga, puertos dañados y conectores. Recupera la carga rápida de tu dispositivo.",
        "tiempo": "1 hora",
        "icono": "⚡"
    },
    {
        "titulo": "Cambio de Baterías",
        "descripcion": "Baterías nuevas con máxima duración. Diagnóstico gratuito de salud de batería.",
        "tiempo": "45 minutos",
        "icono": "🔋"
    },
    {
        "titulo": "Desbloqueos Complejos",
        "descripcion": "Especialistas en: FRP, MDM, iCloud, cuenta MI, bloqueo de red, KG y todo tipo de desbloqueos.",
        "tiempo": "2-4 horas",
        "icono": "🔓"
    },
    {
        "titulo": "Reparaciones Generales",
        "descripcion": "Módulos de cámara, botones, altavoces, micrófonos, conectores de audio y más.",
        "tiempo": "1-3 horas",
        "icono": "🔧"
    },
    {
        "titulo": "Conversión eSIM a SIM Física",
        "descripcion": "Servicio exclusivo de Jamir: Convertimos iPhone eSIM a bandeja SIM física. Todo queda como de fábrica.",
        "tiempo": "30-45 minutos",
        "icono": "📲",
        "especial": True
    }
]

@app.route('/')
def home():
    return render_template('index.html', 
                         info=BUSINESS_INFO, 
                         servicios=SERVICIOS)

@app.route('/servicios')
def servicios():
    return render_template('servicios.html', 
                         info=BUSINESS_INFO, 
                         servicios=SERVICIOS)

@app.route('/contacto', methods=['POST'])
def contacto():
    if request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        telefono = data.get('telefono')
        servicio = data.get('servicio')
        mensaje = data.get('mensaje')
        
        # Aquí normalmente enviarías un email o guardarías en BD
        print(f"Nuevo contacto: {nombre}, Tel: {telefono}, Servicio: {servicio}")
        
        return jsonify({
            'success': True,
            'message': 'Mensaje recibido. Te contactaremos pronto.'
        })
    
    return jsonify({'success': False, 'message': 'Método no permitido'})

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5000)