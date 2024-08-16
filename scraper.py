import json

# Open the JSONL file for reading
with open("ukri.jsonl", "r") as jsonl_file:
    # Open the text file for writing
    with open("ukri.txt", "w") as txt_file:
        # Read each line in the JSONL file
        for line in jsonl_file:
            # Parse the JSON object
            data = json.loads(line)
            
            # Write the desired fields to the text file
            txt_file.write(f"Title: {data['title']}\n")
            txt_file.write(f"URL: {data['url']}\n\n")