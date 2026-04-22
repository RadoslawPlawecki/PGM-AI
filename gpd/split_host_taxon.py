import pandas as pd


file_path = "gpd/data/02_gpd_filtered.csv"
df = pd.read_csv(file_path, delimiter=';')


def deduplicate_taxon(taxon_str):
    if pd.isna(taxon_str):
        return 'Unknown'
    taxa_list = [t.strip() for t in taxon_str.split(',')]
    taxa_list = list(dict.fromkeys(taxa_list))  # preserve order and remove duplicates
    return ','.join(taxa_list)

df['Host_range_taxon'] = df['Host_range_taxon'].apply(deduplicate_taxon)

# split Host_range_taxon into taxonomic levels
df['Host_range_taxon'] = df['Host_range_taxon'].apply(lambda x: x.split(',')[0])

# Fill missing with placeholder
df['Host_range_taxon'] = df['Host_range_taxon'].fillna('Unknown/Unknown/Unknown/Unknown/Unknown/Unknown')

# split into Phylum, Class, Order, Family, Genus, Species
tax_cols = ['Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
host_tax_split = df['Host_range_taxon'].str.split('/', expand=True)

# ensure exactly 6 columns
for i in range(len(tax_cols)):
    if i not in host_tax_split.columns:
        host_tax_split[i] = 'Unknown'
host_tax_split = host_tax_split.iloc[:, :6]
host_tax_split.columns = tax_cols

# concatenate back to main DataFrame
df = pd.concat([df.drop(columns=['Host_range_taxon']), host_tax_split], axis=1)
df.to_csv("gpd/data/03_gpd_taxa_split.csv", sep=';', index=False)
