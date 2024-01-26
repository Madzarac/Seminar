import re


def find_resulting_tax_id(current_tax, target_rank, taxonomy_tree, ranks):
    not_found_resulting_tax_id = True
    resulting_tax_id = 0
    tax = current_tax
    while not_found_resulting_tax_id:
        if tax in taxonomy_tree:
            parent_rank = ranks[tax]
            if parent_rank == target_rank:
                not_found_resulting_tax_id = False
                resulting_tax_id = tax
            else:
                prev_tax = tax
                tax = taxonomy_tree[tax]
                if tax == prev_tax:
                    not_found_resulting_tax_id = False
        else:
            not_found_resulting_tax_id = False
    return resulting_tax_id


def analyse_sam_paf(lines, target_rank, taxonomy_tree, ranks, is_sam):
    results = {}
    max_values = {}
    transformed_rows = {}
    for line in lines:
        parts = re.split(r'\t+', line.strip())
        if is_sam:
            if parts[1].strip() != "0" and parts[1].strip() != "16":
                continue
        read_id = parts[0].strip()
        tax_id_extended = parts[2].strip()
        if is_sam == False:
            tax_id_extended = parts[5].strip()

        parts2 = re.split(r'\|+', tax_id_extended.strip())
        if len(parts2) == 1:
            continue
        tax_id = parts2[2].strip()
        resulting_tax_id = find_resulting_tax_id(tax_id, target_rank, taxonomy_tree, ranks)
        if resulting_tax_id == 0:
            resulting_tax_id = tax_id

        value_cig = 0.0
        if is_sam:
            if len(parts) >= 14 :
                nm = parts[13].strip()
                parts3 = re.split(r':+', nm.strip())
                value_cig = int(parts3[-1].strip())
        else:
            length_q = int(parts[3].strip()) - int(parts[2].strip())
            length_t = int(parts[9].strip()) - int(parts[8].strip())
            length = max(length_t, length_q)
            nm = int(parts[9].strip())
            cm = re.split(r':+', parts[13].strip())
            value_cig = float((float(cm[2]) * float(length) * float(nm)) / (float(cm[2]) + float(length) + float(nm)))

        if read_id in results:
            if value_cig > max_values[read_id]:
                results[read_id] = []
                results[read_id].append(resulting_tax_id)
                max_values[read_id] = value_cig
            elif value_cig == max_values[read_id]:
                results[read_id].append(resulting_tax_id)
        else:
            results[read_id] = []
            results[read_id].append(resulting_tax_id)
            max_values[read_id] = value_cig

    for read_id in results:
        tax_ids = results[read_id]
        values = {}
        for tax_id in tax_ids:
            if tax_id not in values:
                values[tax_id] = 0
            values[tax_id] += 1
        max_tax_id = ""
        max_value = 0
        for tax_id in values:
            value = values[tax_id]
            if value > max_value:
                max_value = value
                max_tax_id = tax_id
        transformed_rows[read_id.strip()] = (max_tax_id, ranks[max_tax_id])
    return transformed_rows



def main_func(number_of_nodes_files, path):
    ranks_lists = {}
    taxonomy_tree_lists = {}
    taxonomy_names_lists = {}

    for nodes_index in range(0, int(number_of_nodes_files)):
        nodes_file = open(path + "/" + "nodes.dmp", "r")
        nodes_lines = nodes_file.readlines()
        ranks = {}
        taxonomy_tree = {}
        for line in nodes_lines:
            parts = re.split(r'\t\|\t+', line.strip())
            taxonomy_tree[parts[0].strip()] = parts[1].strip()
            ranks[parts[0].strip()] = parts[2].strip()
        ranks_lists[nodes_index] = ranks
        taxonomy_tree_lists[nodes_index] = taxonomy_tree

    for names_index in range(0, int(number_of_nodes_files)):
        names_file = open(path + "/" + "names.dmp", "r")
        names_lines = names_file.readlines()
        taxonomy_names = {}
        for line in names_lines:
            parts = re.split(r'\|+', line.strip())
            if parts[3].strip() == "scientific name":
                taxonomy_names[parts[0].strip()] = parts[1].strip()
        taxonomy_names_lists[names_index] = taxonomy_names


    target_ranks = ["species", "genus"]
    root_results = "results"
    root_cleaned_results = "cleaned_results5"
    root_reports = "reports"


    databases = ["human_gut_95_kraken_databasehuman_gut_95_kraken_database"]
    datasets = [
        ("human_gut_95_dataset/human_gut_95_species_abundance_equal_length_5000_new_design_header.fasta", False, 1, False, False),
    ]


    for (dataset, is_percentage, number_of_dataset, is_kaiju_exception, is_negative) in datasets:
        print("#Dataset: " + str(dataset))
        path_to_dataset = dataset

        for database in databases:
            print("#Database: " + str(database))
            for target_rank in target_ranks:
                print("Target rank: " + str(target_rank))

                all_transformed_rows = {}
                results_filename = "aln.paf"
                results_file = open(results_filename, "r") 
                results_lines = results_file.readlines()

                parsed_rows = []
                taxonomy_tree = taxonomy_tree_lists[0]
                ranks = ranks_lists[0]

                parsed_rows = analyse_sam_paf(results_lines, target_rank, taxonomy_tree, ranks, False)

                transformed_rows = parsed_rows
                cleaned_filename = root_cleaned_results + "/" + str(database) + "_" + str(target_rank) + ".f2"
                cleaned_outfile = open(cleaned_filename, "w")

                for read_id in transformed_rows:
                            (tax_id, rank) = transformed_rows[read_id]
                            cleaned_outfile.write(read_id.strip() + "\t" + tax_id.strip() + "\t" + rank.strip() + "\n")

                all_transformed_rows[0] = transformed_rows


main_func(1, "names_nodes")
