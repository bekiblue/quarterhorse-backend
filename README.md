# Quarterhorse Backend

A Flask-based REST API backend built with Rococo for web applications. Provides authentication with JWT and OAuth (Google, Microsoft), user profile management, organization management, and task management with CRUD operations.

## What It Does

- User authentication and authorization (JWT tokens, OAuth)
- User profile management
- Multi-tenant organization management
- Task management (create, read, update, delete tasks)
- Email service integration via RabbitMQ
- Database migrations with Rococo

## How to Run

1. Set up environment variables: Create `.env.secrets` from the sample `.env.secrets.example`
2. Run with Docker: `./run.sh` or `./run.sh --rebuild true`

## Tech Stack

Python 3.11+, Flask, Flask-RESTX, Rococo, PostgreSQL, RabbitMQ
