# LinkedIn Connection Note Generator

A Python application that automates the generation and evaluation of personalized LinkedIn connection notes. The application scrapes LinkedIn profiles, generates customized connection requests using OpenAI's GPT models, evaluates the quality of these notes, and provides comprehensive metrics on their effectiveness.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Testing Suite Metrics](#testing-suite-metrics)
- [Project Structure](#project-structure)
- [Additional Information](#additional-information)

## Features

- **LinkedIn Profile Scraping**: Fetches profile data including name, headline, summary, experience, education, and skills.
- **Personalized Note Generation**: Creates customized connection requests using LangChain and OpenAI's GPT-4.
- **Note Evaluation**: Assesses the quality of the generated notes based on length, specificity, and tone using VADER sentiment analysis.
- **Automated Testing**: Comprehensive test suite to ensure reliability and correctness.
- **Metrics Reporting**: Provides detailed metrics on the evaluation of generated notes.

## Prerequisites

- **Python 3.12** or higher
- **LinkedIn Account**: For accessing LinkedIn profiles.
- **OpenAI API Key**: To utilize OpenAI's language models.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/linkedin-connection-note-generator.git
    cd linkedin-connection-note-generator
    ```

2. **Create a Virtual Environment**

    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    Ensure that `requirements.txt` contains all necessary packages. Here's an example:

    ```plaintext
    linkedin-api==2.1.6
    langchain==0.3.31
    langchain-community==0.3.15
    langchain-text-splitters==0.3.5
    langsmith==0.1.125
    python-dotenv==1.0.0
    openai==0.27.0
    pytest==7.2.2
    vaderSentiment==3.3.2
    ```

    Install the dependencies using:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` File**

    In the root directory of the project, create a file named `.env` and populate it with the following variables:

    ```dotenv
    LINKEDIN_SESSION_COOKIE=your_linkedin_session_cookie
    OPENAI_API_KEY=your_openai_api_key
    LINKEDIN_USERNAME=your_linkedin_username
    LINKEDIN_PASSWORD=your_linkedin_password
    ```

2. **Obtaining the LinkedIn Session Cookie**

    The `LINKEDIN_SESSION_COOKIE` is required for authenticated scraping of LinkedIn profiles. Here's how to obtain it:

    - **Log in to LinkedIn**: Open your web browser and log in to your LinkedIn account.

    - **Access Developer Tools**:
        - Right-click on the page and select "Inspect" or press `Ctrl+Shift+I` (`Cmd+Option+I` on Mac).
        - Navigate to the "Network" tab.

    - **Find the Session Cookie**:
        - Refresh the LinkedIn page to capture network activity.
        - In the "Network" tab, filter by "Cookies" or look for network requests related to `linkedin.com`.
        - Locate the `li_at` cookie, which represents your session cookie.

    - **Copy the Cookie Value**:
        - Right-click on the `li_at` cookie and select "Copy Value".
        - Paste this value into your `.env` file under `LINKEDIN_SESSION_COOKIE`.

    **Note**: Be cautious with your session cookie as it grants access to your LinkedIn account. Do not share it and consider using environment variables or secure storage mechanisms to protect it.

## Usage

1. **Prepare the Configuration File**

    Create a `linkedin_profiles.json` file in the root directory with the following structure, listing all LinkedIn profile URLs you want to process:

    ```json
    {
        "profile_urls": [
            "https://linkedin.com/in/example1",
            "https://linkedin.com/in/example2"
            // Add more profile URLs as needed
        ]
    }
    ```

2. **Run the Application**

    Execute the main script to generate and evaluate connection notes:

    ```bash
    python generate_and_evaluate_notes.py
    ```

    This script will:

    - Authenticate with LinkedIn using provided credentials.
    - Scrape each profile listed in `linkedin_profiles.json`.
    - Generate a personalized connection note.
    - Evaluate the note based on defined metrics.
    - Save the results to `connections_notes.json`.

## Running Tests

A comprehensive test suite ensures that all components of the application function correctly. To run the tests:

1. **Ensure All Dependencies Are Installed**

    Make sure you have installed all required packages as specified in `requirements.txt`.

2. **Run the Test Suite**

    From the root directory of the project, execute:

    ```bash
    python -m unittest discover -s tests
    ```

    This command discovers and runs all test cases located in the `tests/` directory.

## Testing Suite Metrics

After running the tests, you will receive a summary of evaluation metrics. An example output might look like:

INFO:main:Processed 11 profiles
INFO:main:Successful Evaluations:
length_ok: 3
specific_details_ok: 4
tone: 11
professional text: 11
INFO:main:Failed Evaluations:
length_ok: 8
specific_details_ok: 7
tone: 0
professional text: 0


### Metric Descriptions

- **Processed Profiles**: Total number of LinkedIn profiles evaluated.
- **Successful Evaluations**:
  - `length_ok`: Number of notes that met the length requirement.
  - `specific_details_ok`: Number of notes that included 1-2 specific details from the profile.
  - `tone`: Number of notes with an appropriate tone as determined by sentiment analysis.
  - `professional text`: Number of notes that maintained a professional and friendly tone without emojis or hashtags.
- **Failed Evaluations**:
  - `length_ok`: Number of notes that did not meet the length requirement.
  - `specific_details_ok`: Number of notes that did not include the required specific details.
  - `tone`: Number of notes that failed the tone check.
  - `professional text`: Number of notes that contained emojis or hashtags.

## Project Structure
```
madkudu/
├── .env
├── linkedin_prfiles.json
├── generate_and_evaluate_notes.py
├── requirements.txt
├── connection_notes.json
├── evaluation.py
├── linkedin_utils.py
├── note_generator.py
└── tests/
      ├── init.py
      ├── test_evaluation.py
      ├── test_linkedin_utils.py
      └── test_note_generator.py
```

### File Descriptions

- **`.env`**: Environment variables for sensitive information.
- **`config.json`**: Configuration file containing LinkedIn profile URLs.
- **`linkedin_note_generator.py`**: Main script to generate and evaluate connection notes.
- **`requirements.txt`**: Python dependencies.
- **`results.json`**: Output file with profile data, generated notes, and evaluation metrics.
- **`evaluation.py`**: Module containing evaluation functions.
- **`linkedin_utils.py`**: Module for LinkedIn authentication and profile scraping.
- **`note_generator.py`**: Module for generating personalized connection notes.
- **`tests/`**: Directory containing unit and integration tests.
  - **`__init__.py`**: Marks the directory as a Python package.
  - **`test_evaluation.py`**: Tests for evaluation functions.
  - **`test_linkedin_utils.py`**: Tests for LinkedIn utilities.
  - **`test_note_generator.py`**: Tests for note generation.

## Additional Information

- **Environment Variables Security**: Ensure that your `.env` file is included in `.gitignore` to prevent sensitive information from being committed to version control.

- **Logging**: The application uses Python’s `logging` module to provide detailed information about its operation. Adjust the logging level as needed for your use case.

- **Error Handling**: The application includes basic error handling. Consider enhancing it to cover more edge cases and provide more informative error messages.

- **Dependencies Compatibility**: Ensure that the versions of `langchain`, `langchain-community`, `langchain-text-splitters`, and `langsmith` in your `requirements.txt` are compatible to prevent module import errors.

- **Virtual Environment**: Always activate your virtual environment before running the application or tests to ensure that dependencies are correctly managed.

---

By following the steps outlined in this README, you can set up, run, and test the LinkedIn Connection Note Generator effectively. Feel free to contribute or raise issues for further improvements or bug fixes.
