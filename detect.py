import re
from collections import defaultdict

failed = defaultdict(int)
success = defaultdict(int)

with open("authCOPY.log") as file:

    for line in file:

        ip_match = re.search(
            r"\d+\.\d+\.\d+\.\d+",
            line
        )

        if not ip_match:
            continue

        ip = ip_match.group()

        if "Failed password" in line:
            failed[ip] += 1

        elif "Accepted password" in line:
            success[ip] += 1

print("\n===== ALERT REPORT =====\n")

for ip in failed:

    if failed[ip] >= 3:

        print(f"IP Address: {ip}")
        print(f"Failed Attempts: {failed[ip]}")
        print(f"Successful Login: {success[ip]}")

        if success[ip] > 0:
            print("Risk Level: HIGH")
        else:
            print("Risk Level: MEDIUM")

        print()


# This part will extract a CSV file which can open by using Excel
import csv

with open("report.csv", "w", newline="") as file:
	
	writer = csv.writer(file)

	writer.writerow([
		"IP",
		"Failed",
		"Success",
		"Risk"
	])

	for ip in failed:
		if failed[ip] >= 3:
		
			risk = "HIGH" if success[ip] > 0 else "MEDIUM"
			writer.writerow([
				ip,
				failed[ip],
				success[ip],
				risk
			])

