# goit-cs-hw-06

Woolf University. GoIT Neoversity. Computer Systems. Homework #6

## Project Description

Web application with HTTP server and Socket server for processing form messages and saving them to MongoDB.

### Main Components:

1. **HTTP Server** (port 3000) - serves web pages and static resources
2. **Socket Server** (port 5000) - receives form data via UDP protocol
3. **MongoDB** - stores messages with timestamps

## Project Structure

```
goit-cs-hw-06/
├── main.py              # Main file with HTTP and Socket servers
├── Dockerfile           # Docker image configuration
├── docker-compose.yaml  # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── front/              # Static files
    ├── index.html      # Home page
    ├── message.html    # Page with form
    ├── error.html      # 404 error page
    ├── style.css       # CSS styles
    └── logo.png        # Logo
```

## Running the Project

### Using Docker Compose (recommended):

```bash
docker-compose up
```

Or in detached mode:

```bash
docker-compose up -d
```

### Stop:

```bash
docker-compose down
```

### Stop with volume removal:

```bash
docker-compose down -v
```

## Application Access

After launching, the application will be available at:

-   Home page: http://localhost:3000
-   Message submission form: http://localhost:3000/message.html

## MongoDB Data Format

Messages are stored in the `messages_db` database in the `messages` collection in the following format:

```json
{
    "date": "2025-11-15 20:20:58.020261",
    "username": "krabaton",
    "message": "First message"
}
```

## Checking Data in MongoDB

Connect to MongoDB container:

```bash
docker exec -it <mongodb_container_id> mongosh
```

View messages:

```javascript
use messages_db
db.messages.find().pretty()
```

## Technical Details

-   **HTTP Server**: uses built-in Python `http.server` modules
-   **Socket Server**: uses UDP protocol for receiving data
-   **Multithreading**: HTTP and Socket servers run in different threads
-   **MongoDB**: data is stored outside the container thanks to Docker volumes
-   **Ports**:
    -   3000: HTTP server
    -   5000: Socket server (UDP)
    -   27018: MongoDB (mapped to avoid conflicts)

## Requirements

-   Docker
-   Docker Compose

## Implementation Features

1. All servers are launched from a single `main.py` file
2. HTTP and Socket servers run in different threads
3. All static resources are handled (CSS, PNG)
4. On 404 error, error.html page is returned
5. MongoDB data is stored in a volume, so it persists after container restart
