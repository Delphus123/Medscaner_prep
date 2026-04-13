#!/usr/bin/env python3
"""Replace all 29 RM exam entries - process LAST to FIRST."""
import re, json

# Load all entries from JSON batches
all_entries = {}
for i in range(1, 6):
    with open(f'/home/hal9000/Projects/Medscaner_prep/entries_batch{i}.json', 'r', encoding='utf-8') as f:
        batch = json.load(f)
    all_entries.update(batch)
print(f"Loaded {len(all_entries)} entries")

# Load HTML
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def make_entry(key, data):
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

def find_entry_range(content, key):
    """Find the range of an entry in content. Returns (start, end) or None.
    Handles first entry (no leading newline) separately."""
    if key == 'abdome':
        # First entry: starts after `resonancia: {`
        m = re.search(r'abdome:\s*`[^`]*`', content)
        if m:
            return m.start(), m.end()
        return None
    else:
        # Other entries: preceded by newline + spaces
        m = re.search(r'\n\s+' + re.escape(key) + r':\s*`[^`]*`', content)
        if m:
            return m.start(), m.end()
        return None

# Process from LAST to FIRST
keys_in_order = list(all_entries.keys())
# Reverse order so we process from tornozelo backwards to abdome
keys_reversed = list(reversed(keys_in_order))

print(f"Processing {len(keys_reversed)} entries in reverse order...")
for key in keys_reversed:
    new_entry_content = make_entry(key, all_entries[key])
    result = find_entry_range(content, key)
    if result is None:
        print(f"  {key}: NOT FOUND")
        continue
    start, end = result
    entry_text = content[start:end]
    print(f"  {key}: replacing at {start}-{end} ({len(entry_text)} chars) with {len(new_entry_content)} chars")
    content = content[:start] + new_entry_content + content[end:]

# Save
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("\nSaved!")
