from flask_sqlalchemy import SQLAlchemy #importar SQLAlchemy

#permite crear modelos de base de datos
db = SQLAlchemy()

class Contact(db.Model): #esta clase podra crear, buscar, eliminar desde la base de datos
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

    #esto es lo que enviaremos para crear el JSON
    def serialize(self):
        return {
           "id": self.id,
           "name": self.name,
           "phone": self.phone           
        }
    
    def save(self):
       db.session.add()
       db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
