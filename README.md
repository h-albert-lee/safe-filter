# Pattern Filtering Module with Streamlit UI

This repository provides a Python-based pattern filtering module designed for fast detection of sensitive patterns in text. It uses `pyahocorasick` for rapid literal matching and regular expressions for format-based matching. A simple Streamlit UI is included for managing pattern entries and testing text detection.

## Features

### Literal Matching:
- Uses `pyahocorasick` for fast scanning of literal patterns such as explicit profanities.

### Regex Matching:
- Detects various identifiers and formats (e.g., social security numbers, email addresses, passport numbers, etc.) using regular expressions.
- Multiple regex patterns can be combined to improve performance.

### External Pattern Configuration:
- All patterns are stored in a JSON file (`patterns.json`), separating the literal (e.g., swear words) and regex patterns (e.g., identifiers) with corresponding categories.

### Streamlit UI:
A user-friendly interface (`app.py`) is provided to:
- Add new patterns (both literal and regex).
- View the current pattern list.
- Test text input for pattern detection, returning whether sensitive data was detected and its category.

## Files

### `pattern_filter.py`
Contains the core filtering module which:
- Loads literal and regex patterns from `patterns.json`.
- Uses `pyahocorasick` for literal matching.
- Implements regex matching with a combined regex approach (with fallback to individual matching).

### `patterns.json`
A JSON file that holds the pattern definitions:
- **Literal patterns** are used for direct string matching (e.g., profanities).
- **Regex patterns** cover formats like identifiers and contact information.

### `app.py`
A Streamlit application that allows you to:
- Add new patterns to `patterns.json`.
- View the current list of patterns.
- Enter text for detection testing.

## Setup and Usage

### Install Dependencies:
Make sure you have Python installed. Then, install the required packages:

```bash
pip install streamlit pyahocorasick
```

### Running the Streamlit App:
Launch the UI by running:

```bash
streamlit run app.py
```

The Streamlit interface will open in your browser, allowing you to add patterns, view the current list, and test text input.

### Pattern Configuration:
The default `patterns.json` file includes sample literal patterns for profanity and regex patterns for various identifiers. Feel free to modify or extend this file to suit your needs.

## Notes
- The combined regex matching approach is implemented to enhance performance. If testing shows no significant performance improvement, you can easily revert to the original individual regex matching logic.
- Ensure to thoroughly test regex patterns, as formats for identifiers can be complex and may require fine-tuning for your specific application.
