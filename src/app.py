"""
Flask API Application for ERP System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import json

from src.database import SessionLocal, init_db
from src.services import (
    ProjectService, MaterialService, SupplierService,
    ProcurementService, ProductionService, FinancialService,
    QualityService
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
init_db()


def get_db():
    """Get database session"""
    return SessionLocal()


# ============= PROJECT ENDPOINTS =============

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create new project"""
    try:
        data = request.get_json()
        db = get_db()
        service = ProjectService(db)
        
        project = service.create_project(
            company_id=data['company_id'],
            project_code=data.get('project_code', f"PRJ-{datetime.now().timestamp()}"),
            name=data['name'],
            start_date=datetime.fromisoformat(data['start_date']).date(),
            budget=float(data['budget']),
            client_name=data.get('client_name')
        )
        
        db.close()
        return jsonify({'message': 'Project created', 'project_id': project.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get project details"""
    try:
        db = get_db()
        service = ProjectService(db)
        project = service.get_project(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        db.close()
        return jsonify({
            'id': project.id,
            'project_code': project.project_code,
            'name': project.name,
            'budget': float(project.budget or 0),
            'progress': project.progress_percentage
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<int:project_id>/progress', methods=['PUT'])
def update_project_progress(project_id):
    """Update project progress"""
    try:
        data = request.get_json()
        db = get_db()
        service = ProjectService(db)
        
        service.update_project_progress(project_id, float(data['progress_percentage']))
        db.close()
        
        return jsonify({'message': 'Progress updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= MATERIAL ENDPOINTS =============

@app.route('/api/materials', methods=['POST'])
def create_material():
    """Create new material"""
    try:
        data = request.get_json()
        db = get_db()
        service = MaterialService(db)
        
        material = service.create_material(
            material_code=data['material_code'],
            name=data['name'],
            category=data.get('category', 'Uncategorized'),
            unit=data.get('unit', 'kg'),
            unit_price=float(data['unit_price']),
            reorder_level=float(data.get('reorder_level', 0))
        )
        
        db.close()
        return jsonify({'message': 'Material created', 'material_id': material.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/materials/low-stock', methods=['GET'])
def get_low_stock_materials():
    """Get low stock materials"""
    try:
        db = get_db()
        service = MaterialService(db)
        materials = service.get_low_stock_materials()
        
        db.close()
        
        return jsonify([{
            'material_code': m.material_code,
            'name': m.name,
            'current_stock': float(m.quantity_in_stock),
            'reorder_level': float(m.reorder_level or 0)
        } for m in materials]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/materials/<int:material_id>/stock-movement', methods=['POST'])
def record_stock_movement(material_id):
    """Record stock movement"""
    try:
        data = request.get_json()
        db = get_db()
        service = MaterialService(db)
        
        service.record_stock_movement(
            material_id=material_id,
            movement_type=data['movement_type'],
            quantity=float(data['quantity']),
            notes=data.get('notes')
        )
        
        db.close()
        return jsonify({'message': 'Stock movement recorded'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= SUPPLIER ENDPOINTS =============

@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    """Create new supplier"""
    try:
        data = request.get_json()
        db = get_db()
        service = SupplierService(db)
        
        supplier = service.create_supplier(
            company_id=data['company_id'],
            supplier_code=data['supplier_code'],
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        db.close()
        return jsonify({'message': 'Supplier created', 'supplier_id': supplier.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= PURCHASE ORDER ENDPOINTS =============

@app.route('/api/purchase-orders', methods=['POST'])
def create_purchase_order():
    """Create purchase order"""
    try:
        data = request.get_json()
        db = get_db()
        service = ProcurementService(db)
        
        po = service.create_purchase_order(
            supplier_id=data['supplier_id'],
            po_number=data['po_number'],
            order_date=datetime.fromisoformat(data['order_date']).date()
        )
        
        db.close()
        return jsonify({'message': 'PO created', 'po_id': po.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/purchase-orders/<int:po_id>/items', methods=['POST'])
def add_po_item(po_id):
    """Add item to PO"""
    try:
        data = request.get_json()
        db = get_db()
        service = ProcurementService(db)
        
        item = service.add_item_to_po(
            po_id=po_id,
            material_id=data['material_id'],
            quantity=float(data['quantity']),
            unit_price=float(data['unit_price'])
        )
        
        db.close()
        return jsonify({'message': 'Item added', 'item_id': item.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= PRODUCTION ENDPOINTS =============

@app.route('/api/production-orders', methods=['POST'])
def create_production_order():
    """Create production order"""
    try:
        data = request.get_json()
        db = get_db()
        service = ProductionService(db)
        
        po = service.create_production_order(
            production_order_number=data['production_order_number'],
            product_name=data['product_name'],
            quantity_to_produce=float(data['quantity_to_produce'])
        )
        
        db.close()
        return jsonify({'message': 'Production order created', 'po_id': po.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/production-orders/<int:po_id>/progress', methods=['PUT'])
def update_production_progress(po_id):
    """Update production progress"""
    try:
        data = request.get_json()
        db = get_db()
        service = ProductionService(db)
        
        service.update_production_progress(po_id, float(data['quantity_produced']))
        db.close()
        
        return jsonify({'message': 'Production progress updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= INVOICE ENDPOINTS =============

@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    """Create invoice"""
    try:
        data = request.get_json()
        db = get_db()
        service = FinancialService(db)
        
        invoice = service.create_invoice(
            invoice_number=data['invoice_number'],
            project_id=data.get('project_id'),
            invoice_date=datetime.fromisoformat(data['invoice_date']).date()
        )
        
        db.close()
        return jsonify({'message': 'Invoice created', 'invoice_id': invoice.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/invoices/<int:invoice_id>/items', methods=['POST'])
def add_invoice_item(invoice_id):
    """Add item to invoice"""
    try:
        data = request.get_json()
        db = get_db()
        service = FinancialService(db)
        
        service.add_invoice_item(
            invoice_id=invoice_id,
            description=data['description'],
            quantity=float(data['quantity']),
            unit_price=float(data['unit_price'])
        )
        
        service.calculate_invoice_totals(invoice_id)
        db.close()
        
        return jsonify({'message': 'Item added to invoice'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= QUALITY ENDPOINTS =============

@app.route('/api/quality-inspections', methods=['POST'])
def create_quality_inspection():
    """Create quality inspection"""
    try:
        data = request.get_json()
        db = get_db()
        service = QualityService(db)
        
        inspection = service.create_inspection(
            inspection_code=data['inspection_code'],
            inspector_name=data['inspector_name'],
            total_samples=data.get('total_samples'),
            defective_samples=data.get('defective_samples')
        )
        
        db.close()
        return jsonify({'message': 'Inspection created', 'inspection_id': inspection.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
