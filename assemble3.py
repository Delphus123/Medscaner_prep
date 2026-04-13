#!/usr/bin/env python3

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'resonancia: {'
end_marker = '},        tomografia: {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)
print(f"Boundaries: start={start_idx}, end={end_idx}")

# Load parts
with open('/home/hal9000/Projects/Medscaner_prep/new_resonance_part1.txt', 'r', encoding='utf-8') as f:
    part1 = f.read()
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part1b.txt', 'r', encoding='utf-8') as f:
    part1b = f.read()
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part3.txt', 'r', encoding='utf-8') as f:
    part3 = f.read()

# Patch part1: it ends with "T2" (cut-off at end of coluna_toracica entry)
# part1 ends: "...T1 sagital, T2 SPIR/STIR sagital, T2" (T2 is the cut-off)
# part1b starts: "axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio..."
# The continuation of the coluna_toracica entry should be appended to part1
# Then cotovelo: starts in part1b

# Check where column_toracica ends in part1
import re
# Find the end of column_toracica entry in part1
# The pattern: after "coluna_toracica: `<b>...(protocol)...`,"
# Then next exam key starts
coluna_end_in_part1 = part1.find('`,\n\n            cotovelo:')
print(f"coluna_toracica ends at position: {coluna_end_in_part1}")

if coluna_end_in_part1 == -1:
    # Find where the column_toracica entry ends
    # The last complete exam should be coluna_sacro
    # column_toracica starts with "coluna_toracica: `"
    col_t_idx = part1.find('coluna_toracica: `')
    print(f"coluna_toracica starts at: {col_t_idx}")
    # Find where it ends - look for "},\n            cotovelo"
    col_end_marker = '`,\n\n            cotovelo:'
    col_t_end = part1.find(col_end_marker, col_t_idx)
    print(f"coluna_toracica ends at: {col_t_end}")
    
    # The part1 ends with "T2" which is part of the column_toracica protocol
    # The full protocol end should replace the trailing "T2"
    # We need to cut part1 at "T2" and add the continuation
    
    # Find the last occurrence of "T2" at the end
    part1_ends_t2 = part1.rstrip().endswith('T2')
    print(f"part1 ends with T2: {part1_ends_t2}")
    
    # part1_ends = "...T1 sagital, T2 SPIR/STIR sagital, T2" (truncated)
    # We need to replace the trailing "T2" with the full continuation:
    # " axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio..."
    
    if part1.rstrip().endswith('T2'):
        # Get part1 without the trailing T2
        part1_base = part1[:len(part1)-2].rstrip()
        # Add the continuation
        continuation = ' axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio 0,1 mmol/kg para neoplasia e espondilodiscite<br>• Gating respiratório ou apneias para minimizar artefatos<br>• Incluir de C7 a L1, com cobertura completa da coluna torácica<br>• Cortes sagitais 3mm, axiais 4mm perpendiculares ao eixo vertebral<br>• Avaliar: medula espinhal torácica, discos, corpos vertebrais, costelas adjacentes`,\n\n            cotovelo:'
        part1_fixed = part1_base + continuation
    else:
        print(f"ERROR: Unexpected ending: {repr(part1[-100:])}")
        exit(1)
else:
    print("coluna_toracica already complete in part1")
    part1_fixed = part1.rstrip()
    if not part1_fixed.endswith('`,'):
        part1_fixed = part1_fixed + '`,'
    # Ensure it ends with `,\n\n            cotovelo:
    if not part1_fixed.endswith('`,\n\n            cotovelo:'):
        part1_fixed = part1_fixed.rstrip().rstrip(',') + '`,\n\n            cotovelo:'

print(f"part1_fixed ends with: {repr(part1_fixed[-100:])}")
print(f"part1b starts with: {repr(part1b[:100])}")

# Verify part1b starts with the continuation of coluna_toracica
# (i.e., starts with "axiais, difusão...")
assert part1b.startswith('axiais, difusão'), f"part1b bad start: {part1b[:50]}"

# Concatenate: part1_fixed (ends with "cotovelo:") + part1b (starts with continuation + cotovelo content)
# This would create duplicate cotovelo! Need to remove cotovelo from part1_fixed

# Actually: part1_fixed ends with "`,\n\n            cotovelo:" (the KEY, not content)
# part1b starts with "axiais, difusão...`,\n\n            cotovelo: `..." (continuation of column_toracica, then cotovelo CONTENT)
# So part1_fixed = [...coluna_toracica..., `,\n\n            cotovelo:]
# part1b = [axiais continuation, `,\n\n            cotovelo: `cotovelo content...]

# The correct assembly:
# part1_fixed ends with: `,\n\n            cotovelo: (just the key, no content)
# part1b starts with: axiais continuation (this IS the cotovelo content)
# So: part1_fixed + part1b = complete column_toracica + cotovelo + ... + pescoco

new_resonance = part1_fixed + part1b + part3

print(f"Total new resonance: {len(new_resonance)} chars")

# Check for duplicate exam keys
keys = re.findall(r'\n\s+(\w+):', new_resonance)
unique = set(keys)
if len(keys) != len(unique):
    dupes = set([k for k in keys if keys.count(k) > 1])
    print(f"WARNING - Duplicate exam keys: {dupes}")
else:
    print(f"All {len(unique)} exam keys are unique")

# Do replacement
new_content = content[:start_idx] + new_resonance + content[end_idx:]

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: File updated")

# Verify
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    v = f.read()
keys_v = re.findall(r'\n\s+(\w+):', v)
unique_v = set(keys_v)
# Filter out CSS properties that might match
exam_keys = [k for k in keys_v if k not in ('display', 'opacity', 'cursor', 'width', 'padding', 'outline', 'transition', 'margin', 'color', 'transform', 'border', 'background', 'gap', 'height', 'left', 'top', 'right', 'bottom', 'position', 'font', 'text', 'line', 'z', 'min', 'max', 'flex', 'grid', 'align', 'content', 'justify')]
unique_exam = set(exam_keys)
dupe_exam = set([k for k in exam_keys if exam_keys.count(k) > 1])
print(f"Final: {len(unique_exam)} exam keys, duplicates: {dupe_exam if dupe_exam else 'none'}")
print(f"File size: {len(v)} chars")
