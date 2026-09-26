from flask import Flask, render_template

app = Flask(__name__)


# ==========================================================
# PÁGINA DE INICIO
# ==========================================================
@app.route('/')
def index():

    # Variable simple para mostrar contenido dinámico con Jinja2
    nombre_negocio = "Acuario Vaporeon"

    return render_template(
        'index.html',
        nombre_negocio=nombre_negocio
    )


# ==========================================================
# MÓDULO DE PRODUCTOS
# ==========================================================
@app.route('/productos')
def productos():

    # Lista de productos.
    # Cada elemento es un diccionario con información del producto.
    productos = [
        {
            "id": 1,
            "nombre": "Pez Betta",
            "precio": 15.00,
            "stock": 10
        },
        {
            "id": 2,
            "nombre": "Pez Guppy",
            "precio": 8.00,
            "stock": 25
        },
        {
            "id": 3,
            "nombre": "Pez Goldfish",
            "precio": 12.00,
            "stock": 8
        },
        {
            "id": 4,
            "nombre": "Pez Molly",
            "precio": 10.00,
            "stock": 0
        }
    ]

    return render_template(
        'productos.html',
        productos=productos
    )


# ==========================================================
# MÓDULO DE CLIENTES
# ==========================================================
@app.route('/clientes')
def clientes():

    # Lista temporal de clientes.
    clientes = [
        {
            "id": 1,
            "nombre": "Ana Martínez",
            "email": "ana@email.com",
            "telefono": "0987654321"
        },
        {
            "id": 2,
            "nombre": "Carlos López",
            "email": "carlos@email.com",
            "telefono": "0987123456"
        },
        {
            "id": 3,
            "nombre": "María Gómez",
            "email": "maria@email.com",
            "telefono": "0987567890"
        }
    ]

    return render_template(
        'clientes.html',
        clientes=clientes
    )


# ==========================================================
# MÓDULO DE PROVEEDORES
# ==========================================================
@app.route('/proveedores')
def proveedores():

    # Lista temporal de proveedores.
    proveedores = [
        {
            "id": 1,
            "nombre": "Proveedor X",
            "contacto": "Juan Pérez",
            "telefono": "0987000111"
        },
        {
            "id": 2,
            "nombre": "Proveedor Y",
            "contacto": "Luis Torres",
            "telefono": "0987000222"
        },
        {
            "id": 3,
            "nombre": "Proveedor Z",
            "contacto": "Elena Ruiz",
            "telefono": "0987000333"
        }
    ]

    return render_template(
        'proveedores.html',
        proveedores=proveedores
    )


# ==========================================================
# MÓDULO DE FACTURACIÓN
# ==========================================================
@app.route('/facturacion')
def facturacion():

    # Lista temporal de facturas.
    facturas = [
        {
            "numero": "001",
            "cliente": "Ana Martínez",
            "fecha": "2026-08-15",
            "total": 150.00
        },
        {
            "numero": "002",
            "cliente": "Carlos López",
            "fecha": "2026-08-16",
            "total": 230.00
        },
        {
            "numero": "003",
            "cliente": "María Gómez",
            "fecha": "2026-08-16",
            "total": 85.00
        }
    ]

    return render_template(
        'facturacion.html',
        facturas=facturas
    )


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)

