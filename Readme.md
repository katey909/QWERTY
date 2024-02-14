# Parking Problem

This project implements a simple Parking Lot API using FastAPI and MongoDB. It allows clients to park and unpark cars, and query car or slot information.
## Features

- **Park a Car**: Assign a car to an available parking slot.
- **Unpark a Car**: Free up a parking slot by removing the car.
- **Get Car/Slot Information**: Retrieve the car number and slot information by either slot number or car number.


## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/parking-lot-api.git
   cd parking-lot-api
2. **Environment Configuration**

   Create a .env file at the root of your project with the following content:
   ```bash
   MONGODB_URL=mongodb://mongodb:27017
   MONGODB_DBNAME=parking_lot_db
   PARKING_LOT_SIZE=10
   ```
   
   This file configures the MongoDB connection and sets the parking lot size.


3. **Launch with Docker Compose**

   Run the following command to build and start the application in daemon mode:
   
   ```bash
   docker-compose up -d
   ```
## Using the API

Once the service is running, you can access the API at `http://localhost:8000`. The API endpoints include:

- **POST /park**: Park a car.
  - Payload: `{"car_number": "ABC123"}`
- **POST /unpark**: Unpark a car.
  - Payload: `{"slot_number": "1"}`
- **GET /info/{identifier}**: Get information about a car or slot.

Explore the API documentation and try out the endpoints by navigating to `http://localhost:8000/docs`.

## Stopping the Service

To stop and remove the containers, execute:

```bash
docker-compose down
```
## Solution Overview

The project is designed to manage parking operations efficiently through three main endpoints. It leverages MongoDB for data persistence to ensure the parking lot state is accurately maintained across sessions. 

The architecture of this project consists of three layers:

- **API Layer**: This layer exposes endpoints to interact with the parking lot system, allowing users to park and unpark cars, and retrieve parking slot information.
- **Database Layer**: Utilizes MongoDB to store and manage parking data, including information about parked cars and their assigned slots.
- **Service Layer**: Contains the core business logic for processing parking operations, ensuring that requests are handled efficiently and effectively.

## Future Scope/ Improvement

Currenty we just specify the parking lot size in .env, That is convinent but pose a real problem if we scale it down. Because we can not remove existing cars/objects to help with it.