#!/usr/bin/env python3
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('resonancia: {')
end = content.find('},        tomografia: {')
before = content[:start]
block = content[start:end]
after = content[end:]

# Find crânio block and what comes after it
c_idx = block.find('cranio:')
# Find the next key after cranio
next_keys = ['angior', 'arcos', 'articulacao', 'bacia', 'braco', 'colangio']
next_pos = len(block)
for k in next_keys:
    pos = block.find('\n            ' + k, c_idx + 10)
    if pos != -1 and pos < next_pos:
        next_pos = pos

cranio_block = block[c_idx:next_pos]
print(f'cranio block: {len(cranio_block)} chars')
print(f'Starts: {repr(cranio_block[:80])}')

# Build correct crânio content (no backticks in the string literal itself)
correct_cranio = (
    "cranio: `<b>RESSONÂNCIA MAGNÉTICA DE CRÂNIO — TRIAGEM E PROTOCOLO</b><br><br>"
    "<b>1. INFORMAÇÕES PARA AGENDAMENTO:</b><br>"
    "• Não é necessário jejum para estudo sem contraste<br>"
    "• Com contraste: jejum de 4 horas (prevenir náuseas/aspiração)<br>"
    "• Avaliar função renal se gadolínio será usado (NSF)<br>"
    "• Tempo de exame: 25–45 minutos<br>"
    "• Claustrofobia — a cabeça fica totalmente dentro do imã<br>"
    "• Confirmar ausência de marca-passo convencional (contraindicação absoluta)<br>"
    "• Perguntar sobre implantes metálicos intracranianos (clipes de aneurisma, stents, bobina de estimulação)<br>"
    "• Implantes cocleares — verificar compatibilidade com RM antes do exame<br><br>"
    "<b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>"
    "• Qual a indicação? (cefaleia, AVC, tumor, epilepsia, demência?)<br>"
    "• Cefaleia de início recente, súbita ou com sinais neurológicos?<br>"
    "• Déficits neurológicos focais (motor, sensitivo, linguagem)?<br>"
    "• Crises convulsivas? Quando foram as últimas?<br>"
    "• Perdas de consciência ou alterações de memória?<br>"
    "• Histórico de neoplasia sistêmica com risco de metástase cerebral?<br>"
    "• Doenças desmielinizantes conhecidas (esclerose múltipla)?<br><br>"
    "<b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>"
    "• Lesões expansivas intracranianas — glioma, meningioma, metástases, linfoma<br>"
    "• Doenças desmielinizantes — placas de EM (periventricular, juxtacortical, infratentorial)<br>"
    "• AVC isquêmico — avaliação de fase aguda (DWI), penumbra, core isquêmico<br>"
    "• Hemorragia intracraniana — epidural, subdural, subaracnóidea, intraparenquimatosa<br>"
    "• Malformações developmentais — Chiari, agenesia de corpo caloso, polimicrogiria<br>"
    "• Hidrocefalia — dilatação ventricular, causa obstrutiva vs. comunicante<br><br>"
    "<b>4. RECOMENDAÇÕES AO TÉCNICO (Protocolo):</b><br>"
    "• Bobina de crânio phased-array<br>"
    "• Sequências: FLAIR, DWI (b=0,1000), T1 spin-echo, T2 TSE, SWI (susceptibilidade)<br>"
    "• Contraste: T1+MPRAGE pós-gadolínio 0,1 mmol/kg para lesões tumorais e inflamatórias<br>"
    "• Avaliar fossa posterior e junção crânio-cervical para Chiari<br>"
    "• Incluir órbitas e base do crânio na avaliação<br>"
    "• Cortes axiais 5mm, coronais e sagitais quando indicado<br>"
    "• SWI para micro-hemorragias, cavernoma, petéquias`,\n"
)

if cranio_block in block:
    block = block.replace(cranio_block, correct_cranio, 1)
    print("Replacement done")
else:
    print("ERROR: cranio block not found exactly")
    # Try to find approximate location
    idx = block.find('AN')
    if idx != -1:
        print(f"Found AN at {idx}: {repr(block[idx:idx+50])}")

new_content = before + block + after
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("File saved")

# Verify
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    v = f.read()
s = v.find('resonancia: {')
e = v.find('},        tomografia: {')
blk = v[s:e]
c = blk.find('cranio:')
ne = blk.find('\n            ', c+10)
cr = blk[c:ne if ne != -1 else c+3000]
print(f"Verified cranio first 100: {repr(cr[:100])}")
print(f"Verified cranio has FLAIR: {'FLAIR' in cr}")
print(f"Verified cranio has SWI: {'SWI' in cr}")
print(f"Verified cranio has DWI: {'DWI' in cr}")
