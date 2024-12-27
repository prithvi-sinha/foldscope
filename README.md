# Foldscope Image Analysis

A Python-based program that assists users in analyzing microscope images captured using Foldscope. The program leverages OpenAI's powerful image recognition and natural language capabilities to identify, classify, and provide detailed insights about microorganisms, structures, and patterns observed in microscopic images.

## Features

### 1. Image Analysis
- Upload and process images captured using Foldscope
- Utilizes OpenAI's Vision API for advanced image recognition
- Provides detailed classification of microorganisms and structures
- Identifies key characteristics and notable features

### 2. Educational Insights
- Generates natural language explanations of findings
- Offers detailed descriptions of observed structures
- Provides context for biological and microscopic features
- Includes suggestions for further learning and exploration

### 3. Technical Details
- Built with Python
- Uses OpenAI's API for image analysis
- Implements environment variables for secure API key management
- Supports high-resolution image processing

## Getting Started

### Prerequisites
- Python 3.x
- OpenAI API key
- Python packages:
  - openai
  - python-dotenv

### Installation

1. Clone the repository:
```bash
git clone https://github.com/prithvi-sinha/foldscope.git
cd foldscope
```

2. Install required packages:
```bash
pip install openai python-dotenv
```

3. Create a `.env` file in the project root and add your OpenAI API key and Assistant ID:
```
OPENAI_API_KEY=your_api_key_here
ASSISTANT_ID=your_assistant_id_here
```

### Usage

1. Place your Foldscope images in the `images/` directory

2. Run the program:
```bash
python main.py
```

3. The program will analyze the image and provide:
   - Classification of the observed specimen
   - Detailed description of key features
   - Educational insights and context
   - Suggestions for further learning

## Future Enhancements

- [ ] Crowdsourced data sharing capabilities
- [ ] Interactive learning features and quizzes
- [ ] Environmental context analysis
- [ ] Integration with a shared database
- [ ] Enhanced image preprocessing
- [ ] Support for batch processing multiple images

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the Vision API
- Foldscope community for inspiration and support
