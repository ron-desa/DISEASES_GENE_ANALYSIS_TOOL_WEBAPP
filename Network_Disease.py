import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time

# Path to the TSV file
tsv_file_path = "/home/rounak/Desktop/human_disease_experiments_full.tsv"

# Define column headers
column_headers = ['gene identifier', 'gene name', 'disease identifier', 'disease name', 'z-score', 'confidence score', 'URL']

# Read the TSV file into a pandas DataFrame with column headers
start_time = time.time()
df = pd.read_csv(tsv_file_path, sep='\t', names=column_headers)
print(f"Time taken to read TSV file: {time.time() - start_time:.2f} seconds")

# Take user input for Disease Ontology ID (DOID)
user_input_doid = input("Enter Disease Ontology ID (DOID): ")

# Filter the DataFrame based on user input DOID
start_time = time.time()
filtered_df = df[df['disease identifier'] == user_input_doid]
num_lines = filtered_df.shape[0]
print("complete data set:",df.shape[0])
print("user input:",filtered_df.shape[0])
print(f"Time taken to filter DataFrame: {time.time() - start_time:.2f} seconds")

# Remove duplicate lines
start_time = time.time()
filtered_df = filtered_df.drop_duplicates()
print(f"Time taken to remove duplicates: {time.time() - start_time:.2f} seconds")

# Construct a network graph
start_time = time.time()
G = nx.Graph()

# Add genes and diseases as nodes to the network graph
for index, row in filtered_df.iterrows():
    G.add_node(row['gene identifier'], node_type='gene')
    G.add_node(row['disease identifier'], node_type='disease')

# Add associations (edges) between genes and diseases
for index, row in filtered_df.iterrows():
    G.add_edge(row['gene identifier'], row['disease identifier'])
print(f"Time taken to construct network graph: {time.time() - start_time:.2f} seconds")

# Draw the network graph
start_time = time.time()
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold')

# Add labels for node types
labels = {node: node_type for node, node_type in nx.get_node_attributes(G, 'node_type').items()}
nx.draw_networkx_labels(G, pos, labels=labels)

# Show the network graph
plt.title('Gene-Disease Associations Network')
plt.show()
print(f"Time taken to draw network graph: {time.time() - start_time:.2f} seconds")
