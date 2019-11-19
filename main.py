import os
import sqlite3

# TODO
# - gebruik execute i.p.v. executescript --> meerdere mensen inserten nog steeds mogelijk
# - demonstreer veilige manier: https://docs.python.org/2/library/sqlite3.html#cursor-objects

# normale gebruikersinvoer
user_input_normal_achternaam = "Somers"
user_input_normal_voornaam = "Willy"

# gebruikersinvoer van iemand die een SQL injection attack probeert
user_input_hacked_achternaam = "hacker"
user_input_hacked_voornaam = "man'); DROP TABLE mensen; SELECT ('"


conn = sqlite3.connect(database=':memory:')

def maak_tabel():
    conn.execute('''
    CREATE TABLE mensen (
        achternaam TEXT,
        voornaam TEXT
    )
    ''')

def voeg_startdata_toe():
    conn.execute('''
    INSERT INTO mensen (achternaam, voornaam)
    VALUES
        ('Janssens', 'Jos'),
        ('Schrijvers', 'Mieke')
    ''')

def voeg_mens_toe(achternaam, voornaam):
    qry = f'''
        INSERT INTO mensen (achternaam, voornaam)
        VALUES
            ('{achternaam}', '{voornaam}')
        '''
    print("We gaan deze query uitvoeren:")
    print(qry)
    conn.executescript(qry)

def toon_mensen():
    print("Mensen in database")
    for mens in conn.execute('SELECT * FROM mensen'):
        print(mens)
    print()


if __name__ == "__main__":
    maak_tabel()
    voeg_startdata_toe()
    
    voeg_mens_toe(user_input_normal_achternaam, user_input_normal_voornaam)
    
    toon_mensen()

    # SQL INJECTION ATTACK IMMINENT:
    voeg_mens_toe(user_input_hacked_achternaam, user_input_hacked_voornaam)
    
    # TABLE GONE?!
    try:
        toon_mensen()
    except sqlite3.OperationalError as e:
        print(e)

