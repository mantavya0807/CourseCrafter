# Course Scheduler

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Node](https://img.shields.io/badge/node-14.x-green)

A modern web application that leverages web scraping and natural language processing to automatically gather and process course information. Built with the MERN stack, it provides an intelligent course planning solution.

## Features

- **Automated Data Collection**
  - Web scraping using Selenium and Beautiful Soup
  - Real-time course information updates
  - Automated data cleaning and processing

- **Intelligent Processing**
  - Natural Language Processing for course description analysis
  - Course prerequisite mapping
  - Automated course categorization
  - Keyword extraction and topic modeling

- **Smart Scheduling**
  - Real-time schedule generation
  - Conflict detection and resolution
  - Prerequisite validation
  - Schedule optimization

- **Modern Web Interface**
  - Responsive React frontend
  - Interactive schedule visualization
  - Real-time updates
  - User-friendly interface

## Tech Stack

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MongoDB** - Database
- **Python** - Data processing and NLP
- **NLTK** - Natural Language Processing
- **Selenium** - Web scraping
- **Beautiful Soup** - HTML parsing

### Frontend
- **React** - UI framework
- **Material-UI** - Component library
- **Redux** - State management
- **Axios** - API client

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/course-scheduler.git
cd course-scheduler
```

2. Install Python dependencies
```bash
cd scraper
pip install -r requirements.txt
```

3. Install Node.js dependencies
```bash
# Backend dependencies
cd ../server
npm install

# Frontend dependencies
cd ../client
npm install
```

4. Set up environment variables
```bash
# In server directory, create .env:
PORT=5000
MONGODB_URI=mongodb://localhost:27017/course-scheduler
NODE_ENV=development

# In scraper directory, create .env:
CHROME_DRIVER_PATH=/path/to/chromedriver
```

5. Start the development servers
```bash
# Start backend server
cd server
npm run dev

# Start frontend server in a new terminal
cd client
npm start

# Run scraper (when needed)
cd scraper
python main.py
```

The application will be available at `http://localhost:3000`

## Project Structure

```
course-scheduler/
│
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/        # Page components
│   │   ├── redux/        # State management
│   │   └── utils/        # Utility functions
│   │
│   └── public/           # Static files
│
├── server/                # Node.js backend
│   ├── controllers/      # Request handlers
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   └── utils/           # Utility functions
│
└── scraper/              # Python scraper
    ├── processors/      # Data processors
    ├── scrapers/       # Web scrapers
    └── utils/          # Utility functions
```

## API Documentation

### Course Endpoints
- GET `/api/courses` - Get all courses
- GET `/api/courses/:id` - Get course by ID
- POST `/api/schedules` - Generate new schedule
- GET `/api/schedules/:id` - Get schedule by ID

Detailed API documentation is available in the [API.md](API.md) file.

## Data Processing Pipeline

1. **Web Scraping**
   - Course information collection
   - Schedule data gathering
   - Real-time updates

2. **Data Processing**
   - Text cleaning and normalization
   - NLP processing
   - Keyword extraction
   - Topic modeling

3. **Storage**
   - MongoDB database storage
   - Data validation
   - Indexing for quick retrieval

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Running Tests

```bash
# Backend tests
cd server
npm test

# Frontend tests
cd client
npm test

# Scraper tests
cd scraper
python -m pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [NLTK](https://www.nltk.org/) for natural language processing
- [Selenium](https://www.selenium.dev/) for web automation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [MongoDB](https://www.mongodb.com/) for database
- [Express.js](https://expressjs.com/) for backend framework
- [React](https://reactjs.org/) for frontend framework

