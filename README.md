# Review-Analyzer

## Description:
Review Analyzer is a Python script that uses OpenAI's GPT-3 API to rate and sort reviews based on sentiment analysis. The script reads review data from a CSV file, sends the data to OpenAI for analysis, and then writes the analyzed data back to a new CSV file.

## Requirements
- Python 3.6 or later
- openai package
- dotenv package
- requests package

## Installation
1. Clone the repository to your local machine.
2. Install the required packages by running the following command:
```
pip install -r requirements.txt
```
3. Create a file named .env in the root directory of the project and add your OpenAI API key to the file:
```
OPENAI_API_KEY=<your_api_key_here>
```

## Usage
1. Put your review data in a CSV file named data.csv, with columns email, review text, and date.
2. Run the script:
```
python review_analyzer.py
```

## License
- MIT license
  ([LICENSE](LICENSE) or http://opensource.org/licenses/MIT)
