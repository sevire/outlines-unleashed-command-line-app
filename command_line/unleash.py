#!/Users/thomasdeveloper/anaconda3/envs/outlines_unleashed_command_line/bin/python

from outline.outline import Outline
from outlines_unleashed.data_node_specifier import DataNodeSpecifier
from outlines_unleashed.unleashed_outline import UnleashedOutline
import sys
from output_generators.csv_output_generator import CsvOutputGenerator
from tests.test_resources.test_data import data_node_specifier_test_01


def main():
    num_arguments = len(sys.argv)
    expected_num_arguments = 2  # Note command line arguments will be one more as filename is first
    if False and num_arguments != expected_num_arguments + 1:
        print(f"Wrong number of arguments ({num_arguments - 1} (should be {expected_num_arguments})")
    else:
        opml_path = sys.argv[1]
        csv_path = sys.argv[2]

        # opml_path = "/Users/thomasdeveloper/Documents/Projects/outlines_unleashed_command_line/tests/test_resources/opml_data_extraction_test_01.opml"
        # csv_path = "/Users/thomasdeveloper/Documents/Projects/outlines_unleashed_command_line/tests/test_resources/output_files/opml_data_extraction_test_01.csv"
        # outline_specifier_json = "/Users/thomasdeveloper/Documents/Projects/outlines_unleashed_command_line/tests/test_resources/opml_data_extraction_test_01a.json"

        outline_specifier_data = data_node_specifier_test_01

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

        # with open(outline_specifier_json, 'r') as json_file:
        #     json_string = json_file.read().replace('\n', '')

        data_node_specifier = DataNodeSpecifier(outline_specifier_data)
        extracted_data_table = data_node_specifier.extract_data_node_dispatch(data_node)

        CsvOutputGenerator.create_csv_file(extracted_data_table, csv_path)


if __name__ == "__main__":
    main()
