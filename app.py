from flask import Flask, render_template, request, jsonify #importar Flask
from flask_script import Manager # permite administrar los comandos por consola y permite crear comandos propios
from flask_migrate import Migrate, MigrateCommand # crea comandos de migracion y llevar a la base de datos
from models import db, Contact #importamos la instancia que creamos en models.py


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #si ocupamos mysql cambiamos "sqlite" por "mysql"
db.init_app(app) 
Migrate(app,db) #vinculando las migraciones entre app y la base de datos
manager = Manager(app) #administrar la app por manager
manager.add_command('db', MigrateCommand) # de todos los comandos los voy administrar por db
#comandos a ejecutar
#db init
#db migrate / migra las instancias creadas en models
#db upgradde / es el que se encarga de llevar las migraciones a la base de datos

@app.route("/")
def main():
    return render_template('index.html')
#@app.route('/api/contacts', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/contacts', methods=['GET', 'POST'])
@app.route('/api/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def contacts(id = None):
    if request.method == 'GET':
        if id is not None:
            contact = Contact.query.get(id)
            if contact:
                return jsonify(contact.serialize()), 200
            else:
                return jsonify({"msg": "Contact not found"})
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
        return jsonify(contacts), 200
        #return jsonify({"msg": "Llegando por el metodo GET"}), 200
        
    if request.method == 'POST':
        name = request.json.get('name')
        phone = request.json.get('phone')
        
        contact = Contact()
        contact.name = name
        contact.phone = phone
        contact.save()
        return jsonify(contact.serialize()), 201
        #return jsonify({"msg": "Llegando por el metodo POST"}), 200
    if request.method == 'PUT':
        name = request.json.get('name')
        phone = request.json.get('phone')

        contact = Contact.query.get(id)

        if not contact:
            return jsonify({"msg": "Contact not found"}), 404

        contact.name = name
        contact.phone = phone
        contact.update()

        return jsonify(contact.serialize()), 200
        
    if request.method == 'DELETE':
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"msg": "Contact not found"}), 404
        contact.delete()
        return jsonify({"success": "Contact deleted"}), 200
        #return jsonify({"msg": "Llegando por el metodo DELETE"}), 200

if __name__ == '__main__':
    manager.run()