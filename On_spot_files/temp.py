import json

# Load the JSON file
with open('language_codes.json', 'r') as file:
    language_details = json.load(file)

# Rearrange the JSON file based on the name of the country
sorted_language_details = dict(sorted(language_details.items(), key=lambda x: x[1]))

# Save the rearranged JSON file
with open('language_codes.json', 'w') as file:
    json.dump(sorted_language_details, file, indent=4)
