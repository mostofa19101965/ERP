"""
Example usage of the ERP system
"""

from datetime import datetime, date
from src.database import SessionLocal, init_db
from src.services import (
    ProjectService, MaterialService, SupplierService,
    ProcurementService, ProductionService, FinancialService,
    QualityService
)


def main():
    """Run examples"""
    print("=" * 60)
    print("ERP SYSTEM - USAGE EXAMPLES")
    print("=" * 60)
    
    # Initialize database
    init_db()
    print("\n✓ Database initialized")
    
    db = SessionLocal()
    
    # Example 1: Create Project
    print("\n=== PROJECT EXAMPLE ===")
    project_service = ProjectService(db)
    project = project_service.create_project(
        company_id=1,
        project_code="STR-2024-001",
        name="Bridge Construction Project",
        start_date=date.today(),
        budget=500000.00,
        client_name="City Infrastructure Corp"
    )
    print(f"✓ Created Project: {project.project_code}")
    print(f"  Name: {project.name}")
    print(f"  Budget: ${project.budget}")
    
    # Example 2: Create Material
    print("\n=== MATERIAL EXAMPLE ===")
    material_service = MaterialService(db)
    material = material_service.create_material(
        material_code="STL-001",
        name="Structural Steel Beams",
        category="Steel",
        unit="kg",
        unit_price=50.00,
        reorder_level=1000
    )
    print(f"✓ Created Material: {material.material_code}")
    print(f"  Name: {material.name}")
    print(f"  Unit Price: ${material.unit_price}")
    
    # Example 3: Record Stock Movement
    print("\n=== STOCK MOVEMENT EXAMPLE ===")
    movement = material_service.record_stock_movement(
        material_id=material.id,
        movement_type="inbound",
        quantity=5000.0,
        notes="Initial stock receipt"
    )
    print(f"✓ Recorded stock movement")
    print(f"  Type: {movement.movement_type}")
    print(f"  Quantity: {movement.quantity} kg")
    
    # Example 4: Create Supplier
    print("\n=== SUPPLIER EXAMPLE ===")
    supplier_service = SupplierService(db)
    supplier = supplier_service.create_supplier(
        company_id=1,
        supplier_code="SUP-001",
        name="Steel Supplies Ltd",
        email="contact@steelsupplies.com",
        phone="+1-234-567-8900"
    )
    print(f"✓ Created Supplier: {supplier.supplier_code}")
    print(f"  Name: {supplier.name}")
    print(f"  Email: {supplier.email}")
    
    # Example 5: Create Purchase Order
    print("\n=== PURCHASE ORDER EXAMPLE ===")
    procurement_service = ProcurementService(db)
    po = procurement_service.create_purchase_order(
        supplier_id=supplier.id,
        po_number="PO-2024-001",
        order_date=date.today()
    )
    print(f"✓ Created Purchase Order: {po.po_number}")
    
    # Add item to PO
    po_item = procurement_service.add_item_to_po(
        po_id=po.id,
        material_id=material.id,
        quantity=1000.0,
        unit_price=50.00
    )
    print(f"✓ Added PO Item")
    print(f"  Quantity: {po_item.quantity}")
    print(f"  Line Total: ${po_item.line_total}")
    
    # Example 6: Create Production Order
    print("\n=== PRODUCTION ORDER EXAMPLE ===")
    production_service = ProductionService(db)
    prod_order = production_service.create_production_order(
        production_order_number="PROD-2024-001",
        product_name="Structural Steel Frame",
        quantity_to_produce=100.0
    )
    print(f"✓ Created Production Order: {prod_order.production_order_number}")
    print(f"  Product: {prod_order.product_name}")
    print(f"  Quantity: {prod_order.quantity_to_produce}")
    
    # Update production progress
    production_service.update_production_progress(prod_order.id, 50.0)
    print(f"✓ Updated production: 50 units produced")
    
    # Example 7: Create Invoice
    print("\n=== INVOICE EXAMPLE ===")
    financial_service = FinancialService(db)
    invoice = financial_service.create_invoice(
        invoice_number="INV-2024-001",
        project_id=project.id,
        invoice_date=date.today()
    )
    print(f"✓ Created Invoice: {invoice.invoice_number}")
    
    # Add items to invoice
    item1 = financial_service.add_invoice_item(
        invoice_id=invoice.id,
        description="Labor and Installation",
        quantity=100.0,
        unit_price=500.00
    )
    
    item2 = financial_service.add_invoice_item(
        invoice_id=invoice.id,
        description="Materials",
        quantity=50.0,
        unit_price=200.00
    )
    
    # Calculate totals
    financial_service.calculate_invoice_totals(invoice.id, tax_rate=0.10)
    print(f"✓ Added invoice items and calculated totals")
    print(f"  Item 1: 100 x $500 = $50,000")
    print(f"  Item 2: 50 x $200 = $10,000")
    print(f"  Subtotal: $60,000")
    print(f"  Tax (10%): $6,000")
    print(f"  Total: $66,000")
    
    # Example 8: Quality Inspection
    print("\n=== QUALITY INSPECTION EXAMPLE ===")
    quality_service = QualityService(db)
    inspection = quality_service.create_inspection(
        inspection_code="QC-2024-001",
        inspector_name="John Smith",
        total_samples=100,
        defective_samples=5
    )
    print(f"✓ Created Quality Inspection: {inspection.inspection_code}")
    print(f"  Inspector: {inspection.inspector_name}")
    print(f"  Defect Rate: {(5/100)*100}%")
    
    db.close()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
