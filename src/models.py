"""
Database Models for ERP System
Defines all database schemas for structural engineering manufacturing
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, 
    ForeignKey, Boolean, Text, Enum, Date, Numeric
)
from sqlalchemy.orm import relationship
from src.database import Base
import enum


# ============= STATUS ENUMS =============

class ProjectStatus(enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProductionStatus(enum.Enum):
    PENDING = "pending"
    IN_PRODUCTION = "in_production"
    COMPLETED = "completed"
    QUALITY_CHECK = "quality_check"
    READY_FOR_DELIVERY = "ready_for_delivery"


class PurchaseOrderStatus(enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    CONFIRMED = "confirmed"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class QualityStatus(enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    REWORK_REQUIRED = "rework_required"


# ============= ORGANIZATIONAL MODELS =============

class Company(Base):
    """Company information"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    registration_number = Column(String(100), unique=True)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    phone = Column(String(20))
    email = Column(String(120))
    website = Column(String(255))
    established_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    departments = relationship("Department", back_populates="company")
    projects = relationship("Project", back_populates="company")
    suppliers = relationship("Supplier", back_populates="company")
    
    def __repr__(self):
        return f"<Company {self.name}>"


class Department(Base):
    """Department structure"""
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    manager_name = Column(String(255))
    budget = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department")
    
    def __repr__(self):
        return f"<Department {self.name}>"


class Employee(Base):
    """Employee information"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True)
    phone = Column(String(20))
    designation = Column(String(100))
    salary = Column(Numeric(15, 2))
    hire_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    department = relationship("Department", back_populates="employees")
    
    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"


# ============= PROJECT MODELS =============

class Project(Base):
    """Project information"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    project_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    client_name = Column(String(255))
    client_address = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    budget = Column(Numeric(15, 2))
    actual_cost = Column(Numeric(15, 2), default=0)
    progress_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    materials = relationship("ProjectMaterial", back_populates="project")
    
    def __repr__(self):
        return f"<Project {self.project_code}>"


class Task(Base):
    """Project tasks"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")
    start_date = Column(Date)
    end_date = Column(Date)
    assigned_to = Column(String(255))
    priority = Column(String(50), default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task {self.task_code}>"


# ============= MATERIAL & INVENTORY MODELS =============

class Material(Base):
    """Raw materials and components"""
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True)
    material_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    unit = Column(String(50))
    unit_price = Column(Numeric(12, 2), nullable=False)
    quantity_in_stock = Column(Float, default=0)
    reorder_level = Column(Float)
    reorder_quantity = Column(Float)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    supplier = relationship("Supplier", back_populates="materials")
    purchase_order_items = relationship("PurchaseOrderItem", back_populates="material")
    stock_movements = relationship("StockMovement", back_populates="material")
    
    def __repr__(self):
        return f"<Material {self.material_code}>"


class Warehouse(Base):
    """Warehouse/Storage locations"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255))
    capacity = Column(Float)
    current_utilization = Column(Float, default=0)
    manager_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    inventory = relationship("Inventory", back_populates="warehouse")
    
    def __repr__(self):
        return f"<Warehouse {self.code}>"


class Inventory(Base):
    """Inventory tracking per warehouse"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    quantity = Column(Float, default=0)
    last_counted_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    warehouse = relationship("Warehouse", back_populates="inventory")
    material = relationship("Material")
    
    def __repr__(self):
        return f"<Inventory {self.material_id}>"


class StockMovement(Base):
    """Stock movement history"""
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    movement_type = Column(String(50))
    quantity = Column(Float, nullable=False)
    reference_type = Column(String(100))
    reference_id = Column(Integer)
    notes = Column(Text)
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    material = relationship("Material", back_populates="stock_movements")
    
    def __repr__(self):
        return f"<StockMovement {self.movement_type}>"


class ProjectMaterial(Base):
    """Materials assigned to projects"""
    __tablename__ = "project_materials"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    required_quantity = Column(Float, nullable=False)
    allocated_quantity = Column(Float, default=0)
    consumed_quantity = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="materials")
    material = relationship("Material")
    
    def __repr__(self):
        return f"<ProjectMaterial {self.project_id}>"


# ============= PROCUREMENT MODELS =============

class Supplier(Base):
    """Supplier/Vendor information"""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    supplier_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    email = Column(String(120))
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    payment_terms = Column(String(100))
    rating = Column(Float, default=5.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="suppliers")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
    materials = relationship("Material", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier {self.supplier_code}>"


class PurchaseOrder(Base):
    """Purchase Orders"""
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True)
    po_number = Column(String(100), unique=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    status = Column(Enum(PurchaseOrderStatus), default=PurchaseOrderStatus.DRAFT)
    order_date = Column(Date, nullable=False)
    expected_delivery_date = Column(Date)
    actual_delivery_date = Column(Date)
    total_amount = Column(Numeric(15, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order")
    
    def __repr__(self):
        return f"<PurchaseOrder {self.po_number}>"


class PurchaseOrderItem(Base):
    """Items in Purchase Orders"""
    __tablename__ = "purchase_order_items"
    
    id = Column(Integer, primary_key=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    line_total = Column(Numeric(15, 2))
    received_quantity = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    material = relationship("Material", back_populates="purchase_order_items")
    
    def __repr__(self):
        return f"<PurchaseOrderItem {self.material_id}>"


# ============= PRODUCTION MODELS =============

class ProductionOrder(Base):
    """Production/Manufacturing Orders"""
    __tablename__ = "production_orders"
    
    id = Column(Integer, primary_key=True)
    production_order_number = Column(String(100), unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    product_name = Column(String(255), nullable=False)
    status = Column(Enum(ProductionStatus), default=ProductionStatus.PENDING)
    quantity_to_produce = Column(Float, nullable=False)
    quantity_produced = Column(Float, default=0)
    start_date = Column(Date)
    end_date = Column(Date)
    estimated_completion = Column(Date)
    priority = Column(String(50), default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project")
    bom_items = relationship("BillOfMaterial", back_populates="production_order")
    
    def __repr__(self):
        return f"<ProductionOrder {self.production_order_number}>"


class BillOfMaterial(Base):
    """Bill of Materials for production"""
    __tablename__ = "bill_of_materials"
    
    id = Column(Integer, primary_key=True)
    production_order_id = Column(Integer, ForeignKey("production_orders.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    quantity_per_unit = Column(Float, nullable=False)
    total_quantity_required = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    production_order = relationship("ProductionOrder", back_populates="bom_items")
    material = relationship("Material")
    
    def __repr__(self):
        return f"<BillOfMaterial {self.material_id}>"


class Machinery(Base):
    """Equipment and Machinery"""
    __tablename__ = "machinery"
    
    id = Column(Integer, primary_key=True)
    equipment_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(100))
    manufacturer = Column(String(255))
    model = Column(String(100))
    purchase_date = Column(Date)
    installation_date = Column(Date)
    capacity = Column(String(100))
    status = Column(String(50), default="operational")
    maintenance_schedule = Column(String(255))
    last_maintenance_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Machinery {self.equipment_code}>"


# ============= QUALITY CONTROL MODELS =============

class QualityInspection(Base):
    """Quality Control Inspections"""
    __tablename__ = "quality_inspections"
    
    id = Column(Integer, primary_key=True)
    inspection_code = Column(String(100), unique=True, nullable=False)
    production_order_id = Column(Integer, ForeignKey("production_orders.id"))
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"))
    inspector_name = Column(String(255))
    inspection_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(QualityStatus), default=QualityStatus.PASSED)
    total_samples = Column(Integer)
    defective_samples = Column(Integer)
    defect_rate = Column(Float)
    comments = Column(Text)
    approved_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    defects = relationship("QualityDefect", back_populates="inspection")
    
    def __repr__(self):
        return f"<QualityInspection {self.inspection_code}>"


class QualityDefect(Base):
    """Quality Defects found during inspection"""
    __tablename__ = "quality_defects"
    
    id = Column(Integer, primary_key=True)
    inspection_id = Column(Integer, ForeignKey("quality_inspections.id"), nullable=False)
    defect_type = Column(String(255))
    description = Column(Text)
    severity = Column(String(50))
    action_taken = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    inspection = relationship("QualityInspection", back_populates="defects")
    
    def __repr__(self):
        return f"<QualityDefect {self.defect_type}>"


# ============= FINANCIAL MODELS =============

class Invoice(Base):
    """Sales Invoices"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(100), unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date)
    subtotal = Column(Numeric(15, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    status = Column(String(50), default="draft")
    payment_status = Column(String(50), default="pending")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project")
    items = relationship("InvoiceItem", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")
    
    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"


class InvoiceItem(Base):
    """Items in Invoices"""
    __tablename__ = "invoice_items"
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    description = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    line_total = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    invoice = relationship("Invoice", back_populates="items")
    
    def __repr__(self):
        return f"<InvoiceItem {self.description}>"


class Payment(Base):
    """Payment records"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_method = Column(String(50))
    reference_number = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    invoice = relationship("Invoice", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.payment_date}>"


class Expense(Base):
    """Expense tracking"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True)
    expense_code = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    amount = Column(Numeric(15, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    department = Column(String(255))
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String(50), default="pending")
    created_by = Column(String(255))
    approved_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project")
    
    def __repr__(self):
        return f"<Expense {self.expense_code}>"
