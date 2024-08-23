import dns.resolver
import csv

def read_column_to_list(file_path, column_name):
    column_data = []
    
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='latin-1') as csvfile:
        # Create a CSV DictReader object to access columns by name
        csvreader = csv.DictReader(csvfile)
        
        # Iterate through each row and append the specific column value to the list
        for row in csvreader:
            column_data.append(row[column_name])
    
    return column_data

def write_row_to_csv(file_path, row):
    with open(file_path, mode='a', newline='', encoding='latin-1') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)

def check_provider(mx_record):
    if ('google' in mx_record) or ('GOOGLE' in mx_record):
        return "Google"
    elif ('outlook' in mx_record) or ('OUTLOOK' in mx_record):
        return "Microsoft"
    elif ('MX NOT FOUND' in mx_record) or ('DOMAIN NON EXIST' in mx_record) or (mx_record == "") or (mx_record == "ERR"):
        return "N/A"
    else:
        return "Third Party"

def process_domains(domains, file_path):
    cache = {}
    count = 1

    for domain in domains:
        print(f"{domain} -------- {count}/{len(domains)}")
        count = count + 1
        if domain in cache.keys():
            mx_string = cache[domain]
            provider = check_provider(mx_string)
            write_row_to_csv(file_path, [domain, mx_string, provider])
            continue

        if (domain == ' ') or (domain == ''):
            mx_string = ""
            provider = check_provider(mx_string)
            write_row_to_csv(file_path, [domain, mx_string, provider])
            continue

        try:
            mx = dns.resolver.resolve(domain[1:], 'MX')
            mx_list = []
            for rdata in mx:
                mx_list.append(rdata.to_text())
            mx_string = ' / '.join(mx_list)
        except dns.resolver.NoAnswer:
            mx_string = 'MX NOT FOUND'
            cache[domain] = 'MX NOT FOUND'
        except dns.resolver.NXDOMAIN:
            mx_string = 'DOMAIN NON EXIST'
            cache[domain] = 'DOMAIN NON EXIST'
        except:
            mx_string = 'ERR'
            cache[domain] = 'ERR'
        
        provider = check_provider(mx_string)
        write_row_to_csv(file_path, [domain, mx_string, provider])

"""
d = ['@frontiercargroup.com']
process_domains(d, 'domain1.csv')

print(d)
"""

domain1 = read_column_to_list('domains.csv', 'domain1')
process_domains(domain1, 'domain1.csv')
print("WRITTEN OUTPUT1")

domain2 = read_column_to_list('domains.csv', 'domain1')
process_domains(domain2, 'domain2.csv')
print("\n\n")
print("WRITTEN OUTPUT2")

print("\n\n")
print(domain1)
print("\n\n")
print(mx1)
print("\n\n")
print(provider1)
