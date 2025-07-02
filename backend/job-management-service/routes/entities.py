from flask import Blueprint, request, jsonify
from models import Entity
from utils.database import db

entities_bp = Blueprint('entities', __name__)

@entities_bp.route('/', methods=['GET'])
def get_entities():
    entities = Entity.query.order_by(Entity.created_at.desc()).all()
    return jsonify([entity.to_dict() for entity in entities])

@entities_bp.route('/', methods=['POST'])
def create_entity():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Check if name already exists
    existing_entity = Entity.query.filter_by(name=data['name']).first()
    if existing_entity:
        return jsonify({'error': 'Entity name already exists'}), 400
    
    entity = Entity(
        name=data['name'],
        description=data.get('description')
    )
    
    try:
        db.session.add(entity)
        db.session.commit()
        return jsonify(entity.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create entity'}), 500

@entities_bp.route('/<int:entity_id>', methods=['GET'])
def get_entity(entity_id):
    entity = Entity.query.get_or_404(entity_id)
    return jsonify(entity.to_dict())

@entities_bp.route('/<int:entity_id>', methods=['PUT'])
def update_entity(entity_id):
    entity = Entity.query.get_or_404(entity_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'name' in data:
        existing_entity = Entity.query.filter(
            Entity.name == data['name'], 
            Entity.id != entity_id
        ).first()
        if existing_entity:
            return jsonify({'error': 'Entity name already exists'}), 400
        entity.name = data['name']
    
    if 'description' in data:
        entity.description = data['description']
    
    try:
        db.session.commit()
        return jsonify(entity.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update entity'}), 500

@entities_bp.route('/<int:entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    entity = Entity.query.get_or_404(entity_id)
    
    if len(entity.jobs) > 0:
        return jsonify({'error': 'Cannot delete entity with associated jobs'}), 400
    
    try:
        db.session.delete(entity)
        db.session.commit()
        return jsonify({'message': 'Entity deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete entity'}), 500