from flask import Flask, render_template, redirect, url_for, flash, request

# Importar conexión centralizada con PostgreSQL
from conexion.conexion import get_connection

# Importar seguridad de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

# Importar Flask-Login
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

# Importar modelo de usuario
from models import Usuario

# Importar formularios
from forms.cliente_form import ClienteForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm


app = Flask(__name__)


# ==========================================================
# CONFIGURACIÓN DE FLASK-LOGIN
# ==========================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app.config['SECRET_KEY'] = 'acuario_vaporeon_secret_key_2026'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


# ==========================================================
# CARGAR USUARIO DE FLASK-LOGIN
# ==========================================================

@login_manager.user_loader
def load_user(user_id):

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario_db = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario_db:
        return Usuario(
            usuario_db['id'],
            usuario_db['usuario']
        )

    return None


# ==========================================================
# USUARIO AUTENTICADO DISPONIBLE EN LAS PLANTILLAS
# ==========================================================

@app.context_processor
def inyectar_usuario():

    return {
        'usuario_actual': current_user
    }


# ==========================================================
# REGISTRO DE USUARIOS
# ==========================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'registro.html',
                form=form
            )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (
            form.usuario.data,
        ))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conn.close()

            flash(
                'El usuario ya existe.',
                'danger'
            )

            return render_template(
                'registro.html',
                form=form
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            '¡Usuario registrado correctamente!',
            'success'
        )

        return redirect(url_for('login'))

    return render_template(
        'registro.html',
        form=form
    )


# ==========================================================
# INICIO DE SESIÓN
# ==========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        usuario = form.usuario.data
        password = form.password.data

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'login.html',
                form=form
            )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (usuario,))

        usuario_db = cursor.fetchone()

        if usuario_db and check_password_hash(
            usuario_db['password'],
            password
        ):

            usuario_obj = Usuario(
                usuario_db['id'],
                usuario_db['usuario']
            )

            login_user(usuario_obj)

            cursor.execute("""
                INSERT INTO sesiones (usuario_id)
                VALUES (%s)
            """, (usuario_db['id'],))

            conn.commit()

            cursor.close()
            conn.close()

            flash(
                '¡Inicio de sesión exitoso!',
                'success'
            )

            return redirect(url_for('index'))

        cursor.close()
        conn.close()

        flash(
            'Usuario o contraseña incorrectos.',
            'danger'
        )

    return render_template(
        'login.html',
        form=form
    )


# ==========================================================
# CERRAR SESIÓN
# ==========================================================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'Sesión cerrada correctamente.',
        'success'
    )

    return redirect(url_for('login'))


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
@login_required
def productos():

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('index'))

    cursor = conn.cursor()

    # Consulta relacionada mediante JOIN
    cursor.execute("""
        SELECT
            p.id_producto AS id,
            p.nombre,
            p.precio,
            p.stock,
            p.id_proveedor,
            COALESCE(pr.nombre, 'Sin proveedor') AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto
    """)

    productos_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'productos.html',
        productos=productos_db
    )


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():

    form = ProductoForm()

    # Cargar proveedores
    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return render_template(
            'formulario_producto.html',
            form=form
        )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conn.close()

    # Crear opciones del campo proveedor
    form.id_proveedor.choices = [
        (
            proveedor['id_proveedor'],
            proveedor['nombre']
        )
        for proveedor in proveedores_db
    ]

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_producto.html',
                form=form
            )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
                (nombre, precio, stock, id_proveedor)
            VALUES
                (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            '¡Producto guardado y relacionado con el proveedor correctamente!',
            'success'
        )

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form
    )


@app.route(
    '/productos/editar/<int:id_producto>',
    methods=['GET', 'POST']
)
@login_required
def editar_producto(id_producto):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('productos'))

    cursor = conn.cursor()

    # Buscar producto
    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    # Buscar proveedores
    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conn.close()

    if producto is None:

        flash(
            'Producto no encontrado.',
            'danger'
        )

        return redirect(url_for('productos'))

    form = ProductoForm()

    form.id_proveedor.choices = [
        (
            proveedor['id_proveedor'],
            proveedor['nombre']
        )
        for proveedor in proveedores_db
    ]

    # Cargar datos actuales
    if request.method == 'GET':

        form.nombre.data = producto['nombre']
        form.precio.data = producto['precio']
        form.stock.data = producto['stock']
        form.id_proveedor.data = producto['id_proveedor']

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_producto.html',
                form=form,
                editando=True
            )

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data,
            id_producto
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_producto(id_producto):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('productos'))

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    conn.commit()

    cursor.close()
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
@login_required
def clientes():

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('index'))

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_cliente AS id,
            nombre,
            email,
            telefono
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'clientes.html',
        clientes=clientes_db
    )


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_cliente.html',
                form=form
            )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes (nombre, email, telefono)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.email.data,
            form.telefono.data
        ))

        conn.commit()

        cursor.close()
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


@app.route(
    '/clientes/editar/<int:id_cliente>',
    methods=['GET', 'POST']
)
@login_required
def editar_cliente(id_cliente):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('clientes'))

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, email, telefono
        FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if cliente is None:

        flash(
            'Cliente no encontrado.',
            'danger'
        )

        return redirect(url_for('clientes'))

    form = ClienteForm(
        data={
            'nombre': cliente['nombre'],
            'email': cliente['email'],
            'telefono': cliente['telefono']
        }
    )

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_cliente.html',
                form=form,
                editando=True
            )

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                email = %s,
                telefono = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.email.data,
            form.telefono.data,
            id_cliente
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_cliente(id_cliente):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('clientes'))

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    conn.commit()

    cursor.close()
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
@login_required
def proveedores():

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('index'))

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_proveedor AS id,
            nombre,
            contacto,
            telefono
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'proveedores.html',
        proveedores=proveedores_db
    )


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_proveedor.html',
                form=form
            )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores (nombre, contacto, telefono)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.contacto.data,
            form.telefono.data
        ))

        conn.commit()

        cursor.close()
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


@app.route(
    '/proveedores/editar/<int:id_proveedor>',
    methods=['GET', 'POST']
)
@login_required
def editar_proveedor(id_proveedor):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('proveedores'))

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre, contacto, telefono
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if proveedor is None:

        flash(
            'Proveedor no encontrado.',
            'danger'
        )

        return redirect(url_for('proveedores'))

    form = ProveedorForm(
        data={
            'nombre': proveedor['nombre'],
            'contacto': proveedor['contacto'],
            'telefono': proveedor['telefono']
        }
    )

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_proveedor.html',
                form=form,
                editando=True
            )

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                contacto = %s,
                telefono = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.contacto.data,
            form.telefono.data,
            id_proveedor
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_proveedor(id_proveedor):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('proveedores'))

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    conn.commit()

    cursor.close()
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
@login_required
def facturacion():

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('index'))

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id_factura AS id,
            numero,
            cliente,
            fecha,
            total
        FROM facturas
        ORDER BY id_factura
    """)

    facturas_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'facturacion.html',
        facturas=facturas_db
    )


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_facturacion.html',
                form=form
            )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas (numero, cliente, fecha, total)
            VALUES (%s, %s, %s, %s)
        """, (
            form.numero.data,
            form.cliente.data,
            form.fecha.data,
            form.total.data
        ))

        conn.commit()

        cursor.close()
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


@app.route(
    '/facturacion/editar/<int:id_factura>',
    methods=['GET', 'POST']
)
@login_required
def editar_factura(id_factura):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('facturacion'))

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_factura, numero, cliente, fecha, total
        FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    factura = cursor.fetchone()

    cursor.close()
    conn.close()

    if factura is None:

        flash(
            'Factura no encontrada.',
            'danger'
        )

        return redirect(url_for('facturacion'))

    form = FacturacionForm(
        data={
            'numero': factura['numero'],
            'cliente': factura['cliente'],
            'fecha': factura['fecha'],
            'total': factura['total']
        }
    )

    if form.validate_on_submit():

        conn = get_connection()

        if conn is None:
            flash(
                'No se pudo conectar con PostgreSQL.',
                'danger'
            )
            return render_template(
                'formulario_facturacion.html',
                form=form,
                editando=True
            )

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE facturas
            SET numero = %s,
                cliente = %s,
                fecha = %s,
                total = %s
            WHERE id_factura = %s
        """, (
            form.numero.data,
            form.cliente.data,
            form.fecha.data,
            form.total.data,
            id_factura
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_factura(id_factura):

    conn = get_connection()

    if conn is None:
        flash(
            'No se pudo conectar con PostgreSQL.',
            'danger'
        )
        return redirect(url_for('facturacion'))

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    conn.commit()

    cursor.close()
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
    app.run(debug=False)