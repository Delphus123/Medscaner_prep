#!/usr/bin/env python3
"""Merge all JSON batches and replace exam content."""
import re, json

# Load and merge all batches
all_entries = {}
for i in range(1, 6):
    with open(f'/home/hal9000/Projects/Medscaner_prep/entries_batch{i}.json', 'r', encoding='utf-8') as f:
        batch = json.load(f)
    all_entries.update(batch)
    print(f"Batch {i}: {len(batch)} entries")

print(f"\nTotal entries: {len(all_entries)}")
print("Keys:", list(all_entries.keys()))

# Load HTML
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the resonance block boundaries correctly
res_start = content.find('resonancia: {')
# Find the closing brace of resonance: look for pattern after tomografia block
tom_idx = content.find('tomografia: {')
depth = 0
res_end = None
for i in range(tom_idx, len(content)):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        if depth == 0:
            res_end = i + 1  # include the closing brace
            break
        depth -= 1
print(f'Resonance block: {res_start} to {res_end} ({res_end - res_start} chars)')

def make_entry(key, data):
    """Build a single exam entry. No trailing comma — separator is kept separately."""
    d = data
    parts = [key + ': `<b>' + d['title'] + ' \u2014 TRIAGEM E PROTOCOLO</b><br><br>']
    parts.append('<b>1. INFORMA\u00c7\u00d5ES PARA AGENDAMENTO:</b><br>')
    for x in d['agend']: parts.append('\u2022 ' + x + '<br>')
    parts.append('<br><b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>')
    for x in d['anam']: parts.append('\u2022 ' + x + '<br>')
    parts.append('<br><b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>')
    for x in d['triag']: parts.append('\u2022 ' + x + '<br>')
    parts.append('<br><b>4. RECOMENDA\u00c7\u00d5ES AO T\u00c9CNICO (Protocolo):</b><br>')
    for x in d['prot']: parts.append('\u2022 ' + x + '<br>')
    parts.append('`')
    return ''.join(parts)

# Replace each entry
replaced = 0
not_found = []
for key in all_entries:
    new_entry = make_entry(key, all_entries[key])
    # First entry (abdome) has no leading newline; others do
    if key == 'abdome':
        pattern = r'abdome:\s*`[^`]*`'
    else:
        pattern = r'\n\s+' + re.escape(key) + r':\s*`[^`]*`'
    m = re.search(pattern, content)
    if m:
        # After match: ,\n\n + indent + next_key + ` (non-last) OR ,\n\n + 8sp + }, + ... (last)
        rest = content[m.end():]
        # rest starts right after the closing backtick of the entry
        # For first entry (abdome): no leading newline, just key: `content`
        # After match: ,\n\n + indent + next_key (non-last) or ,\n\n + 8sp + } (last)
        if key == 'abdome':
            # First entry: after backtick, the separator starts with ,\n\n + indent
            # Keep 14 chars: ,\n\n + 12sp (next_key starts at [14])
            keep_len = 14
            old_total = (m.end() + keep_len) - m.start()
            content = content[:m.start()] + new_entry + content[m.end() + keep_len:]
        else:
            rest = content[m.end():]
            if len(rest) >= 12 and rest[11] == '}':
                keep_len = 12  # last entry
            else:
                keep_len = 15  # non-last entry
            old_total = (m.end() + keep_len) - m.start()
            content = content[:m.start()] + new_entry + content[m.end() + keep_len:]
        old_total = (m.end() + keep_len) - m.start()
        content = content[:m.start()] + new_entry + content[m.end() + keep_len:]
        print(f"  {key}: OK ({old_total} -> {len(new_entry)} chars)")
        replaced += 1
    else:
        print(f"  {key}: NOT FOUND")
        not_found.append(key)

print(f"\nReplaced {replaced}/{len(all_entries)} entries")
if not_found:
    print(f"NOT FOUND: {not_found}")

# Save
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("\nSaved!")
