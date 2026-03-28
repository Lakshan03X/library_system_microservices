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

Start each service individually:

```bash
# API Gateway (Port 8000)
cd api-gateway
uvicorn main:app --reload --port 8080

# Book Service (Port 8001)
cd book-service
uvicorn main:app --reload --port 8081

# And so on for other services...
```

## API Endpoints

All requests go through the API Gateway at `http://localhost:8080`

### Books

- `GET /books` - Get all books
- `POST /books` - Create a book
- `PUT /books/{id}` - Update a book
- `DELETE /books/{id}` - Delete a book

### Members

- `GET /members` - Get all members
- `POST /members` - Create a member
- `PUT /members/{id}` - Update a member
- `DELETE /members/{id}` - Delete a member

### Borrows

- `GET /borrows` - Get all borrows
- `POST /borrows` - Create a borrow
- `PUT /borrows/{id}` - Update a borrow
- `DELETE /borrows/{id}` - Delete a borrow

### Reviews

- `GET /reviews` - Get all reviews
- `POST /reviews` - Create a review
- `PUT /reviews/{id}` - Update a review
- `DELETE /reviews/{id}` - Delete a review

### Staff

- `GET /staff` - Get all staff
- `POST /staff` - Create staff
- `PUT /staff/{id}` - Update staff
- `DELETE /staff/{id}` - Delete staff

### Reservations

- `GET /reservations` - Get all reservations
- `POST /reservations` - Create a reservation
- `PUT /reservations/{id}` - Update a reservation
- `DELETE /reservations/{id}` - Delete a reservation
