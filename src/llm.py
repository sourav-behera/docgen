import os
from dotenv import load_dotenv
from google import genai
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
# Load environment variables
load_dotenv()

def generate_documentation(code_chunk: str) -> str:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    logger.info("Invoking Gemini client for documentation generation.")
    logger.debug(f"Code chunk length: {len(code_chunk)} characters")
    logger.debug(f"Code chunk preview: {code_chunk[:1000]}")  # Log first 500 characters
    prompt = f"""
    Analyze the following code and generate comprehensive technical documentation.
    
    The code may contain the main source code followed by similar function chunks from the codebase for context.
    Extract meaningful information and focus on the main code while using the similar functions as context.

    Code to analyze:
    ```
    {code_chunk}
    ```

    Please provide:
    1. **Overview**: Brief description of what this code does
    2. **Architecture**: How the code is structured and organized
    3. **Key Components**: Main functions, classes, and their purposes
    4. **Dependencies**: Important imports and external libraries used
    5. **Functionality**: Detailed explanation of the core logic and algorithms
    6. **Usage Examples**: How to use the main functions/classes (if available)
    7. **Error Handling**: Any error handling mechanisms present (if avaiable)
    8. **Performance Considerations**: Any notable performance aspects
    9. **Integration Points**: How this code interacts with other parts of the system
    10. **Potential Improvements**: Suggestions for code enhancement

    Focus on technical accuracy and provide practical insights for developers.
    Format the response in clean markdown with proper headers and code blocks.
    Ignore any irrelevant or duplicate code snippets and focus on the most meaningful parts.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        documentation = str(response)        
        logger.info("Documentation generation completed successfully.")
        return documentation
        
    except Exception as e:
        return f"Error generating documentation: {str(e)}\n\nRaw code chunk:\n\n{code_chunk}"

def save_documentation(documentation: str, output_file: str = "generated_docs.md") -> None:
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(documentation)
        print(f"Documentation saved to {output_file}")
    except Exception as e:
        print(f"Error saving documentation: {str(e)}")