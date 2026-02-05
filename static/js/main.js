// Manejo del formulario de contacto
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const nombre = document.getElementById('nombre').value;
            const telefono = document.getElementById('telefono').value;
            const servicio = document.getElementById('servicio').value;
            const mensaje = document.getElementById('mensaje').value;
            
            // Validación básica
            if (!nombre || !telefono || !servicio) {
                showMessage('Por favor complete todos los campos requeridos', 'danger');
                return;
            }
            
            // Mostrar mensaje de procesando
            showMessage('Enviando consulta...', 'info');
            
            try {
                const response = await fetch('/contacto', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        nombre: nombre,
                        telefono: telefono,
                        servicio: servicio,
                        mensaje: mensaje
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage(data.message, 'success');
                    contactForm.reset();
                    
                    // Redirigir a WhatsApp después de 2 segundos
                    setTimeout(() => {
                        const whatsappUrl = `https://wa.me/5359642359?text=Hola,%20soy%20${encodeURIComponent(nombre)}.%20Consulté%20por:%20${encodeURIComponent(servicio)}.%20${mensaje ? encodeURIComponent('Detalles: ' + mensaje) : ''}`;
                        window.open(whatsappUrl, '_blank');
                    }, 2000);
                } else {
                    showMessage(data.message || 'Error al enviar el formulario', 'danger');
                }
            } catch (error) {
                showMessage('Error de conexión. Por favor, use WhatsApp directamente.', 'danger');
            }
        });
    }
    
    function showMessage(text, type) {
        formMessage.textContent = text;
        formMessage.className = `alert alert-${type} mt-3`;
        formMessage.style.display = 'block';
        
        // Ocultar mensaje después de 5 segundos
        if (type !== 'info') {
            setTimeout(() => {
                formMessage.style.display = 'none';
            }, 5000);
        }
    }
    
    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});