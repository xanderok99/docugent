# 🎤 API Conference AI Agent

A comprehensive AI assistant for the API Conference Lagos 2025 community, built with Google ADK and FastAPI. This agent helps conference attendees with navigation, speaker information, schedule management, and general support for the event taking place on July 18th & 19th, 2025 at The Zone in Gbagada, Lagos.

## 🌟 Features

### 🚌 Navigation & Transportation
- **Route Planning**: Get directions to the conference venue using Google Maps
- **Transportation Options**: Find nearby bus stops, train stations, and transport options
- **Venue Access**: Information about parking, accessibility, and venue facilities
- **Real-time Updates**: Traffic and transport information

### 🎤 Speaker Information
- **Speaker Profiles**: Detailed information about conference speakers
- **Session Details**: Find sessions by speaker, topic, or time
- **Expertise Search**: Search speakers by their areas of expertise
- **Speaker Sessions**: Get all sessions for a specific speaker

### 📅 Schedule Management
- **Full Schedule**: Complete conference schedule with session details
- **Day-by-Day View**: Filter sessions by specific days
- **Session Search**: Find sessions by title, topic, or speaker
- **Personalized Recommendations**: Get schedule recommendations based on interests and experience level

### 💬 General Support
- **FAQ Support**: Answer common conference questions
- **Venue Information**: Details about facilities and services
- **Registration Help**: Assistance with registration and ticketing
- **Emergency Contacts**: Quick access to support information

### 🔄 Fallback Support
- **Human Contact**: Always provides support phone number when AI can't help
- **Graceful Degradation**: Handles errors gracefully with helpful fallback options

## 🏗️ Architecture

```
apiconf-agent/
├── app/
│   ├── agents/
│   │   ├── apiconf_agent.py          # Main agent implementation
│   │   └── tools/
│   │       ├── navigation_tools.py   # Maps, directions, transportation
│   │       ├── speaker_tools.py      # Speaker information
│   │       ├── schedule_tools.py     # Event scheduling
│   │       └── web_scraping_tools.py # Data extraction from apiconf.net
│   ├── config/
│   │   ├── settings.py               # Environment configuration
│   │   └── logger.py                 # Logging setup
│   ├── schemas/
│   │   ├── base.py                   # Base response schemas
│   │   └── agents.py                 # Agent request/response models
│   └── api/
│       └── v1/
│           └── agents_router.py      # FastAPI endpoints
├── data/
│   ├── speakers.json                 # Speaker information
│   └── schedule.json                 # Event schedule
├── pyproject.toml                    # Dependencies
├── env.example                       # Environment variables template
├── main.py                           # FastAPI application entry
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Google API Key (for Google ADK and Maps)
- Google Maps API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd apiconf-agent
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Configure your API keys**
   ```bash
   # In your .env file:
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   CONFERENCE_VENUE_NAME="The Zone"
CONFERENCE_VENUE_ADDRESS="Plot 9, Gbagada Industrial Scheme beside UPS, Gbagada - Oworonshoki Expy, Lagos, Lagos, Nigeria 100234"
CONFERENCE_VENUE_COORDINATES="6.5481,3.3789"
CONFERENCE_DATES="July 18th & 19th, 2025"
SUPPORT_PHONE="+234-XXX-XXX-XXXX"
SUPPORT_EMAIL="support@apiconf.net"
   ```

5. **Run the application**
   ```bash
   poetry run python main.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Endpoints

#### Chat with Agent
```http
POST /api/v1/agents/chat
```

**Request Body:**
```json
{
  "message": "How do I get to the conference venue from Ikeja?",
  "user_id": "user123",
  "session_id": "session456"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "To get to the Lagos Continental Hotel from Ikeja, you can take...",
    "user_id": "user123",
    "session_id": "session456"
  },
  "message": "Message processed successfully"
}
```

#### Get Agent Status
```http
GET /api/v1/agents/status
```

#### Health Check
```http
GET /api/v1/agents/health
```

#### Conference Information
```http
GET /api/v1/agents/info
```

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠️ Development

### Project Structure

The project follows a modular architecture:

- **`app/agents/`**: AI agent implementation and tools
- **`app/config/`**: Configuration and settings management
- **`app/schemas/`**: Pydantic models for API requests/responses
- **`app/api/`**: FastAPI routes and endpoints
- **`data/`**: Static data files (speakers, schedule)

### Adding New Tools

1. Create a new tool file in `app/agents/tools/`
2. Implement your tool functions
3. Register the tool in `app/agents/apiconf_agent.py`
4. Update the agent instructions if needed

Example tool:
```python
# app/agents/tools/my_tool.py
def my_tool_function(param: str, **kwargs) -> Dict[str, Any]:
    """My custom tool function."""
    return {
        "success": True,
        "result": f"Processed: {param}"
    }
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google ADK API key | Yes |
| `GOOGLE_MODEL_NAME` | Google model to use | No (default: gemini-2.5-flash) |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | Yes |
| `CONFERENCE_VENUE_NAME` | Conference venue name | Yes |
| `CONFERENCE_VENUE_ADDRESS` | Venue address | Yes |
| `CONFERENCE_VENUE_COORDINATES` | Venue coordinates (lat,lng) | Yes |
| `SUPPORT_PHONE` | Support phone number | Yes |
| `SUPPORT_EMAIL` | Support email | Yes |

## 🧪 Testing

### Run Tests
```bash
poetry run pytest
```

### Run with Coverage
```bash
poetry run pytest --cov=app
```

## 🚀 Running with Docker (Recommended)

This is the recommended way to run the application for both development and production.

### Prerequisites

- Docker
- Docker Compose

### Setup

1.  **Create an environment file**:

    Copy the example environment file and update it with your configuration and API keys.

    ```bash
    cp env.example .env
    ```

    Make sure to fill in all the required variables in the `.env` file.

2.  **Build and run the application**:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images for the backend and frontend, and start the services. The `-d` flag can be added to run in detached mode.

3.  **Access the application**:

    Once the containers are running, you can access:
    - **Frontend Application**: [http://localhost](http://localhost)
    - **API Docs (Swagger UI)**: [http://localhost/docs](http://localhost/docs)
    - **API Docs (ReDoc)**: [http://localhost/redoc](http://localhost/redoc)

### Stopping the application

To stop the services, press `Ctrl+C` in the terminal where `docker-compose` is running, or run:

```bash
docker-compose down
```

## 📊 Monitoring

The application includes comprehensive logging and monitoring:

- **Structured Logging**: All operations are logged with context
- **Health Checks**: Built-in health check endpoints
- **Performance Metrics**: Request processing time headers
- **Error Handling**: Graceful error handling with fallback options

## 🔧 Configuration

### Logging Levels
- `DEBUG`: Detailed debug information
- `INFO`: General information (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages

### CORS Configuration
Configure allowed origins in your `.env` file:
```bash
CORS_ORIGINS=["http://localhost:3000", "https://apiconf.net"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Phone**: Check your `.env` file for the support phone number
- **Email**: Check your `.env` file for the support email
- **Documentation**: Visit `/docs` when the server is running

## 🎯 Roadmap

- [ ] Real-time session updates
- [ ] Integration with conference registration system
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Advanced analytics and insights
- [ ] Integration with social media platforms

---

**Built with ❤️ for the API Conference community in Nigeria** 