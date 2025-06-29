# CrewAI Multi-Agent Project Documentation System

A sophisticated multi-agent system that processes uploaded media files (audio/video) and generates professional project documentation through specialized agents working in sequence.

## Overview

This system uses CrewAI to orchestrate multiple specialized agents that work together to:

1. Handle file uploads and validation
2. Process media files and extract transcriptions
3. Store transcriptions in vector database
4. Generate comprehensive project documentation
5. Export documents in various formats (PDF, DOCX, HTML, JSON)

## Technical Stack

- **Backend**: Python (>=3.10), CrewAI, FastAPI
- **Frontend**: HTML Templates with Jinja2
- **Vector Database**: Local storage with vector embeddings
- **LLM Integration**: Configurable LLM service
- **Media Processing**: FFmpeg, Whisper

## Prerequisites

- Python 3.10 or higher
- FFmpeg installed on your system
- Virtual environment (recommended)

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd crewai-project-documentation
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root with the following variables:

```
# Application Settings
DEBUG=True
LOG_LEVEL=INFO

# File Upload Settings
MAX_FILE_SIZE=500MB
TEMP_FILE_RETENTION=24  # hours
```

5. **Install FFmpeg**

Follow the instructions for your operating system to install FFmpeg:
- Windows: Download from [FFmpeg's website](https://ffmpeg.org/download.html) or install via Chocolatey
- Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent
- Mac: `brew install ffmpeg`

## Running the Application

1. **Start the FastAPI backend**

```bash
uvicorn main:app --reload
```

2. **Access the application**

Open your browser and go to:
- Web Interface: http://localhost:8000
- API docs: http://localhost:8000/docs

## System Architecture

The system consists of five specialized agents:

### 1. File Upload Handler Agent
- Validates file formats and integrity
- Generates unique file IDs
- Stores files temporarily for processing

### 2. Media Processing Agent
- Extracts audio from video files using FFmpeg
- Transcribes audio using Whisper
- Handles multiple languages and speaker diarization

### 3. Vector Storage Agent
- Stores transcriptions with vector embeddings
- Manages local storage of processed data
- Creates metadata for each transcription

### 4. Documentation Generator Agent
- Retrieves transcriptions from storage
- Analyzes content for project requirements
- Generates comprehensive project documentation

### 5. Document Download Agent
- Generates downloadable documents (PDF, DOCX, HTML, JSON)
- Manages temporary file creation
- Provides download links through the API

## API Endpoints

- `POST /upload`: Upload media files for processing
- `GET /status/{file_id}`: Check processing status
- `GET /documentation/{file_id}`: Retrieve generated documentation
- `GET /download/{file_id}`: Download documentation in various formats

## Folder Structure

```
crewai_project/
├── main.py                          # FastAPI entry point
├── app.py                           # Application logic
├── requirements.txt                 # Dependencies
├── .env                            # Environment variables
├── agents/
│   ├── file_upload_agent.py        # Agent 1
│   ├── media_processing_agent.py    # Agent 2
│   ├── vector_storage_agent.py     # Agent 3
│   ├── documentation_agent.py      # Agent 4
│   └── download_agent.py           # Agent 5
├── services/
│   ├── llm_service.py             # LLM integration
│   ├── local_storage_service.py    # Local storage
│   └── media_processor.py         # FFmpeg/Whisper
├── models/
│   ├── schemas.py                  # Pydantic models
│   └── database.py                 # Database configurations
├── utils/
│   ├── config.py                   # Configuration management
│   ├── logger.py                   # Logging setup
│   └── document_download.py        # Download utilities
├── templates/                      # HTML templates
├── static/                         # Static files
│   └── downloads/                  # Generated documents
├── temp_files/                     # Temporary file storage
└── logs/                          # Application logs
```

## Error Handling & Resilience

The system includes robust error handling:
- File validation and integrity checks
- Processing status tracking
- Detailed error logging
- Graceful failure handling
- Background task management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
