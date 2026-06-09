# Structural Engineering Manufacturing ERP System

A comprehensive Enterprise Resource Planning (ERP) system for structural engineering manufacturing companies.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python -c "from src.database import init_db; init_db()"
```

### 3. Run Examples
```bash
python examples/example_usage.py
```

### 4. Start API Server
```bash
python -m src.app
```

The server will run on http://localhost:5000

## API Endpoints

### Projects
- `POST /api/projects` - Create project
- `GET /api/projects/<id>` - Get project
- `PUT /api/projects/<id>/progress` - Update progress

### Materials
- `POST /api/materials` - Create material
- `GET /api/materials/low-stock` - Get low stock items
- `POST /api/materials/<id>/stock-movement` - Record movement

### Suppliers
- `POST /api/suppliers` - Create supplier

### Purchase Orders
- `POST /api/purchase-orders` - Create PO
- `POST /api/purchase-orders/<id>/items` - Add item

### Production
- `POST /api/production-orders` - Create production order
- `PUT /api/production-orders/<id>/progress` - Update progress

### Invoicing
- `POST /api/invoices` - Create invoice
- `POST /api/invoices/<id>/items` - Add item

### Quality
- `POST /api/quality-inspections` - Create inspection

### Health
- `GET /api/health` - Health check

## Example Usage

```python
from src.database import SessionLocal, init_db
from src.services import ProjectService
from datetime import date

# Initialize
init_db()
db = SessionLocal()

# Create project
project_service = ProjectService(db)
project = project_service.create_project(
    company_id=1,
    project_code="PRJ-001",
    name="Bridge Construction",
    start_date=date.today(),
    budget=500000.00
)

print(f"Created: {project.project_code}")
db.close()
```

## Features

- Project Management
- Inventory Management
- Production Planning
- Procurement Management
- Quality Control
- Financial Management

## License

MIT License
