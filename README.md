# 📦 Inventory Management System – Backend

A secure backend for managing products, warehouses, and inventory with **multi-warehouse support**, **real-time low-stock alerts**, **reorder suggestions**, **reporting**, and **role-based access control**.

---

## 🚀 Tech Stack

- FastAPI  
- PostgreSQL  
- SQLModel  
- Alembic (migrations)  
- JWT Authentication  
- RBAC  
- WebSockets (real-time alerts)

---

## 🔐 Authentication & Authorization

- JWT-based authentication using **HTTP Bearer tokens**
- APIs are **not public**

### Roles

| Role   | Access |
|------|-------|
| `admin` | Full access (master data + inventory) |
| `viewer` | Read-only (views & reports) |

> Admin users are created via **seed scripts only**.

### Auth Endpoints

```http
POST /auth/signup   → create viewer user
POST /auth/login    → login & receive JWT
```

## 🧩 Core Features

### 📦 Products
- Create product (**admin only**)
- Search by name or ID
- View stock across all warehouses

---

### 🏬 Warehouses
- Create warehouse (**admin only**)
- List warehouses
- View warehouse inventory

---

### 📊 Inventory
- Create inventory records (**admin only**)
- Stock adjustment (**IN / OUT**)
- Manual reconciliation
- Inventory movement audit trail

---

## 🔔 Real-Time Low-Stock Alerts (WebSockets)

- Low-stock detected from inventory data
- Alerts pushed in real time using **FastAPI WebSockets**
- Reorder suggestions included
- No external services used

### Alert Condition
```text
inventory.quantity <= product.reorder_level
```
## 🔔 Alert Endpoints

```http
WS   /ws/alerts        → receive real-time alerts
POST /alerts/trigger  → detect & broadcast alerts
```
- Alert delivery is push-based.
- Email / SMS notifications can be added later as extensions.

## 📊 Reports & Exports (Authenticated)

### 📄 Report APIs
```http
GET /reports/low-stock
GET /reports/inventory
GET /reports/warehouse/{warehouse_id}
GET /reports/inventory-movements
GET /reports/reorder-preview
GET /reports/summary
```

## 📥 CSV Exports

- `GET /reports/low-stock/export`
- `GET /reports/inventory/export`
- `GET /reports/warehouse/{warehouse_id}/export`

---

## 🔐 Access Control Summary

| Area                  | Access         |
|-----------------------|----------------|
| Auth (login/signup)   | Public         |
| Create Products       | Admin          |
| Create Warehouses     | Admin          |
| Inventory Adjustments | Admin          |
| Views & Reports       | Authenticated  |

---

## 🌱 Seed Data

```bash
python -m seeds.seed_admin
python -m seeds.seed_products
python -m seeds.seed_warehouses
python -m seeds.seed_inventory
```
## ▶️ Run Application

```bash
uvicorn app.main:app --reload
```



