#!/usr/bin/env python3

# Read the original file
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if it was already replaced (has new specific content)
if 'MODIC CHANGES' in content.upper() or 'Modic changes' in content:
    print("File already has specific content, checking for duplicates...")

# The last correctly replaced file was at index 17817 to 67708
# But that included duplicates from part2. Let's fix by replacing again.

# Find current boundaries
start_marker = 'resonancia: {'
end_marker = '},        tomografia: {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print(f"Found: start={start_idx}, end={end_idx}")

# Load parts 1, 1b, and 3 (skip duplicate part 2)
with open('/home/hal9000/Projects/Medscaner_prep/new_resonance_part1.txt', 'r', encoding='utf-8') as f:
    part1 = f.read()
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part1b.txt', 'r', encoding='utf-8') as f:
    part1b = f.read()
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part3.txt', 'r', encoding='utf-8') as f:
    part3 = f.read()

# Fix part1 - it ends with "T2" (cut-off). Need to complete the coluna_toracica entry
# part1 ends: "...T1 sagital, T2 SPIR/STIR sagital, T2"
# part1b starts: "axiais, difusão (DWI) para tumor/infecção..."
# The fix: remove the trailing "T2" from part1 and add full continuation
part1_patched = part1.rstrip()
if part1_patched.endswith('T2'):
    # Fix by replacing the trailing T2 with full continuation
    part1_patched = part1_patched[:-2].rstrip()
    continuation = ' axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio 0,1 mmol/kg para neoplasia e espondilodiscite<br>• Gating respiratório ou apneias para minimizar artefatos<br>• Incluir de C7 a L1, com cobertura completa da coluna torácica<br>• Cortes sagitais 3mm, axiais 4mm perpendiculares ao eixo vertebral<br>• Avaliar: medula espinhal torácica, discos, corpos vertebrais, costelas adjacentes`,\n\n            cotovelo:'
    part1_patched = part1_patched + continuation
    print(f"Part1 patched. Length: {len(part1_patched)}")
else:
    print(f"WARNING: part1 doesn't end with expected 'T2', ending is: {repr(part1_patched[-50:])}")
    part1_patched = part1_patched.rstrip()
    # Find if there's already a cotovelo entry
    if 'cotovelo' in part1_patched:
        print("Part1 already has cotovelo, not patching")
    else:
        print("ERROR: Cannot patch part1")

# Verify part1b starts correctly
assert part1b.startswith('axiais, difusão'), f"part1b doesn't start correctly: {part1b[:50]}"
print(f"Part1b starts correctly: {part1b[:50]}")

# Verify part3 ends correctly
assert part3.rstrip().endswith("tomografia: {"), f"part3 doesn't end correctly: {part3[-50:]}"
print(f"Part3 ends correctly: ...{part3[-50:]}")

# Concatenate
new_resonance = part1_patched + part1b + part3

print(f"Total new resonance block length: {len(new_resonance)} chars")

# Check for duplicates in the assembled content
import re
keys = re.findall(r'\n\s+(\w+):', new_resonance)
unique_keys = set(keys)
if len(keys) != len(unique_keys):
    dupes = [k for k in keys if keys.count(k) > 1]
    print(f"WARNING: Duplicate exams found: {set(dupes)}")
else:
    print(f"All {len(unique_keys)} exams are unique")

# Do the replacement
new_content = content[:start_idx] + new_resonance + content[end_idx:]

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: File updated")

# Verify
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    verify = f.read()

keys_final = re.findall(r'\n\s+(\w+):', verify)
unique_final = set(keys_final)
dupe_final = [k for k in keys_final if keys_final.count(k) > 1]
print(f"Final file: {len(unique_final)} unique exams, duplicates: {set(dupe_final) if dupe_final else 'none'}")
print(f"File size: {len(verify)} chars")
