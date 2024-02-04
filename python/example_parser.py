# example_parser.py
import ast
import sys
import json

def parse_python_code_to_ast(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read(), filename=file_path)
        # Implement your logic to convert the AST tree to a graph representation
        # For simplicity, let's just return the AST dump
        return ast.dump(tree)

if __name__ == "__main__":
    file_path = sys.argv[1]
    ast_data = parse_python_code_to_ast(file_path)
    print(json.dumps({"ast": ast_data}))
