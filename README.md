# WhatsApp Chat Analyzer

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

A powerful Streamlit application that analyzes WhatsApp chat exports to provide detailed insights and visualizations about your messaging patterns.

## Features

- **Comprehensive Statistics**:
  - Total messages sent
  - Total words used
  - Media files shared
  - Links exchanged

- **Temporal Analysis**:
  - Monthly message timeline
  - Daily activity patterns
  - Weekly activity heatmap
  - Busiest days and months

- **User Insights**:
  - Most active users
  - Individual user statistics
  - Comparison with group averages

- **Content Analysis**:
  - Word cloud visualization
  - Most common words
  - Emoji usage statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Export your WhatsApp chat:
   - Open WhatsApp → Select chat → More options → Export chat (without media)

2. Run the analyzer:
```bash
streamlit run app.py
```

3. In the web interface:
   - Upload your exported chat file
   - Select a user or "Overall" for group analysis
   - Click "Show Analysis" to view insights

## Technical Details

**Core Technologies**:
- Python 3.8+
- Streamlit (Web Interface)
- Pandas (Data Processing)
- Matplotlib/Seaborn (Visualizations)
- WordCloud (Text Analysis)
- Emoji/URLExtract (Content Parsing)

**File Structure**:
- `app.py` - Main application logic
- `helper.py` - Analysis functions
- `preprocessor.py` - Data cleaning and preparation
- `stop_hinglish.txt` - Stop words for text processing

## Screenshots

(Add screenshots of the interface here)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

MIT License - See LICENSE file for details
