#!/Users/thomasdeveloper/anaconda3/envs/outlines_unleashed_command_line/bin/python

from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.unleashed_outline import UnleashedOutline
import sys
from output_generators.csv_output_generator import CsvOutputGenerator
from tests.test_resources.test_data import data_node_specifier_test_01


def main():
    num_arguments = len(sys.argv)
    expected_num_arguments = 3  # Note command line arguments will be one more as filename is first

    opml_path = ""
    json_path = ""
    csv_path = ""

    if num_arguments == 1:
        # Temporary hack to allow debugging. No parameters supplied --> use test files.
        print("Debug mode - hard coded arguments for command line")

        opml_path = "tests/test_resources/opml_data_extraction_test_01.opml"
        json_path = "tests/test_resources/custom_json_test_descriptors_risk_01.json"
        csv_path = "tests/test_resources/output_files/opml_data_extraction_test_01.csv"
    elif num_arguments != expected_num_arguments + 1:
        print(f"Wrong number of arguments ({num_arguments - 1} (should be {expected_num_arguments})")
    else:
        opml_path = sys.argv[1]
        json_path = sys.argv[2]
        csv_path = sys.argv[3]

    outline = Outline.from_opml(opml_path)
    print("Successfully read outline, unleashing...")

    unleashed_outline = UnleashedOutline(outline)
    data_nodes = unleashed_outline.extract_data_nodes()
    print(f"Outline is unleashed, there are {len(data_nodes)} data nodes in this outline")
    for index, node in enumerate(data_nodes):
        print(f"{index}: {node['data_node_name']}")

    print("Processing first node")

    data_node_list_index = data_nodes[0]['data_node_list_index']
    data_node = unleashed_outline.list_unleashed_nodes()[data_node_list_index].node()

    data_node_specifier = DataNodeSpecifier.from_json_file(json_path)
    extracted_data_table = data_node_specifier.extract_data_node_dispatch(data_node)

    CsvOutputGenerator.create_csv_file(extracted_data_table, csv_path)


if __name__ == "__main__":
    main()
