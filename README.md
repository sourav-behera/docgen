# DocGen - Context Aware Documentation Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-powered documentation generation tool that automatically analyzes code repositories and generates comprehensive technical documentation using advanced language models and semantic code analysis.

## 🚀 Features

- **Automated Code Analysis**: Analyzes source code using ctags and semantic indexing with cocoindex
- **AI-Powered Documentation**: Generates comprehensive documentation using Google's Gemini AI
- **Multi-Language Support**: Supports Python, JavaScript, TypeScript, Java, C/C++, and more
- **Git Integration**: Seamlessly clones and analyzes remote repositories
- **Semantic Search**: Uses vector embeddings to find related code patterns and functions
- **Function Detection**: Automatically detects and analyzes function calls and dependencies
- **Comprehensive Output**: Generates detailed markdown documentation with examples and best practices

## 📋 Requirements

- Python 3.8 or higher
- Universal ctags (for code analysis)
- PostgreSQL with pgvector extension (for semantic indexing)
- Google Gemini API key

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd docgen
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ctags:**
   - **Ubuntu/Debian:** `sudo apt-get install universal-ctags`
   - **macOS:** `brew install universal-ctags`
   - **Windows:** Download from [ctags.io](https://ctags.io/)

4. **Set up PostgreSQL with pgvector:**
   ```bash
   # Install PostgreSQL and the pgvector extension
   # Configure your database connection in the environment variables
   ```

5. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   COCOINDEX_DATABASE_URL=your_postgres_connection_url
   ```

## Usage

### Basic Usage

Generate documentation for a Git repository:

```bash
python src/main.py --repo https://github.com/user/repository.git
```

### Command Line Options

- `--repo`: **Required** - URL or path to the Git repository to analyze

### Example

```bash
# Analyze a GitHub repository
python src/main.py --repo https://github.com/microsoft/vscode.git

# Analyze a local repository
python src/main.py --repo /path/to/local/repo
```

## Architecture

### Core Components

1. **CLI Interface** (`cli.py`)
   - Command-line argument parsing
   - Main entry point for the application

2. **Git Operations** (`git_operations.py`)
   - Repository cloning and updating
   - Repository validation and management

3. **Code Indexer** (`indexer.py`)
   - Semantic code indexing using sentence transformers
   - Vector database integration with PostgreSQL/pgvector
   - Code chunking and embedding generation

4. **Function Detection** (`ctags_function_detector.py`)
   - Static code analysis using ctags
   - Function and method detection across multiple languages
   - Cross-reference analysis

5. **Documentation Generator** (`doc_generator.py`)
   - Orchestrates the documentation generation process
   - Combines code analysis with semantic search results

6. **LLM Integration** (`llm.py`)
   - Google Gemini AI integration
   - Prompt engineering for documentation generation
   - Response formatting and file output

### Workflow

1. **Repository Processing**: Clone or update the target repository
2. **Code Indexing**: Analyze and index code files using semantic embeddings
3. **Function Detection**: Extract functions, methods, and classes using ctags
4. **Context Gathering**: Find related code patterns using semantic search
5. **Documentation Generation**: Generate comprehensive documentation using AI
6. **Output**: Save formatted markdown documentation

## 📁 Project Structure

```
docgen/
├── src/
│   ├── main.py                    # Entry point
│   ├── cli.py                     # Command-line interface
│   ├── git_operations.py          # Git repository handling
│   ├── indexer.py                 # Code indexing and search
│   ├── ctags_function_detector.py # Function detection
│   ├── doc_generator.py           # Documentation orchestration
│   ├── llm.py                     # AI integration
│   └── tmp/                       # Temporary analysis files
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Configuration

### Supported File Types

- **Python**: `.py`
- **JavaScript/TypeScript**: `.js`, `.jsx`, `.ts`, `.tsx`
- **Java**: `.java`
- **C/C++**: `.c`, `.cpp`, `.h`, `.hpp`
- **Documentation**: `.md`, `.txt`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `POSTGRES_HOST` | PostgreSQL host | No (default: localhost) |
| `POSTGRES_PORT` | PostgreSQL port | No (default: 5432) |
| `POSTGRES_DB` | Database name | No (default: docgen) |
| `POSTGRES_USER` | Database username | No |
| `POSTGRES_PASSWORD` | Database password | No |

## 📊 Output Format

The generated documentation includes:

1. **Overview**: High-level description of the codebase
2. **Architecture**: System structure and organization
3. **Key Components**: Main functions, classes, and modules
4. **Dependencies**: External libraries and frameworks
5. **Functionality**: Detailed logic and algorithm explanations
6. **Usage Examples**: Code examples and API usage
7. **Error Handling**: Exception handling patterns
8. **Performance Considerations**: Optimization insights
9. **Integration Points**: System interaction patterns
10. **Improvement Suggestions**: Recommendations for enhancement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the existing issues in the repository
2. Create a new issue with detailed information about your problem
3. Include relevant logs and error messages

## 🔮 Future Enhancements

- [ ] Support for more programming languages
- [ ] Integration with additional AI models
- [ ] Real-time documentation updates
- [ ] Plugin system for custom analyzers
- [ ] Web interface for documentation viewing
- [ ] API documentation generation
- [ ] Code quality metrics integration

---

**DocGen** - Making code documentation effortless with AI 🤖✨