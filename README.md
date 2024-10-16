 

# Flow Log Parser and Tag Mapper

## Overview

This Python program processes flow log data and maps each log entry to a corresponding tag based on a lookup table. The lookup table specifies destination port and protocol combinations and assigns a tag for matching entries. The program also generates output files showing the count of matches for each port/protocol combination and each tag. The **default flow log format (version 2)** is used throughout this program.

## Run
- Execute `python .\illumio.py` as is.
- There is support for custom file names, but no need to pass in those at the moment.

## File Descriptions

### Input Files

1. **Flow Log File** (`flow_logs.txt`):
   - This file contains flow log entries in the default format (version 2):
     ```
     version account-id eni source-address destination-address srcport dstport protocol packets bytes start-time end-time action log-status
     ```
   - Example of log entries:
     ```
     2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
     2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK
     ```

2. **Lookup Table File** (`lookup_table.csv`):
   - This file defines the mapping from a destination port and protocol combination to a specific tag. The file structure is as follows:
     ```
     dstport,protocol,tag
     ```
   - Example of entries:
     ```
     25,tcp,sv_P1
     68,udp,sv_P2
     23,tcp,sv_P1
     ```

3. **Protocol Mapping File** (`protocol_mapping.csv`):
   - This file maps protocol numbers to their respective protocol names in lowercase. The format of the file is:
     ```
     Decimal,Keyword,Protocol,IPv6 Extension Header,Reference
     ```
   - Example of entries:
     ```
     6,TCP,Transmission Control,,[RFC9293]
     17,UDP,User Datagram,,[RFC768]
     ```

### Output Files

1. **Tag Count Output File** (`tag_count_output.csv`):
   - This file contains the count of matches for each tag found in the flow logs. The format of the output is:
     ```
     Tag,Count
     ```
   - Example of output:
     ```
     sv_P1,10
     sv_P2,5
     ```

2. **Port/Protocol Count Output File** (`port_protocol_count_output.csv`):
   - This file contains the count of matches for each port and protocol combination. The format is:
     ```
     DstPort,Protocol,Count
     ```
   - Example of output:
     ```
     25,tcp,15
     68,udp,5
     ```

## Usage Instructions

1. Place the **flow log file** (`flow_logs.txt`), **lookup table file** (`lookup_table.csv`), and **protocol mapping file** (`protocol_mapping.csv`) in the same directory as the Python script.
2. Run the script to process the flow log data. The script will:
   - Map each log entry to a corresponding tag using the lookup table.
   - Generate two output files:
     - `tag_count_output.csv` containing the count of matches for each tag.
     - `port_protocol_count_output.csv` containing the count of matches for each port and protocol combination.

## Important Notes

- This program expects flow log files in the **default version 2 format**.
- Ensure that the lookup table and flow logs are consistent with the protocol numbers from the protocol mapping file.
- 

