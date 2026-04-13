#!/usr/bin/env python3
import os

# Read all parts
parts = []

# Part1: resonance_part1.txt (ends with T2 at end of coluna_toracica protocol section)
with open('/home/hal9000/Projects/Medscaner_prep/new_resonance_part1.txt', 'r', encoding='utf-8') as f:
    part1 = f.read()
# Fix the cut-off at end of coluna_toracica
# part1 ends: "...T1 sagital, T2 SPIR/STIR sagital, T2"
# part1b starts: "axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio..."
# So we need to fix the incomplete line
part1 = part1.rstrip()
if part1.endswith('T2'):
    # Fix the incomplete coluna_toracica entry
    part1 = part1 + ' axiais, difusão (DWI) para tumor/infecção<br>• Contraste com gadolínio 0,1 mmol/kg para neoplasia e espondilodiscite<br>• Gating respiratório ou apneias para minimizar artefatos<br>• Incluir de C7 a L1, com cobertura completa da coluna torácica<br>• Cortes sagitais 3mm, axiais 4mm perpendiculares ao eixo vertebral<br>• Avaliar: medula espinhal torácica, discos, corpos vertebrais, costelas adjacentes`,\n\n            cotovelo:'
else:
    # Find last complete exam in part1 and patch
    # Look for the end marker
    idx = part1.rfind('`,\n\n            cotovelo:')
    if idx != -1:
        part1 = part1[:idx+3] + '\n\n            cotovelo:'
        print("WARNING: part1 already has cotovelo, using as-is")
    else:
        print("ERROR: Cannot find expected boundary in part1")
        print(f"Last 200 chars: {repr(part1[-200:])}")

parts.append(part1)

# Read part1b
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part1b.txt', 'r', encoding='utf-8') as f:
    part1b = f.read()
parts.append(part1b)

# Part2: starts with continuation of coluna_toracica, ends with pescoco truncated
# pescoco ends with "...Contraste com gadol---"
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part2.txt', 'r', encoding='utf-8') as f:
    part2 = f.read()
parts.append(part2)

# Part3: starts with continuation of pescoco "...Contraste com gadolínio 0,1 mmol/kg para tumores..."
# ends with tornozelo and tomografia
with open('/home/hal9000/Projects/Medscaner_prep/new_res_part3.txt', 'r', encoding='utf-8') as f:
    part3 = f.read()
parts.append(part3)

# Concatenate
new_resonance = ''.join(parts)

print(f"Total new resonance block length: {len(new_resonance)} chars")

# Now replace in the HTML file
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'resonancia: {'
end_marker = '},        tomografia: {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: Could not find boundaries. start={start_idx}, end={end_idx}")
    exit(1)

print(f"Replacing from {start_idx} to {end_idx}")
print(f"Old block length: {end_idx - start_idx} chars")
print(f"New block length: {len(new_resonance)} chars")

new_content = content[:start_idx] + new_resonance + content[end_idx:]

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: File updated")
