# High-Performance Zoho-Style CRM with Flask, Supabase, and Redis

This project is a modular, high-performance CRM built with a powerful backend stack designed for speed, scalability, and real-time features. It leverages an asynchronous Flask application, a Supabase backend for database, authentication, storage, and serverless functions, and Redis for caching.

## Features

- **Custom Modules**: Dynamically create CRM modules (e.g., Leads, Contacts, Deals).
- **Custom Fields**: Add unlimited, typed custom fields to any module.
- **Relational Data**: Link records to notes, tasks, meetings, files, and more.
- **Real-time Updates**: UI updates instantly via Supabase Realtime.
- **Audit History**: Track all changes to records.
- **Secure File Storage**: Use Supabase Storage with signed URLs for secure access.
- **Background Jobs**: Offload heavy tasks like CSV imports and notifications to Supabase Edge Functions.
- **High Performance**: Asynchronous Flask, Redis caching, and PgBouncer connection pooling.

## Tech Stack

- **Backend**: Flask (Async)
- **Database**: Supabase Postgres
- **Authentication**: Supabase Auth (JWT-based with RLS)
- **File Storage**: Supabase Storage
- **Realtime**: Supabase Realtime
- **Serverless Functions**: Supabase Edge Functions (Deno/TypeScript)
- **Caching**: Redis
- **Containerization**: Docker, Docker Compose
- **Frontend**: Tailwind CSS, Alpine.js

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Supabase Account ([app.supabase.io](https://app.supabase.io/))
- Supabase CLI

### 1. Supabase Project Setup

1.  **Create a New Supabase Project**:
    - Go to [app.supabase.io](https://app.supabase.io/) and create a new project.
    - Save your **Project URL**, **anon key**, and **service_role key**.

2.  **Get Database Connection String**:
    - In your Supabase project dashboard, go to `Settings` > `Database`.
    - Under `Connection string`, find the URI that looks like `postgres://...`. You will need this for PgBouncer.

3.  **Link Local Environment to Supabase**:
    ```bash
    supabase login
    supabase link --project-ref <your-project-id>
    ```

### 2. Local Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create `.env` File**:
    - Copy the example `.env.example` to a new file named `.env`.
    - Populate it with your Supabase credentials and other configuration values.

    ```ini
    # .env
    FLASK_ENV=development
    SECRET_KEY=a-very-strong-and-long-random-secret-key

    # Supabase
    SUPABASE_PROJECT_URL=https://<your-project-ref>.supabase.co
    SUPABASE_ANON_KEY=<your-supabase-anon-key>
    SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-role-key>

    # Redis
    REDIS_URL=redis://redis:6379/0

    # PgBouncer (points to your Supabase DB)
    DATABASE_URL=postgres://postgres:[YOUR-PASSWORD]@db.your-project-ref.supabase.co:6543/postgres?pgbouncer=true
    ```

    **Important**: Replace `[YOUR-PASSWORD]` in `DATABASE_URL` with your actual Supabase database password.

### 3. Running the Application

With Docker and Docker Compose, you can launch the entire stack with one command:

```bash
docker-compose up --build
```

This will:
- Build the Flask application container.
- Start the Redis service.
- Start the PgBouncer service configured to pool connections to your Supabase database.

The Flask application will be available at `http://localhost:5000`.

## Supabase Details

### Migrations

To apply the database schema, run the Supabase CLI command:

```bash
supabase db push
```

This will execute the SQL file located in `supabase/migrations/`.

### Seeding the Database

To add initial data (users, modules), you can either run the `supabase/seed.sql` file manually in the Supabase SQL Editor or use the CLI after a reset:

```bash
supabase db reset
# This command will also apply the seed file.
```

### Edge Functions

Deploy all Edge Functions using the CLI:

```bash
supabase functions deploy --no-verify-jwt
```

Here are `curl` examples for invoking each function. Replace placeholders with your project details and a valid Supabase JWT for an authenticated user.

**1. sendNotification**
```bash
curl -X POST 'https://<project-ref>.supabase.co/functions/v1/sendNotification' \
-H "Authorization: Bearer <SUPABASE_JWT>" \
-H "Content-Type: application/json" \
-d '{ "message": "Hello from curl!", "recipient_user_id": "some-user-uuid" }'
```

**2. bulkImportEntities**
```bash
curl -X POST 'https://<project-ref>.supabase.co/functions/v1/bulkImportEntities' \
-H "Authorization: Bearer <SUPABASE_JWT>" \
-H "Content-Type: text/csv" \
--data-binary '@/path/to/your/import.csv'
```

**3. webhookTrigger**
```bash
curl -X POST 'https://<project-ref>.supabase.co/functions/v1/webhookTrigger' \
-H "Authorization: Bearer <SUPABASE_JWT>" \
-H "Content-Type: application/json" \
-d '{ "event_type": "record_created", "payload": { "module": "Leads", "record_id": 123 } }'
```

**4. generateAnalytics**
```bash
curl -X POST 'https://<project-ref>.supabase.co/functions/v1/generateAnalytics' \
-H "Authorization: Bearer <SUPABASE_JWT>" \
-H "Content-Type: application/json" \
-d '{ "module_id": "some-module-uuid" }'
```
