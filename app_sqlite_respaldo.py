import os
import sqlite3

from flask import Flask, render_template, redirect, url_for, flash

# Importar formularios de la carpeta forms para la Semana 11
from forms.cliente_form import ClienteForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)


# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

# SECRET_KEY necesaria para Flask-WTF y protección CSRF
app.config['SECRET_KEY'] = 'acuario_vaporeon_secret_key_2026'


# ==========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS SQLITE
# ==========================================================

# Ruta principal del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta donde se almacenará la base de datos
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Archivo de base de datos SQLite
DATABASE = os.path.join(DATA_DIR, 'acuario_vaporeon.db')


def get_db_connection():
    """
    Crea una conexión con la base de datos SQLite.
    """

    conn = sqlite3.connect(DATABASE)

    # Permite acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    """
    Crea la carpeta data y las tablas necesarias
    si todavía no existen.
    """

    # Crear la carpeta data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)

    # Abrir conexión
    conn = get_db_connection()

    # ======================================================
    # TABLA PRODUCTOS
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # ======================================================
    # TABLA CLIENTES
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)

    # ======================================================
    # TABLA PROVEEDORES
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)

    # ======================================================
    # TABLA FACTURAS
    # ======================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            cliente TEXT NOT NULL,
            fecha TEXT NOT NULL,
            total REAL NOT NULL
        )
    """)

    # Confirmar creación de las tablas
    conn.commit()

    # Cerrar conexión
    conn.close()


# Inicializar la base de datos
init_db()


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
# MÓDULO DE PRODUCTOS
# ==========================================================

@app.route('/productos')
def productos():

    # Abrir conexión
    conn = get_db_connection()

    # Consultar productos
    productos_db = conn.execute("""
        SELECT id, nombre, precio, stock
        FROM productos
        ORDER BY id
    """).fetchall()

    # Cerrar conexión
    conn.close()

    return render_template(
        'productos.html',
        productos=productos_db
    )


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():

    form = ProductoForm()

    # Validar formulario
    if form.validate_on_submit():

        conn = get_db_connection()

        # Insertar producto
        conn.execute("""
            INSERT INTO productos (nombre, precio, stock)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.precio.data,
            form.stock.data
        ))

        # Confirmar cambios
        conn.commit()

        # Cerrar conexión
        conn.close()

        flash(
            '¡Producto guardado y validado correctamente!',
            'success'
        )

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form
    )


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):

    conn = get_db_connection()

    # Buscar producto
    producto = conn.execute("""
        SELECT id, nombre, precio, stock
        FROM productos
        WHERE id = ?
    """, (id_producto,)).fetchone()

    conn.close()

    # Comprobar si existe
    if producto is None:

        flash(
            'Producto no encontrado.',
            'danger'
        )

        return redirect(url_for('productos'))

    # Cargar datos en el formulario
    form = ProductoForm(
        data={
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'stock': producto['stock']
        }
    )

    # Validar formulario
    if form.validate_on_submit():

        conn = get_db_connection()

        # Actualizar producto
        conn.execute("""
            UPDATE productos
            SET nombre = ?, precio = ?, stock = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            id_producto
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Producto actualizado correctamente!',
            'success'
        )

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form,
        editando=True
    )


@app.route('/productos/eliminar/<int:id_producto>')
def eliminar_producto(id_producto):

    conn = get_db_connection()

    # Eliminar producto
    conn.execute("""
        DELETE FROM productos
        WHERE id = ?
    """, (id_producto,))

    conn.commit()
    conn.close()

    flash(
        '¡Producto eliminado correctamente!',
        'danger'
    )

    return redirect(url_for('productos'))


# ==========================================================
# MÓDULO DE CLIENTES
# ==========================================================

@app.route('/clientes')
def clientes():

    conn = get_db_connection()

    # Consultar clientes
    clientes_db = conn.execute("""
        SELECT id, nombre, email, telefono
        FROM clientes
        ORDER BY id
    """).fetchall()

    conn.close()

    return render_template(
        'clientes.html',
        clientes=clientes_db
    )


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = get_db_connection()

        # Insertar cliente
        conn.execute("""
            INSERT INTO clientes (nombre, email, telefono)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.email.data,
            form.telefono.data
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Cliente guardado y validado correctamente!',
            'success'
        )

        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        form=form
    )


@app.route('/clientes/editar/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):

    conn = get_db_connection()

    # Buscar cliente
    cliente = conn.execute("""
        SELECT id, nombre, email, telefono
        FROM clientes
        WHERE id = ?
    """, (id_cliente,)).fetchone()

    conn.close()

    # Comprobar si existe
    if cliente is None:

        flash(
            'Cliente no encontrado.',
            'danger'
        )

        return redirect(url_for('clientes'))

    # Cargar datos actuales
    form = ClienteForm(
        data={
            'nombre': cliente['nombre'],
            'email': cliente['email'],
            'telefono': cliente['telefono']
        }
    )

    if form.validate_on_submit():

        conn = get_db_connection()

        # Actualizar cliente
        conn.execute("""
            UPDATE clientes
            SET nombre = ?, email = ?, telefono = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.email.data,
            form.telefono.data,
            id_cliente
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Cliente actualizado correctamente!',
            'success'
        )

        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        form=form,
        editando=True
    )


@app.route('/clientes/eliminar/<int:id_cliente>')
def eliminar_cliente(id_cliente):

    conn = get_db_connection()

    # Eliminar cliente
    conn.execute("""
        DELETE FROM clientes
        WHERE id = ?
    """, (id_cliente,))

    conn.commit()
    conn.close()

    flash(
        '¡Cliente eliminado correctamente!',
        'danger'
    )

    return redirect(url_for('clientes'))


# ==========================================================
# MÓDULO DE PROVEEDORES
# ==========================================================

@app.route('/proveedores')
def proveedores():

    conn = get_db_connection()

    # Consultar proveedores
    proveedores_db = conn.execute("""
        SELECT id, nombre, contacto, telefono
        FROM proveedores
        ORDER BY id
    """).fetchall()

    conn.close()

    return render_template(
        'proveedores.html',
        proveedores=proveedores_db
    )


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = get_db_connection()

        # Insertar proveedor
        conn.execute("""
            INSERT INTO proveedores (nombre, contacto, telefono)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.contacto.data,
            form.telefono.data
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Proveedor guardado y validado correctamente!',
            'success'
        )

        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        form=form
    )


@app.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
def editar_proveedor(id_proveedor):

    conn = get_db_connection()

    # Buscar proveedor
    proveedor = conn.execute("""
        SELECT id, nombre, contacto, telefono
        FROM proveedores
        WHERE id = ?
    """, (id_proveedor,)).fetchone()

    conn.close()

    # Comprobar si existe
    if proveedor is None:

        flash(
            'Proveedor no encontrado.',
            'danger'
        )

        return redirect(url_for('proveedores'))

    # Cargar datos actuales
    form = ProveedorForm(
        data={
            'nombre': proveedor['nombre'],
            'contacto': proveedor['contacto'],
            'telefono': proveedor['telefono']
        }
    )

    if form.validate_on_submit():

        conn = get_db_connection()

        # Actualizar proveedor
        conn.execute("""
            UPDATE proveedores
            SET nombre = ?, contacto = ?, telefono = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.contacto.data,
            form.telefono.data,
            id_proveedor
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Proveedor actualizado correctamente!',
            'success'
        )

        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        form=form,
        editando=True
    )


@app.route('/proveedores/eliminar/<int:id_proveedor>')
def eliminar_proveedor(id_proveedor):

    conn = get_db_connection()

    # Eliminar proveedor
    conn.execute("""
        DELETE FROM proveedores
        WHERE id = ?
    """, (id_proveedor,))

    conn.commit()
    conn.close()

    flash(
        '¡Proveedor eliminado correctamente!',
        'danger'
    )

    return redirect(url_for('proveedores'))


# ==========================================================
# MÓDULO DE FACTURACIÓN
# ==========================================================

@app.route('/facturacion')
def facturacion():

    conn = get_db_connection()

    # Consultar facturas
    facturas_db = conn.execute("""
        SELECT id, numero, cliente, fecha, total
        FROM facturas
        ORDER BY id
    """).fetchall()

    conn.close()

    return render_template(
        'facturacion.html',
        facturas=facturas_db
    )


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = get_db_connection()

        # Insertar factura
        conn.execute("""
            INSERT INTO facturas (numero, cliente, fecha, total)
            VALUES (?, ?, ?, ?)
        """, (
            form.numero.data,
            form.cliente.data,
            str(form.fecha.data),
            form.total.data
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Factura guardada y validada correctamente!',
            'success'
        )

        return redirect(url_for('facturacion'))

    return render_template(
        'formulario_facturacion.html',
        form=form
    )


@app.route('/facturacion/editar/<int:id_factura>', methods=['GET', 'POST'])
def editar_factura(id_factura):

    conn = get_db_connection()

    # Buscar factura
    factura = conn.execute("""
        SELECT id, numero, cliente, fecha, total
        FROM facturas
        WHERE id = ?
    """, (id_factura,)).fetchone()

    conn.close()

    # Comprobar si existe
    if factura is None:

        flash(
            'Factura no encontrada.',
            'danger'
        )

        return redirect(url_for('facturacion'))

    # Cargar datos actuales
    form = FacturacionForm(
        data={
            'numero': factura['numero'],
            'cliente': factura['cliente'],
            'fecha': factura['fecha'],
            'total': factura['total']
        }
    )

    if form.validate_on_submit():

        conn = get_db_connection()

        # Actualizar factura
        conn.execute("""
            UPDATE facturas
            SET numero = ?, cliente = ?, fecha = ?, total = ?
            WHERE id = ?
        """, (
            form.numero.data,
            form.cliente.data,
            str(form.fecha.data),
            form.total.data,
            id_factura
        ))

        conn.commit()
        conn.close()

        flash(
            '¡Factura actualizada correctamente!',
            'success'
        )

        return redirect(url_for('facturacion'))

    return render_template(
        'formulario_facturacion.html',
        form=form,
        editando=True
    )


@app.route('/facturacion/eliminar/<int:id_factura>')
def eliminar_factura(id_factura):

    conn = get_db_connection()

    # Eliminar factura
    conn.execute("""
        DELETE FROM facturas
        WHERE id = ?
    """, (id_factura,))

    conn.commit()
    conn.close()

    flash(
        '¡Factura eliminada correctamente!',
        'danger'
    )

    return redirect(url_for('facturacion'))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == '__main__':
    app.run(debug=True)
