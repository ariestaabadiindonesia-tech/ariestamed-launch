# API Documentation - Ariestamed Launch

## Base URL
```
http://localhost:5000/api
```

## Authentication

All endpoints require JWT token in header:
```
Authorization: Bearer {token}
```

## Endpoints

### Auth

#### Register
```
POST /auth/register
{
  "username": "ariesta",
  "email": "ariesta@example.com",
  "password": "password123",
  "full_name": "Ariesta Badii"
}
```

#### Login
```
POST /auth/login
{
  "email": "ariesta@example.com",
  "password": "password123"
}
Response: { "access_token": "jwt_token" }
```

### Products

#### Create Product
```
POST /products
{
  "name": "Python Course",
  "description": "Learn Python programming",
  "category": "course",
  "price": 99.99,
  "link": "https://example.com/course",
  "features": ["30 hours", "Lifetime access", "Certificate"],
  "key_benefits": ["Learn from experts", "Job-ready skills"]
}
```

#### Get All Products
```
GET /products
```

#### Get Product by ID
```
GET /products/{id}
```

#### Update Product
```
PUT /products/{id}
```

#### Delete Product
```
DELETE /products/{id}
```

### Content

#### Generate Content (AI)
```
POST /content/generate
{
  "product_id": 1,
  "content_type": "caption",
  "platform": "instagram",
  "tone": "professional",
  "length": "short"
}
```

#### Create Content
```
POST /content
{
  "product_id": 1,
  "title": "Promo Content",
  "text": "Content text here",
  "content_type": "caption",
  "platform": "instagram",
  "hashtags": ["#python", "#learning"],
  "call_to_action": "Click link in bio"
}
```

#### Get All Content
```
GET /content?product_id={id}&status=draft
```

#### Approve Content
```
PUT /content/{id}/approve
```

### Posts

#### Create Post (Schedule)
```
POST /posts
{
  "content_id": 1,
  "platform": "instagram",
  "scheduled_at": "2024-01-15T10:00:00Z"
}
```

#### Get Scheduled Posts
```
GET /posts?status=scheduled
```

#### Publish Now
```
POST /posts/{id}/publish
```

#### Cancel Scheduled Post
```
POST /posts/{id}/cancel
```

### Analytics

#### Get Post Analytics
```
GET /analytics/posts/{id}
```

#### Get Platform Analytics
```
GET /analytics/platform/{platform}
```

#### Get Dashboard Stats
```
GET /analytics/dashboard
```

#### Get Report (date range)
```
GET /analytics/report?start_date=2024-01-01&end_date=2024-01-31&platform=instagram
```

## Error Responses

```json
{
  "error": "Error message",
  "code": 400,
  "details": "Additional details"
}
```

## Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error
