from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
import datetime

listaEquipo= [
    ['mateo', 'Moreira Mateo','mmoreira@alumnos.uai.cl'],
    ['pascal', 'Novion Pascale','pnovion@alumnos.uai.cl'],
    ['ortiz', 'Ortiz Matías','matiaortiz@alumnos.uai.cl'],
    ['ochoa', 'Ochoa Matías','maochoa@alumnos.uai.cl']
]

app = Flask(__name__)
app.testing = True
app.secret_key = 'EstaEsLaContraseñaQueNoDeberiasConocerBesitosMua'

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3306,
    'database': 'Proyecto_tei'
}

conn = mysql.connector.connect(**config)
cursor= conn.cursor(buffered=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/equipo')
def equipo():
    return render_template('equipo.html', listaEquipo=listaEquipo, CantIntegrantes=len(listaEquipo))

@app.route('/login', methods=['POST'])
def login():
    nombreUsuario = request.form.get('nombreUsuario')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `Usuarios Registrados` WHERE `nombre` LIKE '{}' AND `contrasena` LIKE '{}'""".format(nombreUsuario,password))
    usuarios=cursor.fetchall()

    if len(usuarios) > 0:

        session['id'] = usuarios[0][0]
        session['name'] = usuarios[0][1]
        session['active'] = True
        session.permanent = False

        now = datetime.datetime.now()
        fechaAhora = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        newCursor= conn.cursor(buffered=True, dictionary=True)
        newCursor.execute(""" SELECT (ultimo_dia) FROM `Usuarios Registrados` WHERE id_usuario = '{}' ;""".format(session['id']))
        Consultafecha = newCursor.fetchone()
        ultimaFecha = Consultafecha['ultimo_dia']

        if fechaAhora != ultimaFecha:
            newCursor.execute(""" SELECT * FROM `Tareas` WHERE id_usuario = '{}' ;""".format(session['id']))
            ConsultaTareas = newCursor.fetchone()
            listaTareas = [
                ConsultaTareas['tarea 1'],
                ConsultaTareas['tarea 2'],
                ConsultaTareas['tarea 3'],
                ConsultaTareas['tarea 4']
            ]

            newCursor.execute(""" SELECT * FROM `Experiencia` WHERE id_usuario = '{}' ;""".format(session['id']))
            ConsultaExperiencia = newCursor.fetchone()
            listaExperiencia = [
            ConsultaExperiencia['Alimentacion'],
            ConsultaExperiencia['Transporte'],
            ConsultaExperiencia['Reciclaje'],
            ConsultaExperiencia['Consumo'],
            ConsultaExperiencia['Recursos']
            ]

            nuevaListaExperiencia = [
                listaExperiencia[0] + 4 if listaTareas[0] == 1 else listaExperiencia[0],
                listaExperiencia[1] + 4 if listaTareas[1] == 1 else listaExperiencia[1],
                listaExperiencia[2] + 4 if listaTareas[2] == 1 else listaExperiencia[2],
                listaExperiencia[3] + 4 if listaTareas[2] == 1 else listaExperiencia[3],
                listaExperiencia[4] + 4 if listaTareas[3] == 1 else listaExperiencia[4]
            ]

            newCursor.execute(""" SELECT * FROM `Niveles Post` WHERE id_usuario = '{}' ;""".format(session['id']))
            ConsultaNiveles = newCursor.fetchone()
            listaNiveles = [
                ConsultaNiveles['Alimentacion'],
                ConsultaNiveles['Transporte'],
                ConsultaNiveles['Reciclaje'],
                ConsultaNiveles['Consumo'],
                ConsultaNiveles['Recursos']
            ]

            listaExperienciaLevelup = [
                nuevaListaExperiencia[0] if nuevaListaExperiencia[0] <= 100 else 0,
                nuevaListaExperiencia[0] if nuevaListaExperiencia[0] <= 100 else 0,
                nuevaListaExperiencia[0] if nuevaListaExperiencia[0] <= 100 else 0,
                nuevaListaExperiencia[0] if nuevaListaExperiencia[0] <= 100 else 0,
                nuevaListaExperiencia[0] if nuevaListaExperiencia[0] <= 100 else 0
            ]
            newCursor.execute(""" UPDATE `Experiencia` SET `Alimentacion` = '{}' ,`Transporte` = '{}' ,`Reciclaje` = '{}' ,`Consumo` = '{}' ,`Recursos` = '{}' WHERE `id_usuario` = '{}' ;""".format(listaExperienciaLevelup[0], listaExperienciaLevelup[1], listaExperienciaLevelup[2], listaExperienciaLevelup[3], listaExperienciaLevelup[4], session['id']))
            conn.commit()

            nuevaListaNiveles = [
                listaNiveles[0]+1 if listaExperienciaLevelup[0] == 0 and listaNiveles[0] <= 5 else listaNiveles[0],
                listaNiveles[1]+1 if listaExperienciaLevelup[1] == 0 and listaNiveles[1] <= 5 else listaNiveles[1],
                listaNiveles[2]+1 if listaExperienciaLevelup[2] == 0 and listaNiveles[2] <= 5 else listaNiveles[2],
                listaNiveles[3]+1 if listaExperienciaLevelup[3] == 0 and listaNiveles[3] <= 5 else listaNiveles[3],
                listaNiveles[4]+1 if listaExperienciaLevelup[4] == 0 and listaNiveles[4] <= 5 else listaNiveles[4]
            ]
            newCursor.execute(""" UPDATE `Niveles Post` SET Alimentacion='{}' ,Transporte='{}' ,Reciclaje='{}' ,Consumo='{}' ,Recursos='{}' WHERE `Niveles Post`.id_usuario = '{}' ;""".format(nuevaListaNiveles[0],nuevaListaNiveles[1], nuevaListaNiveles[2], nuevaListaNiveles[3], nuevaListaNiveles[4], session['id']))
            conn.commit()

            newCursor.execute(""" UPDATE `Tareas` SET `tarea 1`='{}' ,`tarea 2`='{}' ,`tarea 3`='{}' ,`tarea 4`='{}' WHERE `Tareas`.id_usuario = '{}' ;""".format(0, 0, 0, 0, session['id']))
            conn.commit()

            newCursor.execute(""" UPDATE `Usuarios Registrados` SET ultimo_dia='{}'  WHERE `Usuarios Registrados`.id_usuario = '{}' """.format(fechaAhora ,session['id']))
            conn.commit()


        newCursor.close()
        return redirect(url_for('profile'))
    else:
        flash('Nombre usuario o contraseña incorrecta')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        nombreUsuarioRegistrado= request.form.get('nombreUsuario')
        contrasenaUsuarioRegistrado= request.form.get('password')
        contrasenaConfirmadaUsuarioRegistrado = request.form.get('cpassword')

        Quest1= int(request.form.get('Quest1'))
        Quest2= int(request.form.get('Quest2'))
        Quest3= int(request.form.get('Quest3'))
        Quest4= int(request.form.get('Quest4'))
        Quest5= int(request.form.get('Quest5'))
        Quest6= int(request.form.get('Quest6'))
        Quest7= int(request.form.get('Quest7'))
        Quest8= int(request.form.get('Quest8'))

        nivelAlimento= int(( Quest1 + Quest4)/2)
        nivelTrasporte= Quest7
        nivelReciclaje= Quest2
        nivelConsumo= int((Quest3 + Quest8)/2)
        nivelRecursos= int((Quest5 + Quest6)/2)


        cursor.execute("""SELECT * FROM `Usuarios Registrados` WHERE `nombre` LIKE '{}'""".format(nombreUsuarioRegistrado))
        usuarios=cursor.fetchall()

        if len(usuarios) == 0 and contrasenaUsuarioRegistrado == contrasenaConfirmadaUsuarioRegistrado:
            cursor.execute("""SELECT LAST_INSERT_ID() FROM `Usuarios Registrados`""")
            ultimoId=cursor.fetchall()

            session['id'] = int(ultimoId[0][0])+1
            session['name'] = nombreUsuarioRegistrado
            session['active'] = True

            now = datetime.datetime.now()
            fechaHoy = str(now.year) + '-' + str(now.month) + '-' + str(now.day)


            cursor.execute("""INSERT INTO `Usuarios Registrados` (id_usuario,nombre, contrasena, ultimo_dia) VALUES ('{}', '{}', '{}', '{}')""".format(session['id'], nombreUsuarioRegistrado, contrasenaUsuarioRegistrado, fechaHoy))
            conn.commit()
            cursor.execute("""INSERT INTO `Niveles` (id_usuario, Alimentacion, Transporte, Reciclaje, Consumo, Recursos) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(session['id'], nivelAlimento, nivelTrasporte, nivelReciclaje, nivelConsumo, nivelRecursos))
            conn.commit()
            cursor.execute("""INSERT INTO `Niveles Post` (id_usuario, Alimentacion, Transporte, Reciclaje, Consumo, Recursos) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(session['id'], nivelAlimento, nivelTrasporte, nivelReciclaje, nivelConsumo, nivelRecursos))
            conn.commit()
            cursor.execute("""INSERT INTO `Experiencia` (id_usuario, Alimentacion, Transporte, Reciclaje, Consumo, Recursos) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(session['id'], 0, 0, 0, 0, 0))
            conn.commit()
            cursor.execute("""INSERT INTO `Tareas` (id_usuario, tarea 1, tarea 2, tarea 3, tarea 4) VALUES ('{}', '{}', '{}', '{}', '{}')""".format(session['id'], 0, 0, 0, 0))
            conn.commit()

            return redirect(url_for('profile'))
        else:
            flash('Nombre usuario ya ocupado')
            return redirect(url_for('registro'))
    return render_template('registro.html')

@app.route('/profile')
def profile():
    if 'active' in session:
        cursor.execute("""SELECT * FROM `Niveles Post` WHERE `id_usuario` LIKE '{}'""".format(int(session['id'])))
        usuario = cursor.fetchall()

        newCursor= conn.cursor(buffered=True, dictionary=True)
        newCursor.execute(""" SELECT * FROM `Tareas` WHERE id_usuario = '{}'""".format(session['id']))
        TareaValor = newCursor.fetchone()

        listaTareas = [
            TareaValor['tarea 1'],
            TareaValor['tarea 2'],
            TareaValor['tarea 3'],
            TareaValor['tarea 4']
        ]

        nombre=session['name']
        NivelComida=usuario[0][1]
        NivelTrasporte=usuario[0][2]
        NivelReciclaje=usuario[0][3]
        NivelConsumo=usuario[0][4]
        NivelRecursos=usuario[0][5]
        PromedioNivel= int((usuario[0][1] + usuario[0][2] + usuario[0][3] + usuario[0][4] + usuario[0][5])/5)
        NivelesOrdenadosPorMenor = {
            "NivelComida":usuario[0][1],
            "NivelTrasporte":usuario[0][2],
            "NivelReciclaje":usuario[0][3],
            "NivelConsumo":usuario[0][4],
            "NivelRecursos":usuario[0][5]
        }
        NivelesOrdenadosPorMenor = dict(sorted(NivelesOrdenadosPorMenor.items(), key=lambda item: item[1]))

        keyTresTareaMenores = list(NivelesOrdenadosPorMenor)[0:4]

        newCursor.close()
        return render_template('nivel.html',
            nombre=nombre,
            NivelComida=NivelComida,
            NivelTrasporte=NivelTrasporte,
            NivelReciclaje=NivelReciclaje,
            NivelConsumo=NivelConsumo,
            NivelRecursos=NivelRecursos,
            PromedioNivel=PromedioNivel,
            listaTareas=listaTareas,
            NivelesOrdenadosPorMenor=NivelesOrdenadosPorMenor,
            keyTresTareaMenores =keyTresTareaMenores
        )

    return redirect(url_for('index'))

@app.route('/checked/<Numtarea>', methods=['POST', 'GET'])
def checked(Numtarea):
    newCursor= conn.cursor(buffered=True, dictionary=True)

    tarea = 'tarea' + ' ' + str(Numtarea)

    newCursor.execute(""" SELECT * FROM `Tareas` WHERE id_usuario = '{}'""".format(session['id']))
    TareaValor = newCursor.fetchone()

    newCursor.execute(""" UPDATE `Tareas` SET `{}` = '{}' WHERE `Tareas`.id_usuario = '{}' """.format(tarea, 1, session['id']) )
    conn.commit()
    

    newCursor.close()
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run()
