# Facebook-Sentiment-Analysis
A tool for data collection and sentiment analysis on Facebook

## Iteration 1: Requirements
### 1. Team Info

   ***Team Name:*** Facebook Sentiment Analysis
   
   ***Team Members:*** Joshua Ritter, Alessandro Rodriguez, Erick De La Rosa Campos

### 2. Vision Statement

   A tool that searches Facebook for keywords from Donaldson's client companies and analyses them to understand company sentiment for alternative powertrain.
   
### 3. Feature List
   - Gather information based on keywords
   - Get keywords straight from a file in order to add more in the future
   - Sorting of data gathered
   - UI for easy access

### 4. UML Use Case Diagram
![image](https://github.com/soot0-JoshR/Facebook-Sentiment-Analysis/blob/main/images/UML.drawio.png)

### 5. UI Sketches

  ![alt text](https://github.com/soot0-JoshR/Facebook-Sentiment-Analysis/blob/main/images/Sketchy_UI.png)
  
### 6. Key use-cases

- Searching for a company/keywords:
  - User selects companies and keywords and presses a button to get a request. Application sends warning to user
    showing amount of requests left since Facebook only allows for 200 * Number of users calls per hour. User will then either accept or decline
    and the data will be dumped to them.
- Sentiment Analysis
  - Runs sentiment analysis on text data extracted from posts and comments using the NLTK python library.
- Sorting Data
  - Sorting feedback data from sentiment analysis. Can be sorted by keyword, user/company name, date/time, and/or general sentiment.

### 7. Architecture

   Facebook's Graph API. PycURL for accesing Facebook's API. Python NLTK library for sentiment analysis.

