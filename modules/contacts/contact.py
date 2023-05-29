from flask import Blueprint, request, jsonify
from bson import ObjectId
from .interface import ContactInterface

contact_request = Blueprint('contacts', __name__)

@contact_request.route('/', methods=['GET'])
def get_all_contacts():
    """
    Route pour récupérer tous les contacts
    Méthode : GET
    """
    contacts = ContactInterface().get_all_contacts()

    if not contacts:
        return jsonify(message="Aucun contact trouvé"), 404

    return jsonify(contacts), 200

@contact_request.route('/create', methods=['POST'])
def create_contact():
    """
    Route pour créer un nouveau contact
    Méthode : POST
    """
    # Obtenir les données du contact à partir de la requête
    data = request.get_json()
    
    # Utilisation de l'interface pour créer un nouveau contact
    new_contact = ContactInterface().create_contact(data)
    
    # Renvoyer le nouveau contact créé sous forme de réponse JSON
    return jsonify(new_contact), 201

@contact_request.route('/update', methods=['PUT'])
def update_contact():
    """
    Route pour mettre à jour un contact existant
    Méthode : PUT
    """
    data = request.get_json()

    if not data:
        return jsonify(message="Données de contact manquantes"), 400

    contact_id = data.get('id')

    if not contact_id:
        return jsonify(message="ID de contact manquant"), 400

    updated_contact = {}

    if 'fullname' in data:
        updated_contact['fullname'] = data.get('fullname')
    
    if 'email' in data:
        updated_contact['email'] = data.get('email')
    
    if 'phone' in data:
        updated_contact['phone'] = data.get('phone')
    filter = {'_id': ObjectId(contact_id)}
    result = ContactInterface().update_contact(filter, updated_contact)

    if not result:
        return jsonify(message="Contact non trouvé"), 404

    return jsonify(message="Contact mis à jour avec succès"), 200

@contact_request.route('/delete', methods=['DELETE'])
def delete_contact():
    """
    Route pour supprimer un contact
    Méthode : DELETE
    """
    data = request.get_json()

    if not data:
        return jsonify(message="Données de contact manquantes"), 400

    contact_id = data.get('id')

    if not contact_id:
        return jsonify(message="ID de contact manquant"), 400

    filter = {'_id': ObjectId(contact_id)}
    result = ContactInterface().delete_contact(filter)

    if not result:
        return jsonify(message="Contact non trouvé"), 404

    return jsonify(message="Contact supprimé avec succès"), 200



@contact_request.route('/<id>', methods=['GET'])
def get_contact_by_id(id):
    """
    Route pour récupérer un contact par son ID
    Méthode : GET
    """
    # Implémentation pour renvoyer un contact spécifique en fonction de son ID
    filter = {'_id': ObjectId(id)}
    contact = ContactInterface().get_contact_by_id(filter)
    if contact:
        return jsonify(contact), 200
    else:
        return jsonify({"message": "Contact not found"}), 404
