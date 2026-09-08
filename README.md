# Distributed Online Marketplace

A university project developed as part of the **Distributed Web Applications** course.

This project demonstrates the design and implementation of an online marketplace using **Flask**. The application was initially developed as a **monolithic web application** and was later refactored into a **microservice architecture** to explore distributed system principles and service-oriented design.

## Features

* User authentication and authorization
* User registration
* Marketplace listings
* Listing search and filtering
* Buyer–seller communication
* Reviews and ratings
* User profile management

## Architecture

The project was developed in two stages: a monolithic architecture followed by a microservice-based architecture.

### Monolithic Architecture

The initial version was implemented as a single Flask application using:

* **Flask** — Web framework
* **SQLAlchemy** — ORM and database interaction
* **SQLite** — Database
* **Flask-Login** — User session management
* **WTForms** — Form handling and validation
* **Jinja** — Server-side templating
* **Bootstrap** — Frontend styling
* **Docker** — Containerization

### Microservice Architecture

The application was later redesigned into a set of independent services:

* **Frontend Service** — Handles the user interface and client-facing functionality
* **Authentication Service** — Manages user authentication and authorization
* **Listing Service** — Manages marketplace listings and related operations
* **Review Service** — Handles reviews and ratings

Each service has its **own database** and communicates with other services through **HTTP-based REST APIs**.

This architecture was used to explore concepts such as service independence, database isolation, inter-service communication, and distributed application design.

## Technologies

* Python
* Flask
* SQLAlchemy
* SQLite
* Docker
* REST APIs
* Microservices
* Jinja
* Bootstrap

## Learning Outcomes

Through this project, we gained practical experience with:

* Distributed systems
* Software architecture and system design
* Monolithic vs. microservice architectures
* Service-to-service communication
* REST API design
* Docker and containerization
* Database isolation
* Authentication and authorization

## Team

Developed as a university group project by:

* **Karim Amin**
* **Mohammad Amin**
* **Taaha Khan**

## Disclaimer

This project was developed for **educational purposes** as part of a university course. It is not intended for production use.
