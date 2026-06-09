"""
Service Layer - Business Logic
"""

from sqlalchemy.orm import Session
from src.models import (
    Project, Material, Supplier, PurchaseOrder, ProductionOrder,
    Invoice, InvoiceItem, QualityInspection, StockMovement,
    ProjectMaterial, BillOfMaterial, PurchaseOrderItem
)
from datetime import datetime, date, timedelta


class ProjectService:
    """Project management services"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_project(self, company_id: int, project_code: str, name: str, 
                      start_date: date, budget: float, **kwargs):
        """Create new project"""
        project = Project(
            company_id=company_id,
            project_code=project_code,
            name=name,
            start_date=start_date,
            budget=budget,
            **kwargs
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_project(self, project_id: int):
        """Get project by ID"""
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def update_project_progress(self, project_id: int, progress_percentage: float):
        """Update project progress"""
        if not 0 <= progress_percentage <= 100:
            raise ValueError("Progress must be between 0 and 100")
        
        project = self.get_project(project_id)
        if project:
            project.progress_percentage = progress_percentage
            self.db.commit()
            self.db.refresh(project)
        return project


class MaterialService:
    """Material and inventory management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_material(self, material_code: str, name: str, category: str,
                       unit: str, unit_price: float, **kwargs):
        """Create new material"""
        material = Material(
            material_code=material_code,
            name=name,
            category=category,
            unit=unit,
            unit_price=unit_price,
            **kwargs
        )
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material
    
    def get_material(self, material_id: int):
        """Get material by ID"""
        return self.db.query(Material).filter(Material.id == material_id).first()
    
    def get_low_stock_materials(self):
        """Get materials below reorder level"""
        return self.db.query(Material).filter(
            Material.quantity_in_stock <= Material.reorder_level
        ).all()
    
    def record_stock_movement(self, material_id: int, movement_type: str,
                            quantity: float, **kwargs):
        """Record stock movement"""
        material = self.get_material(material_id)
        if not material:
            raise ValueError(f"Material {material_id} not found")
        
        # Update stock
        if movement_type == "inbound":
            material.quantity_in_stock += quantity
        elif movement_type == "outbound":
            if material.quantity_in_stock < quantity:
                raise ValueError("Insufficient stock")
            material.quantity_in_stock -= quantity
        
        self.db.add(material)
        
        # Record movement
        movement = StockMovement(
            material_id=material_id,
            movement_type=movement_type,
            quantity=quantity,
            **kwargs
        )
        self.db.add(movement)
        self.db.commit()
        return movement


class SupplierService:
    """Supplier management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_supplier(self, company_id: int, supplier_code: str, name: str, **kwargs):
        """Create new supplier"""
        supplier = Supplier(
            company_id=company_id,
            supplier_code=supplier_code,
            name=name,
            **kwargs
        )
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier
    
    def get_supplier(self, supplier_id: int):
        """Get supplier by ID"""
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()


class ProcurementService:
    """Purchase order management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_purchase_order(self, supplier_id: int, po_number: str,
                            order_date: date, **kwargs):
        """Create purchase order"""
        po = PurchaseOrder(
            supplier_id=supplier_id,
            po_number=po_number,
            order_date=order_date,
            **kwargs
        )
        self.db.add(po)
        self.db.commit()
        self.db.refresh(po)
        return po
    
    def get_purchase_order(self, po_id: int):
        """Get PO by ID"""
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    
    def add_item_to_po(self, po_id: int, material_id: int, quantity: float,
                      unit_price: float):
        """Add item to PO"""
        item = PurchaseOrderItem(
            purchase_order_id=po_id,
            material_id=material_id,
            quantity=quantity,
            unit_price=unit_price,
            line_total=quantity * unit_price
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def get_pending_purchase_orders(self):
        """Get pending POs"""
        from src.models import PurchaseOrderStatus
        return self.db.query(PurchaseOrder).filter(
            PurchaseOrder.status.in_([
                PurchaseOrderStatus.SENT,
                PurchaseOrderStatus.CONFIRMED,
                PurchaseOrderStatus.PARTIALLY_RECEIVED
            ])
        ).all()


class ProductionService:
    """Production management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_production_order(self, production_order_number: str,
                              product_name: str, quantity_to_produce: float, **kwargs):
        """Create production order"""
        po = ProductionOrder(
            production_order_number=production_order_number,
            product_name=product_name,
            quantity_to_produce=quantity_to_produce,
            **kwargs
        )
        self.db.add(po)
        self.db.commit()
        self.db.refresh(po)
        return po
    
    def get_production_order(self, po_id: int):
        """Get production order by ID"""
        return self.db.query(ProductionOrder).filter(ProductionOrder.id == po_id).first()
    
    def update_production_progress(self, po_id: int, quantity_produced: float):
        """Update production progress"""
        po = self.get_production_order(po_id)
        if po:
            if quantity_produced > po.quantity_to_produce:
                raise ValueError("Cannot exceed planned quantity")
            po.quantity_produced = quantity_produced
            self.db.commit()
            self.db.refresh(po)
        return po


class FinancialService:
    """Financial management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_invoice(self, invoice_number: str, project_id: int,
                      invoice_date: date, **kwargs):
        """Create invoice"""
        invoice = Invoice(
            invoice_number=invoice_number,
            project_id=project_id,
            invoice_date=invoice_date,
            **kwargs
        )
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
    
    def get_invoice(self, invoice_id: int):
        """Get invoice by ID"""
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
    
    def add_invoice_item(self, invoice_id: int, description: str,
                        quantity: float, unit_price: float):
        """Add invoice item"""
        item = InvoiceItem(
            invoice_id=invoice_id,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
            line_total=quantity * unit_price
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def calculate_invoice_totals(self, invoice_id: int, tax_rate: float = 0.1):
        """Calculate invoice totals"""
        invoice = self.get_invoice(invoice_id)
        if invoice:
            subtotal = sum(float(item.line_total or 0) for item in invoice.items)
            tax = subtotal * tax_rate
            total = subtotal + tax
            
            invoice.subtotal = subtotal
            invoice.tax_amount = tax
            invoice.total_amount = total
            self.db.commit()
            self.db.refresh(invoice)
        return invoice


class QualityService:
    """Quality control"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_inspection(self, inspection_code: str, inspector_name: str, **kwargs):
        """Create quality inspection"""
        inspection = QualityInspection(
            inspection_code=inspection_code,
            inspector_name=inspector_name,
            **kwargs
        )
        self.db.add(inspection)
        self.db.commit()
        self.db.refresh(inspection)
        return inspection
    
    def get_inspection(self, inspection_id: int):
        """Get inspection by ID"""
        return self.db.query(QualityInspection).filter(
            QualityInspection.id == inspection_id
        ).first()
