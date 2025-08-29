from flask import Blueprint, request, jsonify
from models.contact import Contact, db
from flask_cors import cross_origin
from flask_mail import Message

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('https://back-end-portifolio.onrender.com/contact', methods=['POST'])
@cross_origin()
def submit_contact():
    from main import mail  # Importa aqui, dentro da função, para evitar import circular
    try:
        data = request.get_json()
        
        # Validação básica
        if not data or not all(key in data for key in ['name', 'email', 'subject', 'message']):
            return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
        
        # Criar nova mensagem de contato
        contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()

        # Enviar e-mail
        msg = Message(
            subject=f"Novo contato: {data['subject']}",
            recipients=['pablo2733v@gmail.com'],  # Troque pelo seu e-mail
            body=f"Nome: {data['name']}\nEmail: {data['email']}\nAssunto: {data['subject']}\nMensagem:\n{data['message']}"
        )
        mail.send(msg)
        
        return jsonify({
            'success': True,
            'message': 'Mensagem enviada com sucesso! Retornarei em breve.'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print("Erro submit_contact:", e)
        return jsonify({'error': 'Erro interno do servidor'}), 500

@contact_bp.route('/contact', methods=['GET'])
@cross_origin()
def get_contacts():
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify([contact.to_dict() for contact in contacts]), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar mensagens'}), 500

