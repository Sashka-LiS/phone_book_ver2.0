import db
import UI


class ContactRecord:
    def __init__(self, id: int,surname: str, name: str, father_name: str, email: str):
        self.id = id
        self.surname = surname
        self.name = name
        self.father_name = father_name
        self.email = email


def add_contact(contact_rec: ContactRecord):
    """Добавляет в таблицу contacts"""
    phone_book = db.get_db()
    cursor = phone_book.cursor()
    val_contact = [contact_rec.surname, contact_rec.name, contact_rec.father_name, contact_rec.email]
    cursor.execute("INSERT INTO contacts(surname, name, father_name, email) VALUES (?, ?, ?, ?);", val_contact)
    phone_book.commit()
    id = cursor.lastrowid
    cursor.close()
    return id

def del_contact(id: int):
    phone_book = db.get_db()
    cursor = phone_book.cursor()
    val_for_del = [id]
    cursor.execute('PRAGMA foreign_keys=on')
    cursor.execute('DELETE FROM contacts WHERE id_contact = ?', val_for_del)
    phone_book.commit()
    cursor.close()
    return True

def find_contact(value=None)-> list[ContactRecord]:
    phone_book = db.get_db()
    cursor = phone_book.cursor()
    contacts = []
    if value == None:
        cursor.execute("SELECT id_contact, surname, name, father_name, email FROM contacts;")        
    else:
        value = "%" + value + "%"
        cursor.execute("""SELECT id_contact, surname, name, father_name, email FROM contacts WHERE surname LIKE ?
                          OR name LIKE ?
                          OR father_name LIKE ?
                          OR email LIKE ?;""", [value, value, value, value])
    for contact in cursor.fetchall():
        contacts.append(ContactRecord(contact[0], contact[1], contact[2], contact[3], contact[4]))
    return contacts


