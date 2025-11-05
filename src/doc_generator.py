import cocoindex
import os
from ctags_function_detector import function_detector
from indexer import search
from llm import generate_documentation, save_documentation

def doc_generator(project_path: str, src_file: str, target_dir: str="") -> str:
    """
    Generate comprehensive documentation for a source file.
    
    Args:
        project_path (str): Path to the project root
        src_file (str): Path to the source file to document
        target_dir (str): Target directory for analysis (optional)
    """
    function_calls = function_detector(project_path, target_dir, src_file)
    code_chunk: str = ""
    
    # Read the main source file (limit to reasonable size)
    with open(src_file, 'r') as file:
        content = file.read()
        code_chunk = content[:min(5000, len(content))]
        file.close() 
    
    # Add similar function chunks from the codebase
    if function_calls:
        for function_name in function_calls:
            try:
                query_output: cocoindex.QueryOutput = search(function_name)
                code_chunk += f"\n// Similar Function chunks in usersapce: {function_name}\n"
                for result in query_output.results:
                    # Add each result's code
                    if "code" in result:
                        code_chunk += result["code"]
            except Exception as e:
                print(f"Error searching for function {function_name}: {str(e)}")
                continue
    
    # Generate documentation using LLM
    print("Generating documentation...")
    documentation = generate_documentation(code_chunk)
    
    # Save documentation to file
    output_filename = os.path.splitext(os.path.basename(src_file))[0] + "_documentation.md"
    output_path = os.path.join(os.path.dirname(src_file), output_filename)
    save_documentation(documentation, output_path)
    
    print(f"Documentation generated and saved to: {output_path}")
    return documentation
