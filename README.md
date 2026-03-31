# Library System Microservices

A microservices-based library management system built with FastAPI.

## Architecture

This system consists of the following microservices:

| Service             | Port | Description                          |
| ------------------- | ---- | ------------------------------------ |
| API Gateway         | 8080 | Central entry point for all requests |
| Book Service        | 8081 | Manages book inventory               |
| Member Service      | 8082 | Handles library members              |
| Borrow Service      | 8083 | Manages book borrowing               |
| Review Service      | 8084 | Handles book reviews                 |
| Staff Service       | 8085 | Manages library staff                |
| Reservation Service | 8086 | Handles book reservations            |

## Service Communication

```
                              ┌──────────────────┐
                              │   API Gateway    │
                              │   (Port 8080)    │
                              └────────┬─────────┘
                                       │
       ┌───────────┬───────────┬───────┼───────┬───────────┬───────────┐
       │           │           │       │       │           │           │
       ▼           ▼           ▼       ▼       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  Book    │ │  Member  │ │  Borrow  │ │  Review  │ │  Staff   │ │Reservation│
│ Service  │ │ Service  │ │ Service  │ │ Service  │ │ Service  │ │ Service   │
│  (8081)  │ │  (8082)  │ │  (8083)  │ │  (8084)  │ │  (8085)  │ │  (8086)   │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────────┘ └────┬─────┘
     │            │            │            │                         │
     │            │            │            │                         │
     └────────────┴────────────┴────────────┴─────────────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   MongoDB    │
                        │ (library_db) │
                        └──────────────┘
```

### Inter-Service Validation

The following services validate data against other services before creating records:

- **Borrow Service** → Validates `book_id` against Book Service and `member_id` against Member Service
- **Review Service** → Validates `book_id` against Book Service and `member_id` against Member Service
- **Reservation Service** → Validates `book_id` against Book Service and `member_id` against Member Service

## Project Structure

```
library_system_microservices/
├── api-gateway/          # Central API Gateway
├── book-service/         # Book management service
├── member-service/       # Member management service
├── borrow-service/       # Borrowing management service
├── review-service/       # Review management service
├── staff-service/        # Staff management service
├── reservation-service/  # Reservation management service
├── start_all.bat         # Script to start all services
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd library_system_microservices
```

2. Install dependencies for each service:

```bash
cd api-gateway
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env` in each service
   - Update the values as needed

### Running the Services

**Option 1**: Use the batch script to start all services:

```bash
start_all.bat
```

**Option 2**: Start each service individually:

```bash
# API Gateway (Port 8080)
cd api-gateway
uvicorn main:app --reload --port 8080

# Book Service (Port 8081)
cd book-service
uvicorn main:app --reload --port 8081

# Member Service (Port 8082)
cd member-service
uvicorn main:app --reload --port 8082

# Borrow Service (Port 8083)
cd borrow-service
uvicorn main:app --reload --port 8083

# Review Service (Port 8084)
cd review-service
uvicorn main:app --reload --port 8084

# Staff Service (Port 8085)
cd staff-service
uvicorn main:app --reload --port 8085

# Reservation Service (Port 8086)
cd reservation-service
uvicorn main:app --reload --port 8086
```

## API Endpoints

All requests go through the API Gateway at `http://localhost:8080`

### Books

- `GET /books` - Get all books
- `GET /books/{book_id}` - Get a specific book
- `POST /books` - Create a book
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

### Members

- `GET /members` - Get all members
- `GET /members/{member_id}` - Get a specific member
- `POST /members` - Create a member
- `PUT /members/{member_id}` - Update a member
- `DELETE /members/{member_id}` - Delete a member

### Borrows

- `GET /borrows` - Get all borrows
- `GET /borrows/{borrow_id}` - Get a specific borrow
- `GET /borrows/member/{member_id}` - Get borrows by member
- `GET /borrows/book/{book_id}` - Get borrows by book
- `GET /borrows/status/overdue` - Get overdue borrows
- `POST /borrows` - Create a borrow (validates book_id and member_id)
- `PUT /borrows/{borrow_id}` - Update a borrow
- `PUT /borrows/{borrow_id}/return` - Mark book as returned
- `PUT /borrows/{borrow_id}/overdue` - Mark as overdue
- `DELETE /borrows/{borrow_id}` - Delete a borrow

### Reviews

- `GET /reviews` - Get all reviews
- `GET /reviews/{review_id}` - Get a specific review
- `GET /reviews/book/{book_id}` - Get reviews by book
- `GET /reviews/member/{member_id}` - Get reviews by member
- `POST /reviews` - Create a review (validates book_id and member_id)
- `PUT /reviews/{review_id}` - Update a review
- `DELETE /reviews/{review_id}` - Delete a review

### Staff

- `GET /staff` - Get all staff
- `GET /staff/{staff_id}` - Get a specific staff member
- `POST /staff` - Create staff
- `PUT /staff/{staff_id}` - Update staff
- `DELETE /staff/{staff_id}` - Delete staff

### Reservations

- `GET /reservations` - Get all reservations
- `GET /reservations/{reservation_id}` - Get a specific reservation
- `GET /reservations/member/{member_id}` - Get reservations by member
- `GET /reservations/book/{book_id}` - Get reservations by book
- `POST /reservations` - Create a reservation (validates book_id and member_id)
- `PUT /reservations/{reservation_id}` - Update a reservation
- `PUT /reservations/{reservation_id}/confirm` - Confirm a reservation
- `DELETE /reservations/{reservation_id}` - Delete a reservation

### Health Checks

Each service exposes health endpoints:

- `GET /` - Service info
- `GET /health` - Health status
