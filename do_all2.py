#!/usr/bin/env python3
"""Replace all 29 RM exams with exam-specific content."""
import re, json

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def make_entry(key, title, a, b, c, d):
    lines = [key + ': `<b>' + title + ' \u2014 TRIAGEM E PROTOCOLO</b><br><br>']
    lines.append('<b>1. INFORMA\u00c7\u00d5ES PARA AGENDAMENTO:</b><br>')
    for x in a: lines.append('\u2022 ' + x + '<br>')
    lines.append('<br><b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>')
    for x in b: lines.append('\u2022 ' + x + '<br>')
    lines.append('<br><b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>')
    for x in c: lines.append('\u2022 ' + x + '<br>')
    lines.append('<br><b>4. RECOMENDA\u00c7\u00d5ES AO T\u00c9CNICO (Protocolo):</b><br>')
    for x in d: lines.append('\u2022 ' + x + '<br>')
    lines.append('`,')
    return ''.join(lines)

# Load entries from JSON
with open('/home/hal9000/Projects/Medscaner_prep/new_entries.json', 'r', encoding='utf-8') as f:
    new_entries = json.load(f)

print(f"Loaded {len(new_entries)} entries")

# Find resonance block
start = content.find('resonancia: {')
end = content.find('},        tomografia: {')
print(f"Block: {end-start} chars")

# Replace each entry
for key, data in new_entries.items():
    new_entry = make_entry(key, data['title'], data['agend'], data['anam'], data['triag'], data['prot'])
    # Find this key's entry in the block
    pattern = r'\n\s+' + re.escape(key) + r':\s*`[^`]*`'
    m = re.search(pattern, content)
    if m:
        old_len = m.end() - m.start()
        content = content[:m.start()] + '\n    ' + new_entry + content[m.end():]
        print(f"  {key}: OK ({old_len} -> {len(new_entry)} chars)")
    else:
        print(f"  {key}: NOT FOUND")

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved!")
