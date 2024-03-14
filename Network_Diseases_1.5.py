import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time

# Path to the TSV file
tsv_file_path = "/home/rounak/Desktop/human_disease_knowledge_full.tsv"

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
filtered_df = df[df['disease identifier'] == user_input_doid].copy()  # Make a copy to preserve original DataFrame
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
    G.add_node(row['gene identifier'], node_type='gene', gene_name=row['gene name'])
    G.add_node(row['disease identifier'], node_type='disease', disease_name=row['disease name'])

# Take user input for filtering option
filtering_option = input("Enter 'z-score' to filter based on z-score metric or 'all' to consider all associations: ")

# Find related DOIDs based on user's choice
if filtering_option == 'z-score':
    # Find top 5 related DOIDs for each gene based on z-score
    start_time = time.time()
    top_related_do_ids = {}
    for gene_id in filtered_df['gene identifier'].unique():
        gene_df = df[df['gene identifier'] == gene_id].copy()  # Make a copy to preserve original DataFrame
        gene_df['z-score'] = pd.to_numeric(gene_df['z-score'], errors='coerce')  # Convert z-score to numeric
        top_related_do_ids[gene_id] = gene_df.nlargest(5, 'z-score')[['disease identifier', 'disease name']].values.tolist()
    print(f"Time taken to find top 5 related DOIDs: {time.time() - start_time:.2f} seconds")

else:
    # Consider all associations between each gene and DOIDs
    start_time = time.time()
    all_related_do_ids = {}
    for gene_id in filtered_df['gene identifier'].unique():
        gene_df = df[df['gene identifier'] == gene_id].copy()  # Make a copy to preserve original DataFrame
        all_related_do_ids[gene_id] = gene_df[['disease identifier', 'disease name']].values.tolist()
    print(f"Time taken to find all related DOIDs: {time.time() - start_time:.2f} seconds")

# Add edges between genes and related DOIDs based on user's choice
start_time = time.time()
if filtering_option == 'z-score':
    for gene_id, related_do_ids in top_related_do_ids.items():
        for do_id, do_name in related_do_ids:
            G.add_node(do_id, node_type='disease', disease_name=do_name)
            G.add_edge(gene_id, do_id)
else:
    for gene_id, related_do_ids in all_related_do_ids.items():
        for do_id, do_name in related_do_ids:
            G.add_node(do_id, node_type='disease', disease_name=do_name)
            G.add_edge(gene_id, do_id)

print(f"Time taken to add edges for related DOIDs: {time.time() - start_time:.2f} seconds")

# Define the positions of the nodes using spring layout
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the network graph
plt.figure(figsize=(10, 8))  # Adjust figure size if needed

# Extract disease names from the DataFrame
disease_names = {node_id: data['disease_name'] for node_id, data in G.nodes(data=True) if data['node_type'] == 'disease'}

# Draw nodes with disease names as labels
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if node != user_input_doid], node_color='skyblue', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=[user_input_doid], node_color='red', node_size=700)
nx.draw_networkx_labels(G, pos, labels=disease_names, font_size=8, font_color='orange', font_weight='bold')

# Draw edges
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# Highlight related disease nodes for each gene with green color
if filtering_option == 'z-score':
    for gene_id, related_do_ids in top_related_do_ids.items():
        related_disease_nodes = [do_id for do_id, _ in related_do_ids]
        nx.draw_networkx_nodes(G, pos, nodelist=related_disease_nodes, node_color='green', node_size=500)


# Show the network graph
plt.title('Gene-Disease Associations Network')
plt.axis('off')
plt.show()

print(f"Time taken to draw network graph: {time.time() - start_time:.2f} seconds")
