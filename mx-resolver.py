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

def write_multiple_columns_to_csv(file_path, data_dict, encoding='latin-1'):
    with open(file_path, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write the header row (column names)
        csvwriter.writerow(data_dict.keys())
        
        # Write the rows
        rows = zip(*data_dict.values())
        csvwriter.writerows(rows)

def process_domains(domains):
    mx_records = []
    email_provider = []
    cache = {}
    count = 1

    for domain in domains:
        print(f"{domain} -------- {count}/{len(domains)}")
        count = count + 1
        if domain in cache.keys():
            mx_records.append(cache[domain])
            continue

        if (domain == ' ') or (domain == ''):
            mx_records.append("")
            continue
        mx_list = []

        try:
            mx = dns.resolver.resolve(domain[1:], 'MX')
            for rdata in mx:
                mx_list.append(rdata.to_text())
            mx_string = ' / '.join(mx_list)
            mx_records.append(mx_string)
            cache[domain] = mx_string
        except dns.resolver.NoAnswer:
            mx_records.append('MX NOT FOUND')
            cache[domain] = 'MX NOT FOUND'
        except dns.resolver.NXDOMAIN:
            mx_records.append('DOMAIN NON EXIST')
            cache[domain] = 'DOMAIN NON EXIST'
    
    for mx_record in mx_records:
        if ('google' in mx_record) or ('GOOGLE' in mx_record):
            email_provider.append("Google")
        elif ('outlook' in mx_record) or ('OUTLOOK' in mx_record):
            email_provider.append("Microsoft")
        elif ('MX NOT FOUND' in mx_record) or ('DOMAIN NON EXIST' in mx_record) or (mx_record == ""):
            email_provider.append("N/A")
        else:
            email_provider.append("Third Party")

    return mx_records, email_provider

"""
d = ['@jazz.com.pk']
m, p = process_domains(d)

print(d)
print(m)
print(p)
"""



domain1 = read_column_to_list('domains.csv', 'domain1')
mx1, provider1 = process_domains(domain1)
output1 = {}
output1['domain1'] = domain1
output1['mx1'] = mx1
output1['provider1'] = provider1
write_multiple_columns_to_csv('domain1.csv', output1)
print("\n\n")
print("WRITTEN OUTPUT1")

domain2 = read_column_to_list('domains.csv', 'domain1')
mx2, provider2 = process_domains(domain2)
output2 = {}
output2['domain2'] = domain2
output2['mx2'] = mx2
output2['provider2'] = provider2
write_multiple_columns_to_csv('domain2.csv', output2)
print("\n\n")
print("WRITTEN OUTPUT2")

print("\n\n")
print(domain1)
print("\n\n")
print(mx1)
print("\n\n")
print(provider1)
