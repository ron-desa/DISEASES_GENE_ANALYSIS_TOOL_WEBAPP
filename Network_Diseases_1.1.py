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

# Convert 'z-score' column to numeric
filtered_df['z-score'] = pd.to_numeric(filtered_df['z-score'], errors='coerce')

# Find top 5 related DOIDs for each gene based on z-score
start_time = time.time()
top_related_do_ids = {}
for gene_id in filtered_df['gene identifier'].unique():
    gene_df = df[df['gene identifier'] == gene_id]  # Use original DataFrame df
    gene_df['z-score'] = pd.to_numeric(gene_df['z-score'], errors='coerce')  # Convert z-score to numeric
    top_related_do_ids[gene_id] = gene_df.nlargest(5, 'z-score')['disease identifier'].tolist()
print(f"Time taken to find top 5 related DOIDs: {time.time() - start_time:.2f} seconds")



# Add edges between genes and top 5 related DOIDs
start_time = time.time()
for gene_id, related_do_ids in top_related_do_ids.items():
    for do_id in related_do_ids:
        G.add_edge(gene_id, do_id)
print(f"Time taken to add edges for top related DOIDs: {time.time() - start_time:.2f} seconds")

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
