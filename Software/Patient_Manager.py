import sqlite3

def create_patients_table():
    # Conecta a la base de datos (o crea una nueva si no existe)
    conn = sqlite3.connect('../Database/patients.db')
    c = conn.cursor()

    # Crea la tabla patients
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id varchar PRIMARY KEY,
            firstname varchar,
            lastname varchar,
            description TEXT,
            emotions varchar,
            dominant_emotion TEXT
        )
    ''')

    # Crea un índice en el campo id
    c.execute('CREATE INDEX IF NOT EXISTS idx_patients_id ON patients (id)')

    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()


def insert_patient(id, firstname, lastname, description, emotions, dominant_emotion):
    # Convierte la lista de emociones en una cadena de texto separada por comas
    emotions_str = ','.join(emotions)

    # Conecta a la base de datos
    conn = sqlite3.connect('..Database/patients.db')
    c = conn.cursor()

    # Inserta el nuevo paciente
    c.execute('INSERT INTO patients (id, firstname, lastname, description, emotions, dominant_emotion) VALUES (?,?, ?, ?, ?, ?)',
              (id, firstname, lastname, description, emotions_str, dominant_emotion))

    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()

