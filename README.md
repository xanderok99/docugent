# 🎤 API Conference AI Agent

A comprehensive AI assistant for the API Conference Lagos 2025 community, built with Google ADK and FastAPI. This agent helps conference attendees with navigation, speaker information, schedule management, and general support for the event taking place on July 18th & 19th, 2025 at The Zone in Gbagada, Lagos.

## 🌟 Features

### 🤖 AI Assistant - Ndu
- **Personal AI Guide**: Meet Ndu (short for Ndumodu, meaning "guide" in Igbo), your expressive Nigerian AI assistant
- **Nigerian Flair**: Speaks with local slang and cultural context while remaining professional
- **Smart Conversations**: Powered by Google ADK with Gemini 2.5 Flash model
- **Session Management**: Maintains conversation context across interactions

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

### 🌐 Web Scraping
- **Real-time Data**: Fetch latest information from apiconf.net
- **Dynamic Updates**: Get current speaker information and schedule changes
- **Content Extraction**: Parse and format web content for easy consumption

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
│   │   ├── apiconf_agent.py          # Main agent implementation (Ndu)
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
│   ├── services/
│   │   └── web_scraping_service.py   # Web scraping functionality
│   └── api/
│       └── v1/
│           └── agents_router.py      # FastAPI endpoints
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.tsx              # Chat interface
│   │   │   ├── Sidebar.tsx           # Navigation sidebar
│   │   │   └── TypingIndicator.tsx   # Loading animations
│   │   ├── App.tsx                   # Main React app
│   │   └── main.tsx                  # React entry point
│   ├── package.json                  # Frontend dependencies
│   └── vite.config.ts                # Vite configuration
├── data/
│   ├── speakers.json                 # Speaker information
│   └── schedule.json                 # Event schedule
├── docker/
│   ├── backend/
│   │   └── Dockerfile                # Backend container
│   └── nginx/
│       ├── Dockerfile                # Nginx container
│       └── nginx.conf                # Nginx configuration
├── pyproject.toml                    # Python dependencies
├── docker-compose.yml                # Container orchestration
├── env.example                       # Environment variables template
├── main.py                           # FastAPI application entry
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- Node.js 18+ (for frontend)
- Poetry (for Python dependency management)
- Docker & Docker Compose (recommended)
- Google API Key (for Google ADK and Maps)

### Option 1: Docker (Recommended)

This is the easiest way to get started:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd apiconf-agent
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - **Frontend**: http://localhost
   - **API Docs**: http://localhost/docs
   - **Health Check**: http://localhost/api/v1/agents/health

### Option 2: Local Development

1. **Clone and set up backend**
   ```bash
   git clone <repository-url>
   cd apiconf-agent
   cp env.example .env
   poetry install
   ```

2. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

3. **Configure your API keys**
   ```bash
   # In your .env file:
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   DATABASE_URL=postgresql://user:password@localhost/apiconf_agent
   SECRET_KEY=your-secret-key-here
   ```

4. **Run the applications**
   ```bash
   # Terminal 1 - Backend
   poetry run python main.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

## 📚 API Documentation

### Endpoints

#### Chat with Ndu (AI Agent)
```http
POST /api/v1/agents/chat
```

**Request Body:**
```json
{
  "message": "How do I get to The Zone from Ikeja?",
  "user_id": "user123",
  "session_id": "session456"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Omo, that's a good question! To get to The Zone from Ikeja...",
  "user_id": "user123",
  "session_id": "session456",
  "confidence": 0.9,
  "metadata": {
    "user_id": "user123",
    "session_id": "session456",
    "timestamp": 1703123456.789,
    "tools_used": []
  }
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

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost/docs
- **ReDoc**: http://localhost/redoc

## 🛠️ Development

### Project Structure

The project follows a modular architecture:

- **`app/agents/`**: AI agent implementation (Ndu) and tools
- **`app/config/`**: Configuration and settings management
- **`app/schemas/`**: Pydantic models for API requests/responses
- **`app/api/`**: FastAPI routes and endpoints
- **`app/services/`**: Business logic and external service integrations
- **`frontend/`**: React application with TypeScript
- **`data/`**: Static data files (speakers, schedule)

### Adding New Tools

1. Create a new tool file in `app/agents/tools/`
2. Implement your tool functions following Google ADK conventions
3. Register the tool in `app/agents/apiconf_agent.py`
4. Update the agent instructions if needed

Example tool:
```python
# app/agents/tools/my_tool.py
from google.adk.tools import FunctionTool

def my_tool_function(param: str, **kwargs) -> Dict[str, Any]:
    """My custom tool function."""
    return {
        "success": True,
        "result": f"Processed: {param}"
    }

def get_my_tools() -> List[FunctionTool]:
    """Get my custom tools."""
    return [
        FunctionTool(
            name="my_tool",
            description="A custom tool for processing data",
            function=my_tool_function
        )
    ]
```

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google ADK API key | Yes | - |
| `GOOGLE_MODEL_NAME` | Google model to use | No | gemini-2.5-flash |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | Yes | - |
| `DATABASE_URL` | PostgreSQL database URL | Yes | - |
| `REDIS_URL` | Redis connection URL | No | redis://localhost:6379/0 |
| `CONFERENCE_VENUE_NAME` | Conference venue name | Yes | - |
| `CONFERENCE_VENUE_ADDRESS` | Venue address | Yes | - |
| `CONFERENCE_VENUE_COORDINATES` | Venue coordinates (lat,lng) | Yes | - |
| `CONFERENCE_DATES` | Conference dates | Yes | - |
| `SUPPORT_PHONE` | Support phone number | Yes | - |
| `SUPPORT_EMAIL` | Support email | Yes | - |
| `SECRET_KEY` | Application secret key | Yes | - |
| `CORS_ORIGINS` | Allowed CORS origins | No | ["http://localhost:3000"] |

## 🧪 Testing

### Run Tests
```bash
poetry run pytest
```

### Run with Coverage
```bash
poetry run pytest --cov=app
```

### Frontend Testing
```bash
cd frontend
npm run lint
```

## 🚀 Deployment

### Docker Deployment

1. **Build production images**
   ```bash
   docker-compose -f docker-compose.yml build
   ```

2. **Run in production mode**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

### Environment Configuration

For production deployment, ensure you have:

- **Database**: PostgreSQL instance
- **Redis**: Redis instance for caching
- **API Keys**: Valid Google ADK and Maps API keys
- **SSL**: HTTPS certificates for production
- **Domain**: Configured domain name

## 📊 Monitoring

The application includes comprehensive logging and monitoring:

- **Structured Logging**: All operations are logged with context
- **Health Checks**: Built-in health check endpoints
- **Performance Metrics**: Request processing time headers
- **Error Handling**: Graceful error handling with fallback options
- **Session Management**: Conversation context tracking

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
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following Google ADK conventions
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript**: Use ESLint and Prettier
- **Google ADK**: Follow Google ADK conventions for agent development

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Phone**: Check your `.env` file for the support phone number
- **Email**: Check your `.env` file for the support email
- **Documentation**: Visit `/docs` when the server is running
- **AI Assistant**: Chat with Ndu directly through the application

## 🎯 Roadmap

- [ ] Real-time session updates via WebSockets
- [ ] Integration with conference registration system
- [ ] Multi-language support (Yoruba, Hausa, Igbo)
- [ ] Mobile app integration
- [ ] Advanced analytics and insights
- [ ] Integration with social media platforms
- [ ] Voice interface for Ndu
- [ ] Offline mode for basic functionality

---

**Built with ❤️ for the API Conference community in Nigeria**

*Meet Ndu - Your AI guide for API Conference Lagos 2025! 🎤✨* 