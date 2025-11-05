import cocoindex
from ctags_function_detector import function_detector
from indexer import search

def doc_generator(project_path: str, src_file: str, target_dir: str="src") -> None:
    function_calls = function_detector(project_path, target_dir, src_file)
    code_chunk: str = ""
    with open(src_file, 'r') as file:
        content = file.read()
        code_chunk = content[:min(5000, len(content))]
        file.close()
    
    if function_calls is None:
        print("No function calls detected or an error occurred.")
        return
    for function_name in function_calls:
        query_output: cocoindex.QueryOutput = search(function_name)
        code_chunk += f"\n// Similar Function chunks in usersapce: {function_name}\n"
        for result in query_output.results:
            code_chunk += result["code"]
 
    print(code_chunk)

