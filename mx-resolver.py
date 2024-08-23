import dns.resolver

def process_domains(domains):
    mx_records = []
    email_provider = []

    for domain in domains:
        mx_list = []
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            for rdata in mx:
                mx_list.append(rdata.to_text())
            mx_string = ' / '.join(mx_list)
            mx_records.append(mx_string)
        except dns.resolver.NoAnswer:
            mx_records.append('MX NOT FOUND')
        except dns.resolver.NXDOMAIN:
            mx_records.append('DOMAIN NON EXIST')
    
    for mx_record in mx_records:
        if ('google' in mx_record) or ('GOOGLE' in mx_record):
            email_provider.append("Google")
        elif ('outlook' in mx_record) or ('OUTLOOK' in mx_record):
            email_provider.append("Microsoft")
        elif ('MX NOT FOUND' in mx_record) or ('DOMAIN NON EXIST' in mx_record):
            email_provider.append("N/A")
        else:
            email_provider.append("Third Party")
    
    return mx_records, email_provider

d = ['jazz.com.pk', 'seecs.edu.pk', 'greenvorx.com', 'garajmail.com', 'cus1.mail.garajmail.com']

m, p = process_domains(d)

print("DOMAINS:\n")
print("\n".join(d))
print("\n\nMX:\n")
print("\n".join(m))
print("\n\nPROVIDER:\n")
print("\n".join(p))


"""
try:
    mx_records = dns.resolver.resolve("garajmail.com", 'MX')

    for rdata in mx_records:
        print(rdata.to_text())

except dns.resolver.NoAnswer:
    print(f"No MX records found for domain")
except dns.resolver.NXDOMAIN:
    print(f"Domain does not exist")
except Exception as e:
    print(f"An error occurred: {str(e)}")

"""