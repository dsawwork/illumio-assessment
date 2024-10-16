import csv
from collections import defaultdict
from helper import *

def load_protocol_mapping(protocol_file):
    protocol_map = {}
    # this file has got column headers, hence using DictReader for convenience
    with open(protocol_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            decimal = int(row[IANA_PROTOCOL])
            protocol = row[IANA_PROTOCOL_KEYWORD].lower()
            protocol_map[decimal] = protocol

    return protocol_map

# Parses the lookup table with row format: dstport, protocol, tag
def load_lookup_table(lookup_file):
    lookup_table = {}
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            lookup_table[key] = row['tag'].strip()
    return lookup_table

# Parses the flow log with AWS flow log row format. 
# accepts log file path, lookup_table dict and protocol map dict. 
def process_flow_logs(log_file, lookup_table, protocol_map):
    tag_count = defaultdict(int)
    port_protocol_count = defaultdict(int)

    with open(log_file, mode='r') as file:
        for line in file:
            columns = line.strip().split()
            if len(columns) >= 14 and columns[0] == '2':  # Checking for version 2 logs
                dstport = int(columns[6])
                
                protocol = protocol_map[int(columns[7])].lower()
                
                lookup_key = (dstport, protocol)
                # debugging: print(lookup_key)
                port_protocol_count[(dstport, protocol)] += 1
                if lookup_key in lookup_table:
                    tag = lookup_table[lookup_key]
                    tag_count[tag] += 1
                else:
                    tag_count[UNTAGGED] += 1

    return (tag_count, port_protocol_count)

# Saves the tag counts given the outputfile and tag count variables
def save_tag_counts(output_file, tag_count):
    with open(output_file, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(TAG_COUNT_COLUMNS)
        for tag, count in tag_count.items():
            writer.writerow([tag, count])

def save_port_protocol_counts(output_file, port_protocol_count):
    with open(output_file, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(PORT_PROTOCOL_COLUMNS)
        for (dstport, protocol), count in port_protocol_count.items():
            writer.writerow([dstport, protocol, count])

# Main function
def main(flow_log_file, lookup_file, tag_output_file, port_prot_file, protocol_file):
    protocol_map = load_protocol_mapping(protocol_file)
    lookup_table = load_lookup_table(lookup_file)
    tag_count, port_protocol_count = process_flow_logs(flow_log_file, lookup_table, protocol_map)
    save_tag_counts(tag_output_file, tag_count)
    save_port_protocol_counts(port_prot_file, port_protocol_count)


# COmmand line processing starts here


import argparse


def cmdmain(flow_log_file, lookup_file, output_file, port_prot_file, protocol_file):
    # Placeholder for the actual logic of processing logs
    print(f"Flow log file: {flow_log_file}")
    print(f"Lookup file: {lookup_file}")
    print(f"Tag count output file: {output_file}")
    print(f"Port/Protocol count output file: {port_prot_file}")
    print(f"Protocol mapping file: {protocol_file}")
    main(flow_log_file, lookup_file, output_file, port_prot_file, protocol_file)
    

# Function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Flow Log Parser and Tag Mapper")
    
    parser.add_argument(
        '--flow_log_file', 
        default='flow_logs.txt', 
        help="The flow log file to process (default: 'flow_logs.txt')"
    )
    parser.add_argument(
        '--lookup_file', 
        default='lookup_table.csv', 
        help="The lookup table file (default: 'lookup_table.csv')"
    )
    parser.add_argument(
        '--output_file', 
        default='tag_count_output.csv', 
        help="The output file for tag counts (default: 'tag_count_output.csv')"
    )
    parser.add_argument(
        '--port_prot_file', 
        default='port_protocol_count_output.csv', 
        help="The output file for port/protocol counts (default: 'port_protocol_count_output.csv')"
    )
    parser.add_argument(
        '--protocol_file', 
        default='protocol-numbers-1.csv', 
        help="The protocol mapping file (default: 'protocol-numbers-1.csv')"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(
        args.flow_log_file, 
        args.lookup_file, 
        args.output_file, 
        args.port_prot_file, 
        args.protocol_file
    )
