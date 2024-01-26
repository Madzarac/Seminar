from Bio import SeqIO
import sys
import re


def match(fastaFile):
        result = open("match_id_taxid/test", "w")
        Lines = []
        for record in SeqIO.parse(fastaFile, 'fasta'):
                id = record.id
                parts = re.split(r'\s+', record.description.strip())
                parts = parts[5].strip().replace('|', '!').split('!')
                speciesId = parts[3]
                genusId = parts[5]
                line = id + "\t" + speciesId + "\t" + genusId + "\n"
                Lines.append(line)

        result.writelines(Lines)
        result.close()
        print("?")

if __name__ == "__main__":
        if len(sys.argv) < 2:
                print("Missing database file.")
        else:
                match(sys.argv[1])
