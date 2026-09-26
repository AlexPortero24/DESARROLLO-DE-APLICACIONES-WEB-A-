from flask import Flask, render_template, redirect, url_for, flash, request

# Importar formularios de la carpeta forms para la Semana 11
from forms.cliente_form import ClienteForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# Configuración obligatoria de la SECRET_KEY para permitir la protección CSRF en los formularios
app.config['SECRET_KEY'] = 'acuario_vaporeon_secret_key_2026'

# Listas principales unificadas para el CRUD completo en todos los módulos
lista_clientes = [
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

lista_productos = [
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

lista_proveedores = [
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

lista_facturas = [
    {
        "id": 1,
        "numero": "001",
        "cliente": "Ana Martínez",
        "fecha": "2026-08-15",
        "total": 150.00
    },
    {
        "id": 2,
        "numero": "002",
        "cliente": "Carlos López",
        "fecha": "2026-08-16",
        "total": 230.00
    },
    {
        "id": 3,
        "numero": "003",
        "cliente": "María Gómez",
        "fecha": "2026-08-16",
        "total": 85.00
    }
]


# ==========================================================
# PÁGINA DE INICIO
# ==========================================================
@app.route('/')
def index():
    nombre_negocio = "Acuario Vaporeon"
    return render_template(
        'index.html',
        nombre_negocio=nombre_negocio
    )


# ==========================================================
# MÓDULO DE PRODUCTOS (CRUD Completo)
# ==========================================================
@app.route('/productos')
def productos():
    return render_template(
        'productos.html',
        productos=lista_productos
    )

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_id = max([p['id'] for p in lista_productos], default=0) + 1
        producto = {
            'id': nuevo_id,
            'nombre': form.nombre.data,
            'precio': form.precio.data,
            'stock': form.stock.data
        }
        lista_productos.append(producto)
        flash('¡Producto guardado y validado correctamente!', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form)

@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    producto_encontrado = None
    for p in lista_productos:
        if p['id'] == id_producto:
            producto_encontrado = p
            break

    if not producto_encontrado:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos'))

    form = ProductoForm(data=producto_encontrado)

    if form.validate_on_submit():
        producto_encontrado['nombre'] = form.nombre.data
        producto_encontrado['precio'] = form.precio.data
        producto_encontrado['stock'] = form.stock.data
        flash('¡Producto actualizado correctamente!', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form, editando=True)

@app.route('/productos/eliminar/<int:id_producto>')
def eliminar_producto(id_producto):
    global lista_productos
    lista_productos = [p for p in lista_productos if p['id'] != id_producto]
    flash('¡Producto eliminado correctamente!', 'danger')
    return redirect(url_for('productos'))


# ==========================================================
# MÓDULO DE CLIENTES (CRUD Completo)
# ==========================================================
@app.route('/clientes')
def clientes():
    return render_template(
        'clientes.html',
        clientes=lista_clientes
    )

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_id = max([c['id'] for c in lista_clientes], default=0) + 1
        cliente = {
            'id': nuevo_id,
            'nombre': form.nombre.data,
            'email': form.email.data,
            'telefono': form.telefono.data
        }
        lista_clientes.append(cliente)
        flash('¡Cliente guardado y validado correctamente!', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form)

@app.route('/clientes/editar/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):
    cliente_encontrado = None
    for c in lista_clientes:
        if c['id'] == id_cliente:
            cliente_encontrado = c
            break

    if not cliente_encontrado:
        flash('Cliente no encontrado.', 'danger')
        return redirect(url_for('clientes'))

    form = ClienteForm(data=cliente_encontrado)

    if form.validate_on_submit():
        cliente_encontrado['nombre'] = form.nombre.data
        cliente_encontrado['email'] = form.email.data
        cliente_encontrado['telefono'] = form.telefono.data
        flash('¡Cliente actualizado correctamente!', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form, editando=True)

@app.route('/clientes/eliminar/<int:id_cliente>')
def eliminar_cliente(id_cliente):
    global lista_clientes
    lista_clientes = [c for c in lista_clientes if c['id'] != id_cliente]
    flash('¡Cliente eliminado correctamente!', 'danger')
    return redirect(url_for('clientes'))


# ==========================================================
# MÓDULO DE PROVEEDORES (CRUD Completo)
# ==========================================================
@app.route('/proveedores')
def proveedores():
    return render_template(
        'proveedores.html',
        proveedores=lista_proveedores
    )

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_id = max([p['id'] for p in lista_proveedores], default=0) + 1
        proveedor = {
            'id': nuevo_id,
            'nombre': form.nombre.data,
            'contacto': form.contacto.data,
            'telefono': form.telefono.data
        }
        lista_proveedores.append(proveedor)
        flash('¡Proveedor guardado y validado correctamente!', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form)

@app.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
def editar_proveedor(id_proveedor):
    proveedor_encontrado = None
    for p in lista_proveedores:
        if p['id'] == id_proveedor:
            proveedor_encontrado = p
            break

    if not proveedor_encontrado:
        flash('Proveedor no encontrado.', 'danger')
        return redirect(url_for('proveedores'))

    form = ProveedorForm(data=proveedor_encontrado)

    if form.validate_on_submit():
        proveedor_encontrado['nombre'] = form.nombre.data
        proveedor_encontrado['contacto'] = form.contacto.data
        proveedor_encontrado['telefono'] = form.telefono.data
        flash('¡Proveedor actualizado correctamente!', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form, editando=True)

@app.route('/proveedores/eliminar/<int:id_proveedor>')
def eliminar_proveedor(id_proveedor):
    global lista_proveedores
    lista_proveedores = [p for p in lista_proveedores if p['id'] != id_proveedor]
    flash('¡Proveedor eliminado correctamente!', 'danger')
    return redirect(url_for('proveedores'))


# ==========================================================
# MÓDULO DE FACTURACIÓN (CRUD Completo)
# ==========================================================
@app.route('/facturacion')
def facturacion():
    return render_template(
        'facturacion.html',
        facturas=lista_facturas
    )

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_factura():
    form = FacturacionForm()
    if form.validate_on_submit():
        nuevo_id = max([f['id'] for f in lista_facturas], default=0) + 1
        factura = {
            'id': nuevo_id,
            'numero': form.numero.data,
            'cliente': form.cliente.data,
            'fecha': str(form.fecha.data),
            'total': form.total.data
        }
        lista_facturas.append(factura)
        flash('¡Factura guardada y validada correctamente!', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form)

@app.route('/facturacion/editar/<int:id_factura>', methods=['GET', 'POST'])
def editar_factura(id_factura):
    factura_encontrada = None
    for f in lista_facturas:
        if f['id'] == id_factura:
            factura_encontrada = f
            break

    if not factura_encontrada:
        flash('Factura no encontrada.', 'danger')
        return redirect(url_for('facturacion'))

    form = FacturacionForm(data=factura_encontrada)

    if form.validate_on_submit():
        factura_encontrada['numero'] = form.numero.data
        factura_encontrada['cliente'] = form.cliente.data
        factura_encontrada['fecha'] = str(form.fecha.data)
        factura_encontrada['total'] = form.total.data
        flash('¡Factura actualizada correctamente!', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form, editando=True)

@app.route('/facturacion/eliminar/<int:id_factura>')
def eliminar_factura(id_factura):
    global lista_facturas
    lista_facturas = [f for f in lista_facturas if f['id'] != id_factura]
    flash('¡Factura eliminada correctamente!', 'danger')
    return redirect(url_for('facturacion'))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)