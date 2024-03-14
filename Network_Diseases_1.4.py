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

# Add associations (edges) between genes and diseases
for index, row in filtered_df.iterrows():
    G.add_edge(row['gene identifier'], row['disease identifier'])

# Convert 'z-score' column to numeric
filtered_df['z-score'] = pd.to_numeric(filtered_df['z-score'], errors='coerce')

# Find top 5 related DOIDs for each gene based on z-score
start_time = time.time()
top_related_do_ids = {}
for gene_id in filtered_df['gene identifier'].unique():
    gene_df = df[df['gene identifier'] == gene_id].copy()  # Make a copy to preserve original DataFrame
    gene_df['z-score'] = pd.to_numeric(gene_df['z-score'], errors='coerce')  # Convert z-score to numeric
    top_related_do_ids[gene_id] = gene_df.nlargest(5, 'z-score')[['disease identifier', 'disease name']].values.tolist()
print(f"Time taken to find top 5 related DOIDs: {time.time() - start_time:.2f} seconds")

# Add edges between genes and top 5 related DOIDs
start_time = time.time()
for gene_id, related_do_ids in top_related_do_ids.items():
    for do_id, do_name in related_do_ids:
        G.add_node(do_id, node_type='disease', disease_name=do_name)
        G.add_edge(gene_id, do_id)
print(f"Time taken to add edges for top related DOIDs: {time.time() - start_time:.2f} seconds")

# Draw the network graph
start_time = time.time()
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Highlight search DOID node in red
nx.draw_networkx_nodes(G, pos, nodelist=[user_input_doid], node_color='red', node_size=700)

# Highlight top 5 DOID nodes in green
top_5_doids = set()
for related_do_ids in top_related_do_ids.values():
    top_5_doids.update([doid[0] for doid in related_do_ids])
nx.draw_networkx_nodes(G, pos, nodelist=list(top_5_doids - {user_input_doid}), node_color='green', node_size=700)

# Draw other nodes
nx.draw_networkx_nodes(G, pos, nodelist=[node for node in G.nodes() if node not in {user_input_doid} | top_5_doids], node_color='skyblue', node_size=500)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# Add node labels (gene names, disease names)
node_labels = {node: G.nodes[node].get('gene_name', G.nodes[node].get('disease_name', '')) for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color='orange', font_family='sans-serif', font_weight='bold')

# Show the network graph
plt.title('Gene-Disease Associations Network')
plt.axis('off')
plt.show()
nx.write_graphml(G, 'PD_Experiments_network_graph.graphml')
plt.savefig('PD_Experiments_network_graph.png')
print(f"Time taken to draw network graph: {time.time() - start_time:.2f} seconds")
