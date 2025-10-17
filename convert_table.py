import re

# Read the file
with open(r'c:\projects\retail_clustering_poc\retail_customer_cat_using_mcp_poc\PROJECT_VISION.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and convert the tab-separated data to markdown table
lines = content.split('\n')
new_lines = []
in_table = False

for i, line in enumerate(lines):
    # Check if line matches the pattern: number TAB department TAB class
    if re.match(r'^\d+\t', line):
        if not in_table:
            in_table = True
        # Convert tab-separated to markdown table row
        parts = line.split('\t')
        if len(parts) >= 3:
            new_lines.append(f'| {parts[0]} | {parts[1]} | {parts[2]} |')
        elif len(parts) == 2:
            new_lines.append(f'| {parts[0]} | {parts[1]} | |')
    else:
        if in_table:
            in_table = False
        new_lines.append(line)

# Write back
with open(r'c:\projects\retail_clustering_poc\retail_customer_cat_using_mcp_poc\PROJECT_VISION.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print('✅ Converted tab-separated data to markdown table format')
print(f'✅ Processed {len(lines)} lines')
