# Products API Documentation

## Overview

This document describes the RESTful API endpoints for managing products in the Core-API Supabase project. The Products API provides comprehensive functionality for creating, reading, updating, and deleting product information.

## Base URL

```
https://zxqzmvnauqjtclckddoi.supabase.co/rest/v1
```

## Authentication

All API requests require authentication using the Supabase API key:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4cXptdm5hdXFqdGNsY2tkZG9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMxNjczNTEsImV4cCI6MjA2ODc0MzM1MX0.1q_kfDL8oFlSIN7yyg7AO-e9WfF8NGHIY49-INmS168
apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4cXptdm5hdXFqdGNsY2tkZG9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMxNjczNTEsImV4cCI6MjA2ODc0MzM1MX0.1q_kfDL8oFlSIN7yyg7AO-e9WfF8NGHIY49-INmS168
```

## Data Model

### Product Schema

| Field | Type | Description | Required | Constraints |
|-------|------|-------------|----------|-------------|
| `id` | UUID | Unique product identifier | Auto-generated | Primary key |
| `name` | String | Product name | Yes | Max 255 characters |
| `description` | Text | Product description | No | - |
| `category` | String | Product category | No | Max 255 characters |
| `brand` | String | Product brand | No | Max 255 characters |
| `sku` | String | Stock Keeping Unit | No | Unique, Max 255 characters |
| `price` | Decimal | Product price | No | Positive number |
| `created_at` | Timestamp | Creation timestamp | Auto-generated | ISO 8601 format |
| `updated_at` | Timestamp | Last update timestamp | Auto-generated | ISO 8601 format |

## API Endpoints

### 1. Get All Products

Retrieve a list of all products with optional filtering and pagination.

**Endpoint:** `GET /products`

**Query Parameters:**
- `select` (optional): Specify fields to return (default: all fields)
- `limit` (optional): Number of records to return (default: 1000)
- `offset` (optional): Number of records to skip (default: 0)
- `order` (optional): Sort order (e.g., `created_at.desc`)
- `category` (optional): Filter by category
- `brand` (optional): Filter by brand

**Example Request:**
```http
GET /products?select=id,name,price,category&limit=10&order=created_at.desc
```

**Example Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Wireless Bluetooth Headphones",
    "price": 99.99,
    "category": "Electronics"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Organic Cotton T-Shirt",
    "price": 29.99,
    "category": "Clothing"
  }
]
```

### 2. Get Product by ID

Retrieve a specific product by its unique identifier.

**Endpoint:** `GET /products?id=eq.{product_id}`

**Path Parameters:**
- `product_id` (required): UUID of the product

**Example Request:**
```http
GET /products?id=eq.550e8400-e29b-41d4-a716-446655440000
```

**Example Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Wireless Bluetooth Headphones",
    "description": "High-quality wireless headphones with noise cancellation",
    "category": "Electronics",
    "brand": "TechBrand",
    "sku": "TB-WBH-001",
    "price": 99.99,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 3. Create New Product

Create a new product in the system.

**Endpoint:** `POST /products`

**Request Headers:**
```http
Content-Type: application/json
Prefer: return=representation
```

**Request Body:**
```json
{
  "name": "Smart Fitness Watch",
  "description": "Advanced fitness tracking with heart rate monitor",
  "category": "Electronics",
  "brand": "FitTech",
  "sku": "FT-SFW-002",
  "price": 199.99
}
```

**Example Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "Smart Fitness Watch",
    "description": "Advanced fitness tracking with heart rate monitor",
    "category": "Electronics",
    "brand": "FitTech",
    "sku": "FT-SFW-002",
    "price": 199.99,
    "created_at": "2024-01-16T14:22:00Z",
    "updated_at": "2024-01-16T14:22:00Z"
  }
]
```

### 4. Update Product

Update an existing product's information.

**Endpoint:** `PATCH /products?id=eq.{product_id}`

**Request Headers:**
```http
Content-Type: application/json
Prefer: return=representation
```

**Request Body:**
```json
{
  "price": 179.99,
  "description": "Advanced fitness tracking with heart rate monitor and GPS"
}
```

**Example Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "name": "Smart Fitness Watch",
    "description": "Advanced fitness tracking with heart rate monitor and GPS",
    "category": "Electronics",
    "brand": "FitTech",
    "sku": "FT-SFW-002",
    "price": 179.99,
    "created_at": "2024-01-16T14:22:00Z",
    "updated_at": "2024-01-16T15:45:00Z"
  }
]
```

### 5. Delete Product

Remove a product from the system.

**Endpoint:** `DELETE /products?id=eq.{product_id}`

**Example Request:**
```http
DELETE /products?id=eq.550e8400-e29b-41d4-a716-446655440002
```

**Example Response:**
```http
Status: 204 No Content
```

## Advanced Queries

### Filter by Multiple Criteria

```http
GET /products?category=eq.Electronics&price=gte.50&price=lte.200
```

### Search by Name

```http
GET /products?name=ilike.*headphones*
```

### Get Products with Specific SKUs

```http
GET /products?sku=in.(TB-WBH-001,FT-SFW-002,AC-OCT-003)
```

## Error Responses

### 400 Bad Request
```json
{
  "code": "PGRST102",
  "details": "The request body is not valid JSON",
  "hint": null,
  "message": "Invalid JSON in request body"
}
```

### 401 Unauthorized
```json
{
  "code": "PGRST301",
  "details": null,
  "hint": null,
  "message": "JWT expired"
}
```

### 404 Not Found
```json
{
  "code": "PGRST116",
  "details": "The result contains 0 rows",
  "hint": null,
  "message": "JSON object requested, multiple (or no) rows returned"
}
```

### 409 Conflict
```json
{
  "code": "23505",
  "details": "Key (sku)=(TB-WBH-001) already exists.",
  "hint": null,
  "message": "duplicate key value violates unique constraint \"products_sku_key\""
}
```

### 422 Unprocessable Entity
```json
{
  "code": "PGRST200",
  "details": "Failing row contains (null, Test Product, null, null, null, null, null, 2024-01-16 16:00:00+00, 2024-01-16 16:00:00+00).",
  "hint": null,
  "message": "new row for relation \"products\" violates check constraint"
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- **Anonymous requests**: 100 requests per hour
- **Authenticated requests**: 1000 requests per hour

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642348800
```

## Best Practices

### 1. Use Appropriate HTTP Methods
- `GET` for retrieving data
- `POST` for creating new resources
- `PATCH` for partial updates
- `DELETE` for removing resources

### 2. Handle Errors Gracefully
Always check the HTTP status code and parse error responses appropriately.

### 3. Implement Pagination
For large datasets, use `limit` and `offset` parameters to implement pagination.

### 4. Use Field Selection
Use the `select` parameter to retrieve only the fields you need, reducing bandwidth and improving performance.

### 5. Validate Input Data
Ensure all required fields are provided and data types are correct before making requests.

## SDK Examples

### JavaScript/TypeScript (Supabase Client)

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://zxqzmvnauqjtclckddoi.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4cXptdm5hdXFqdGNsY2tkZG9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMxNjczNTEsImV4cCI6MjA2ODc0MzM1MX0.1q_kfDL8oFlSIN7yyg7AO-e9WfF8NGHIY49-INmS168'
)

// Get all products
const { data: products, error } = await supabase
  .from('products')
  .select('*')

// Get product by ID
const { data: product, error } = await supabase
  .from('products')
  .select('*')
  .eq('id', '550e8400-e29b-41d4-a716-446655440000')
  .single()

// Create new product
const { data: newProduct, error } = await supabase
  .from('products')
  .insert({
    name: 'New Product',
    price: 49.99,
    category: 'Electronics'
  })
  .select()

// Update product
const { data: updatedProduct, error } = await supabase
  .from('products')
  .update({ price: 39.99 })
  .eq('id', '550e8400-e29b-41d4-a716-446655440000')
  .select()

// Delete product
const { error } = await supabase
  .from('products')
  .delete()
  .eq('id', '550e8400-e29b-41d4-a716-446655440000')
```

### Python

```python
import requests

BASE_URL = "https://zxqzmvnauqjtclckddoi.supabase.co/rest/v1"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4cXptdm5hdXFqdGNsY2tkZG9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMxNjczNTEsImV4cCI6MjA2ODc0MzM1MX0.1q_kfDL8oFlSIN7yyg7AO-e9WfF8NGHIY49-INmS168"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

# Get all products
response = requests.get(f"{BASE_URL}/products", headers=headers)
products = response.json()

# Create new product
new_product = {
    "name": "New Product",
    "price": 49.99,
    "category": "Electronics"
}
response = requests.post(
    f"{BASE_URL}/products",
    json=new_product,
    headers={**headers, "Prefer": "return=representation"}
)
created_product = response.json()
```

## Changelog

### Version 1.0.0 (2024-01-16)
- Initial API documentation
- Basic CRUD operations for products
- Error handling documentation
- SDK examples

---

**Last Updated:** January 16, 2024  
**API Version:** 1.0.0  
**Supabase Project:** Core-API (zxqzmvnauqjtclckddoi)