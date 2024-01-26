import re
import sys

def compare(realTaxidsFile, krakenFile, folder):
    dictKraken = {}
    dictKrakenUnclass = {}
    dictRealTaxidValues = {}

    falsePositive = {}
    falseNegative = {}
    truePositive = {}
    trueNegative = {}

    real = open(realTaxidsFile, 'r')
    realTaxids = real.readlines()

    speciesKraken = open(krakenFile, 'r')
    krakenTaxid = speciesKraken.readlines()

    falsePos = open(folder + "/" + "falsePositive.txt", "w")
    falseNeg = open(folder + "/" + "falseNegative.txt", "w")
    truePos = open(folder + "/" + "truePositive.txt", "w")
    trueNeg = open(folder + "/" + "trueNegative.txt", "w")

    for line in realTaxids:
        parts = re.split(r'\s+', line.strip())
        dictRealTaxidValues[parts[0]] = parts[1]

    for line in krakenTaxid:
        parts = re.split(r'\t+', line.strip())
        if parts[0] == "U":
            taxid = parts[2]
            dictKrakenUnclass[parts[1]] = taxid
        else:
            taxid = parts[2]
            dictKraken[parts[1]] = taxid


    correct = 0
    for id in dictKraken.keys():
        if id in dictRealTaxidValues:
            if dictRealTaxidValues[id] == dictKraken[id]:
                correct += 1
                truePositive[id] = "\t" + dictRealTaxidValues[id] + "\t" + dictKraken[id]
            else:
                falsePositive[id] = "\t" + dictRealTaxidValues[id] + "\t" + dictKraken[id]
        else:
            falsePositive[id] = "\t-\t" + dictKraken[id]

    for id in dictKrakenUnclass.keys():
        if dictRealTaxidValues[id] == "?":
            trueNegative[id] = "\t-" + "\t*"
        else:
            falseNegative[id] = "\t" + dictRealTaxidValues[id] + "\t*"

    falsePos.write("Number of false positive reads: " + str(len(falsePositive)) + ".\n\n")
    falseNeg.write("Number of false negative reads: " + str(len(falseNegative)) + ".\n\n")
    truePos.write("Number of true positive reads: " + str(len(truePositive)) + ".\n\n")
    trueNeg.write("Number of true negative reads: " + str(len(trueNegative)) + ".\n\n")

    falsePos.write("id\tcorrect_species_taxid\tkreken_species_taxid\n")
    falseNeg.write("id\tcorrect_species_taxid\tkreken_species_taxid\n")
    truePos.write("id\tcorrect_species_taxid\tkraken_species_taxid\n")
    trueNeg.write("id\tcorrect_species_taxid\tkreken_species_taxid\n")

    for key, value in falsePositive.items():
        falsePos.write(key + value + "\n")

    for key, value in falseNegative.items():
        falseNeg.write(key + value + "\n")

    for key, value in truePositive.items():
        truePos.write(key + value + "\n")

    for key, value in trueNegative.items():
        trueNeg.write(key + value + "\n")


    falsePos.close()
    falseNeg.close()
    truePos.close()
    trueNeg.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Missing taxids file or kraken file or folder name.")
    else:
        compare(sys.argv[1], sys.argv[2], sys.argv[3])
