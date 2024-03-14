# Path to the TSV file
import pandas as pd

tsv_file_path = "/home/rounak/Desktop/arcived_human_disease_textmining_full.tsv"

# Path for the output XLS file
# xls_file_path = "F:\human_disease_textmining_filtered.xls"

# Read the TSV file into a pandas DataFrame
df = pd.read_csv(tsv_file_path, sep='\t')
# print(df.head(10))

# Write the DataFrame to an XLS file
# df.to_excel(xls_file_path, index=False)

filtered_df = df[df['DOID:9643'] == 'DOID:10652']
print(filtered_df.head(10))


# Define a list of desired values
# desired_values = ['DOID:10652','DOID:0080348','DOID:0110035', 'DOID:0110042','DOID:0110040','DOID:0110037','DOID:0110038','DOID:0110039','DOID:0110041','DOID:0111364','DOID:0110043','DOID:0110044','DOID:0110045','DOID:0110046','DOID:0110047','DOID:0110048','DOID:0110036','DOID:0110049','DOID:0110050','DOID:0110051']

# Filter the DataFrame based on multiple values in a specific column
# filtered_df = df[df['DOID:9643'].isin(desired_values)]

# print(filtered_df.head(10))



# Count the number of lines in the filtered DataFrame
# num_lines = filtered_df.shape[0]

# print("Number of lines in the filtered DataFrame:", num_lines)
print("complete data set",df.shape[0])
print("10652 data set",filtered_df.shape[0])

filtered_df.to_csv('filtered_data_from_archive_raw.csv', index=False)

# df.to_csv('filterd_raw.csv', index=False)


print("Filtered data has been exported to 'filtered_data.csv'.")
'''
# print(f"TSV file '{tsv_file_path}' successfully converted to XLS file '{xls_file_path}'.")
'''

'''
import os

# Get the current working directory
current_directory = os.getcwd()

# Specify the file name
file_name = 'filtered_data.csv'

# Concatenate the current directory and file name to get the file location
file_location = os.path.join(current_directory, file_name)

print("File location of the new CSV file:", file_location)
'''




