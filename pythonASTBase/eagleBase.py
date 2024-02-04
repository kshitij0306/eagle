import ast
import json
import pydot
import ast
import os
from graphviz import Digraph, Source
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    # Generate SVG from source code here or through an API call
    svg_content = visitor.render_graph()
    return render_template('index.html', svg_content=svg_content)


function_string = """
def complex_function(param1: int, param2: int = 10) -> int:
    '''Example function with types and default value'''
    if param1 > param2:
        result = param1 - param2
    else:
        result = param2 - param1
    for i in range(5):
        print(i)
    while param1 < param2:
        print(param1)
        param1 += 1
    try:
        risky_operation()
    except Exception as e:
        print(e)
    return result

async def async_function():
    pass

class MyClass:
    '''Example class'''
    def method(self):
        pass
"""

#parsed_ast = ast.parse(function_string)



class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = Digraph(comment='AST Graph', format='png')
        self.graph.attr(rankdir='TB', size='8,5')
        self.graph.attr('node', shape='box', style='filled', color='lightgrey', fontname='Arial')
        self.graph.attr('edge', arrowhead='vee', arrowsize='0.5', color='black')
        self.parent = None
        self.counter = 0  # Counter to ensure unique node names

    def unique_id(self, prefix):
        self.counter += 1
        return f"{prefix}_{self.counter}"

    def visit_FunctionDef(self, node):
        node_id = self.unique_id('function')
        self.graph.node(node_id, label=f"Function: {node.name}", shape='ellipse', color='lightblue')
        if self.parent:
            self.graph.edge(self.parent, node_id)
        old_parent = self.parent
        self.parent = node_id
        self.generic_visit(node)
        self.parent = old_parent

    def visit_AsyncFunctionDef(self, node):
        node_id = self.unique_id('async_function')
        self.graph.node(node_id, label=f"Async Function: {node.name}", shape='ellipse', color='lightgreen')
        if self.parent:
            self.graph.edge(self.parent, node_id)
        old_parent = self.parent
        self.parent = node_id
        self.generic_visit(node)
        self.parent = old_parent

    def visit_ClassDef(self, node):
        # Creating a unique identifier for the subgraph
        subgraph_id = f"cluster_{node.name}"  # Prefix with 'cluster_' is a convention for subgraphs in Graphviz
        label = f"Class: {node.name}"

        # Begin a subgraph for this class
        with self.graph.subgraph(name=subgraph_id) as c:
            c.attr(label=label)  # Set the label for the subgraph
            c.attr(style='filled', color='lightgrey')  # Styling for the subgraph
            c.node_attr.update(style='filled', color='lightpink')  # Default node style within the subgraph

            # Update the parent to be the subgraph itself for contained elements
            old_parent = self.parent
            self.parent = subgraph_id

            # Visit each element in the class body
            for element in node.body:
                if isinstance(element, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.visit(element)

            # Restore the previous parent once done with this class
            self.parent = old_parent

    def visit_If(self, node):
        node_id = self.unique_id('if')
        self.graph.node(node_id, label='If statement', shape='diamond', color='orange')
        if self.parent:
            self.graph.edge(self.parent, node_id)
        old_parent = self.parent
        self.parent = node_id
        self.generic_visit(node)
        self.parent = old_parent

    def visit_For(self, node):
        node_id = self.unique_id('for')
        self.graph.node(node_id, label='For loop', shape='diamond', color='orange')
        if self.parent:
            self.graph.edge(self.parent, node_id)
        old_parent = self.parent
        self.parent = node_id
        self.generic_visit(node)
        self.parent = old_parent

    def visit_While(self, node):
        node_id = self.unique_id('while')
        self.graph.node(node_id, label='While loop', shape='diamond', color='orange')
        if self.parent:
            self.graph.edge(self.parent, node_id)
        old_parent = self.parent
        self.parent = node_id
        self.generic_visit(node)
        self.parent = old_parent

    def visit_Try(self, node):
        node_id = self.unique_id('try')
        self.graph.node(node_id, label='Try block', shape='diamond', color='orange')
        if self.parent:
            self.graph.edge(self.parent, node_id)
        old_parent = self.parent
        self.parent = node_id
        self.generic_visit(node)
        self.parent = old_parent

    # In your FunctionVisitor class
    def render_graph(self, filename='ast_graph'):
        self.graph.format = 'svg'
        self.graph.render(filename, view=False)
        return f"{filename}.svg"



# Define the function to read a Python file and return its AST
def get_ast_from_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
            return ast.parse(code)
    except IOError as e:
        # You could return None or raise an exception depending on how you want to handle errors
        print(f"Error reading file {filename}: {e}")
        return None

# Assuming 'code2.py' is in the same directory as this script
# Adjust the path as necessary for your file system
filename = os.path.join(os.path.dirname(__file__), 'code2.py')
parsed_ast = get_ast_from_file(filename)

# Now you can use 'parsed_ast' as needed, for example:
if parsed_ast:
    visitor = FunctionVisitor()
    visitor.visit(parsed_ast)
    svg_content = visitor.render_graph()
    # Do something with svg_content, like saving it or passing it to a web template




# Save the Dot source from the visitor to a file
dot_source = visitor.graph.source
with open('ast_graph.dot', 'w') as dotfile:
    dotfile.write(dot_source)

# Use Source from graphviz to render the PNG
source = Source(dot_source)
source.render('ast_graph', format='png', cleanup=True)  # Set cleanup=True to remove the Dot file after

# Optionally, convert the Dot source to JSON
# This will require a custom conversion function or a third-party library
# Here's a simple example of how you might start to build a conversion function:
def dot_to_json(dot_source):
    # Parse the DOT data using pydot
    graphs = pydot.graph_from_dot_data(dot_source)

    # Assuming we have a single graph
    graph = graphs[0]

    # Create a list to store JSON node objects
    nodes_json = []
    for node in graph.get_nodes():
        nodes_json.append({
            'name': node.get_name().strip('"'),
            'label': node.get_label().strip('"') if node.get_label() else None
        })

    # Create a list to store JSON edge objects
    edges_json = []
    for edge in graph.get_edges():
        edges_json.append({
            'source': edge.get_source().strip('"'),
            'target': edge.get_destination().strip('"'),
            'label': edge.get_label().strip('"') if edge.get_label() else None
        })

    # Construct the JSON structure
    graph_json = {
        'nodes': nodes_json,
        'edges': edges_json
    }

    return graph_json


# Use the function with your DOT source
ast_json = dot_to_json(dot_source)

with open('ast_graph.json', 'w') as jsonfile:
    json.dump(ast_json, jsonfile, indent=4)

if __name__ == '__main__':
    app.run(debug=True)