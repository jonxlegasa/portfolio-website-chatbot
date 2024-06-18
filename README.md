# portfolio-website-chatbot

## Overview
This project features a dynamic chatbot designed to function as a personal assistant, managing and presenting personal documents and information similar to well-known assistants like Jarvis and Cortana. By integrating with external APIs such as GitHub and LinkedIn, the chatbot provides a comprehensive overview of my professional background, portfolio, and other relevant information.

## Features
- **Resume Reader**: Automatically parses and summarizes the resume content.
- **API Integration**: Connects with GitHub and LinkedIn to fetch and display up-to-date information.
- **Interactive Chatbot**: Engages users with a conversational interface to field inquiries about my professional life and experiences.

## Installation

### Prerequisites
- Python 3.12 or newer
- Poetry for Python dependency management

### Setting Up the Project
1. **Clone the repository:**
   ```bash
   git clone https://github.com/jonxlegasa/portfolio-website-chatbot.git
   cd portfolio-website-chatbot
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

### Configuration
Create a `.env` file in the root directory and add the necessary API keys and configuration variables:
```plaintext
GITHUB_API_KEY="your_github_api_key_here"
LINKEDIN_API_KEY="your_linkedin_api_key_here"
```

## Usage
To run the project, use the following command:
```bash
poetry run run-my-project
```

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
