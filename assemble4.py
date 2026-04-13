#!/usr/bin/env python3

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'resonancia: {'
end_marker = '},        tomografia: {'
start_idx = content.find(start_marker)
end_idx = content.find(end_marker)
print(f"Boundaries: start={start_idx}, end={end_idx}")

with open('/home/hal9000/Projects/Medscaner_prep/new_resonance_part1.txt', 'r') as f:
    part1 = f.read()
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part1b.txt', 'r') as f:
    part1b = f.read()
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part3.txt', 'r') as f:
    part3 = f.read()

import re

# Patch part1: it ends with "T2" (cut-off at end of coluna_toracica entry)
# part1 ends: "...T1 sagital, T2 SPIR/STIR sagital, T2"
# part1b starts: "axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio..."
# part1b's FIRST key is 'cotovelo' (after the continuation)

# Fix: remove trailing T2 from part1, add full continuation
# The continuation ends with `,\n\n            cotovelo: (just the KEY)
# Then part1b starts with axiais continuation + cotovelo content

if part1.rstrip().endswith('T2'):
    part1_base = part1[:len(part1)-2].rstrip()
    # Add continuation - this ends with `cotovelo: (key only)
    continuation = ' axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio 0,1 mmol/kg para neoplasia e espondilodiscite<br>• Gating respiratório ou apneias para minimizar artefatos<br>• Incluir de C7 a L1, com cobertura completa da coluna torácica<br>• Cortes sagitais 3mm, axiais 4mm perpendiculares ao eixo vertebral<br>• Avaliar: medula espinhal torácica, discos, corpos vertebrais, costelas adjacentes`,\n\n            cotovelo:'
    part1_fixed = part1_base + continuation
else:
    print(f"ERROR: Unexpected: {repr(part1[-50:])}")
    exit(1)

# Verify part1_fixed ends with cotovelo: key
print(f"part1_fixed ends: {repr(part1_fixed[-80:])}")
# Verify part1b starts with axiais continuation
print(f"part1b starts: {repr(part1b[:80])}")

# Now: part1_fixed ends with `cotovelo:` KEY
# part1b starts with continuation content + `cotovelo:` KEY + cotovelo CONTENT
# So we should NOT include the trailing `cotovelo:` in part1_fixed
# Remove the trailing `cotovelo:` from part1_fixed

part1_for_join = part1_fixed.rstrip()
if part1_for_join.rstrip().endswith('cotovelo:'):
    part1_for_join = part1_for_join[:len(part1_for_join)-8].rstrip()
    print(f"After removing trailing cotovelo: {repr(part1_for_join[-50:])}")

# Now part1_for_join ends with `,\n\n            ` and part1b starts with content
# The join should work correctly

new_resonance = part1_for_join + '\n\n            ' + part1b + part3

print(f"Total new resonance: {len(new_resonance)} chars")

keys = re.findall(r'\n\s+(\w+):', new_resonance)
unique = set(keys)
print(f"Total keys: {len(keys)}, unique: {len(unique)}")
dupes = set([k for k in keys if keys.count(k) > 1])
if dupes:
    print(f"WARNING - Duplicates: {dupes}")
    for d in dupes:
        positions = [i for i, k in enumerate(keys) if k == d]
        print(f"  {d} appears at positions: {positions}")

# Do replacement
new_content = content[:start_idx] + new_resonance + content[end_idx:]

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w') as f:
    f.write(new_content)

print("SUCCESS")

# Final verification
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r') as f:
    v = f.read()
keys_v = re.findall(r'\n\s+(\w+):', v)
# Filter out CSS
exam_words = {'display','opacity','cursor','width','padding','outline','transition','margin','color','transform','border','background','gap','height','left','top','right','bottom','position','font','text','line','z','min','max','flex','grid','align','content','justify','none','auto','solid','block','relative','absolute','fixed','hidden','visible','inherit','initial','underline','weight','size','family','style','spacing','indent','break','word','letter','white','overflow','vertical','horizontal','align','object','fill','stretch','center','start','end','baseline'}
exam_keys_v = [k for k in keys_v if k not in exam_words]
unique_v = set(exam_keys_v)
dupe_v = set([k for k in exam_keys_v if exam_keys_v.count(k) > 1])
print(f"Final exam keys: {len(unique_v)} unique, duplicates: {dupe_v if dupe_v else 'none'}")
print(f"Expected 29 exams, got {len(unique_v)}")
print(f"File size: {len(v)} chars")
