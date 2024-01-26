import pandas as pd
import sys
import re

def count(speciesFile, genusFile, krakenFile, csvFile):
    df1 = pd.read_csv(csvFile)

    dictSpec = {}
    species = open(speciesFile, 'r')
    species = species.readlines()
    for line in species:
        parts = re.split(r'\t+', line.strip())
        taxid = parts[1]
        if taxid in dictSpec.keys():
            dictSpec[taxid] += int(1)
        else:
            dictSpec[taxid] = int(1)

    dictGenus = {}
    genus = open(genusFile, 'r')
    genus = genus.readlines()
    for line in genus:
        parts = re.split(r'\t+', line.strip())
        taxid = parts[1]
        if taxid in dictGenus.keys():
            dictGenus[taxid] += int(1)
        else:
            dictGenus[taxid] = int(1)

    dictKraken = {}
    taxKraken = open(krakenFile, 'r')
    for line in taxKraken:
        parts = re.split(r'\t+', line.strip())
        if parts[2] in dictKraken.keys():
            taxid = parts[2]
            dictKraken[taxid] += int(1)
        else:
            taxid = parts[2]
            dictKraken[taxid] = int(1)

    dictSpec_df = pd.DataFrame(list(dictSpec.items()), columns=['species_tax_ID', 'Benchmark READ COUNT species'])
    df1['species_tax_ID'] = df1['species_tax_ID'].astype(str)
    dictSpec_df['Benchmark READ COUNT species'] = dictSpec_df['Benchmark READ COUNT species'].astype(str)
    merged_df = pd.merge(df1, dictSpec_df, on='species_tax_ID', how='outer')

    dictGenus_df = pd.DataFrame(list(dictGenus.items()), columns=['genus_tax_ID', 'Benchmark READ COUNT genus'])
    merged_df['genus_tax_ID'] = merged_df['genus_tax_ID'].astype(str)
    dictGenus_df['Benchmark READ COUNT genus'] = dictGenus_df['Benchmark READ COUNT genus'].astype(str)
    merged_df = pd.merge(merged_df, dictGenus_df, on='genus_tax_ID', how='outer')

    dictKraken_df = pd.DataFrame(list(dictKraken.items()), columns=['species_tax_ID', 'kraken READ COUNT species'])
    dictKraken_df['kraken READ COUNT species'] = dictKraken_df['kraken READ COUNT species'].astype(str)
    merged_df = pd.merge(merged_df, dictKraken_df, on='species_tax_ID', how='left')
    dictKrakenGenus_df = pd.DataFrame(list(dictKraken.items()), columns=['genus_tax_ID', 'kraken READ COUNT genus'])
    dictKrakenGenus_df['kraken READ COUNT genus'] = dictKrakenGenus_df['kraken READ COUNT genus'].astype(str)
    merged_df = pd.merge(merged_df, dictKrakenGenus_df, on='genus_tax_ID', how='left')

    merged_df.to_csv('usporedba_popis_bakterija.csv', index=False)

def countAdd(csvFile, speciesFile):
    df1 = pd.read_csv(csvFile)

    dictSpec = {}
    species = open(speciesFile, 'r')
    species = species.readlines()
    for line in species:
        parts = re.split(r'\t+', line.strip())
        taxid = parts[1]
        if taxid in dictSpec.keys():
            dictSpec[taxid] += int(1)
        else:
            dictSpec[taxid] = int(1)
    
    dictSpec_df = pd.DataFrame(list(dictSpec.items()), columns=['species_tax_ID', 'script READ COUNT species'])
    df1['species_tax_ID'] = df1['species_tax_ID'].astype(str)
    dictSpec_df['script READ COUNT species'] = dictSpec_df['script READ COUNT species'].astype(str)
    merged_df = pd.merge(df1, dictSpec_df, on='species_tax_ID', how='outer')
    merged_df.to_csv(csvFile, index=False)





if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[3] == "add":
        countAdd(sys.argv[1], sys.argv[2]) #csv file, species file, "add"
    elif len(sys.argv) < 5:
        print("Missing speciesFile, genusFile, krakenFile and/or csv file with groun truth.")
    else:
        count(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
