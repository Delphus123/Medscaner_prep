#!/usr/bin/env python3
"""Replace all 29 RM exam entries with exam-specific content."""
import re, json

# Load and merge all batches
all_entries = {}
for i in range(1, 6):
    with open(f'/home/hal9000/Projects/Medscaner_prep/entries_batch{i}.json', 'r', encoding='utf-8') as f:
        batch = json.load(f)
    all_entries.update(batch)
print(f"Loaded {len(all_entries)} entries")

# Load HTML
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find resonance block boundaries
res_start = content.find('resonancia: {')
# tomografia: { at 67718, preceded by `,\n\n        },        `
# Resonance block closes at position 67709 (the `}` before the comma)
res_end = 67709

print(f"Resonance block: {res_start} to {res_end} ({res_end - res_start} chars)")

def make_entry(key, data):
    """Build a single exam entry content (no trailing comma)."""
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

def replace_entry(content, key, new_entry):
    """Replace a single exam entry in the content string."""
    if key == 'abdome':
        # First entry: no leading newline, starts right after `resonancia: {`
        pattern = r'abdome:\s*`[^`]*`'
    else:
        pattern = r'\n\s+' + re.escape(key) + r':\s*`[^`]*`'

    m = re.search(pattern, content)
    if not m:
        print(f"  {key}: NOT FOUND")
        return content, False

    # After the match (which ends at the closing backtick):
    # Non-last entries: `,\n\n            ` + next_key  (15 chars: comma, 2 newlines, 12 spaces)
    # Last entry: `,\n\n        },\n    };`  (18 chars: comma, 2 newlines, 8 spaces, }, newline, 4 spaces, ;)
    rest = content[m.end():]

    # Detect if last entry by checking character at position 11 after match
    # Last: char[11] == '}' (closing brace of resonance)
    # Non-last: char[11] == ' ' (indentation of next key)
    if len(rest) >= 12 and rest[11] == '}':
        keep_len = 18  # last entry
    else:
        keep_len = 15  # non-last

    old_total = (m.end() + keep_len) - m.start()
    content = content[:m.start()] + new_entry + content[m.end() + keep_len:]
    print(f"  {key}: OK ({old_total} -> {len(new_entry)} chars)")
    return content, True

# Replace each entry
replaced = 0
for key in all_entries:
    new_entry = make_entry(key, all_entries[key])
    content, success = replace_entry(content, key, new_entry)
    if success:
        replaced += 1

print(f"\nReplaced {replaced}/{len(all_entries)} entries")

# Save
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved!")
