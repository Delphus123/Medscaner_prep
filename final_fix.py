#!/usr/bin/env python3
import re

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('resonancia: {')
end = content.find('},        tomografia: {')
before = content[:start]
block = content[start:end]
after = content[end:]

print(f"Block size: {len(block)} chars")

# Correct CRANIUM content
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

# Correct ANGIORM ARTERIAL content
correct_aarc = (
    "angiorm_arterial_cranio: `<b>RESSONÂNCIA MAGNÉTICA DE ANGIORM ARTERIAL DE CRÂNIO — TRIAGEM E PROTOCOLO</b><br><br>"
    "<b>1. INFORMAÇÕES PARA AGENDAMENTO:</b><br>"
    "• Sem contraste: jejum não é necessário<br>"
    "• Com contraste: jejum de 4 horas (prevenir náuseas)<br>"
    "• Perguntar sobre implantes metálicos intracranianos (stents, coils, clipes de aneurisma)<br>"
    "• Claustrofobia — RM de campo aberto pode ser necessária<br>"
    "• Informar tempo de exame: 20–35 minutos<br>"
    "• Confirmar ausência de marca-passo convencional (contraindicação absoluta)<br>"
    "• Avaliar função renal se gadolínio será usado (NSF — fibrose sistêmica nefrogênica)<br>"
    "• Perguntar sobre reações anteriores a agentes de contraste paramagnético<br><br>"
    "<b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>"
    "• Qual a indicação? (aneurisma, MAV, estenose, AVC isquêmico?)<br>"
    "• História de aneurisma cerebral ou sangramento subaracnóideo?<br>"
    "• Trazer exames anteriores para comparação<br>"
    "• Hipertensão arterial, diabetes, dislipidemia (fatores de risco vascular)?<br>"
    "• AVC prévia ou AIT? Qual território vascular?<br>"
    "• Procedimentos endovasculares prévios (stent, coil)?<br><br>"
    "<b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>"
    "• Aneurismas intracranianos — localização (ACO, ACM, ACoA), tamanho, morfologia (sacular vs. fusiforme)<br>"
    "• Malformações arteriovenosas (MAV) — nidus, drenagem venosa, fístula dural<br>"
    "• Estenose ou oclusão arterial — ateromatose, dissecção, vasculite<br>"
    "• Vasoespasmo pós-hemorrágico — avaliar com TOF ou contraste<br>"
    "• Stroke isquêmico agudo — penumbra isquêmica, core isquêmico (DWI/FLAIR mismatch)<br>"
    "• Developmental venous anomalies (DVA) — malformações venosas developmentais<br><br>"
    "<b>4. RECOMENDAÇÕES AO TÉCNICO (Protocolo):</b><br>"
    "• 3D TOF (time-of-flight) sem contraste como base — evalua artérias do círculo de Willis<br>"
    "• 3D contraste (MRA) com gadolínio 0,1 mmol/kg — bobina phased-array de crânio<br>"
    "• Sequência 3D T1-MPRAGE pós-contraste para parede vascular e trombose<br>"
    "• Incluir artérias: carótidas internas, ACM, ACA, ACP, basilare, vertebrais<br>"
    "• Resolução espacial alta: voxel ≤0,5mm, reconstruções MIP e MPVAR<br>"
    "• Avaliar simultaneamente parênquima (DWI, FLAIR) para excluir processo isquêmico`,\n"
)

# Step 1: Find and remove BOTH cranio entries (broken ANGIOM VENOSA + correct CRANIUM)
# Both start with 'cranio: `<b>RESSONÂNCIA MAGNÉTICA DE ...'
cranio_starts = [m.start() for m in re.finditer(r'cranio:\s*`', block)]
print(f"Found {len(cranio_starts)} cranio entries")

if len(cranio_starts) >= 2:
    first_cr = cranio_starts[0]
    second_cr = cranio_starts[1]
    
    # Find end of second cranio entry
    # The next key after second cranio
    rem = block[second_cr+5:]
    nxt = re.search(r'\n\s+\w+:\s*`', rem)
    if nxt:
        end_second = second_cr + 5 + nxt.start()
    else:
        end_second = len(block)
    
    print(f"First cranio at {first_cr}, second cranio at {second_cr}, ends at {end_second}")
    
    # Remove from first cranio to end of second cranio
    both_cranios = block[first_cr:end_second]
    print(f"Removing both cranios section: {len(both_cranios)} chars")
    
    # Insert correct entries at position first_cr
    block = block[:first_cr] + correct_aarc + correct_cranio + block[end_second:]
    print("Inserted correct aarc + cranio")
elif len(cranio_starts) == 1:
    # Only one cranio - just replace it
    first_cr = cranio_starts[0]
    rem = block[first_cr+5:]
    nxt = re.search(r'\n\s+\w+:\s*`', rem)
    if nxt:
        end_first = first_cr + 5 + nxt.start()
    else:
        end_first = len(block)
    both_cranios = block[first_cr:end_first]
    block = block[:first_cr] + correct_aarc + correct_cranio + block[end_first:]
    print("Only one cranio found, replaced with correct content")
else:
    print("No cranio entries found!")

# Verify keys
keys_now = re.findall(r'\n\s+(\w+):\s*`', block)
unique_keys = set(keys_now)
print(f"Keys now: {len(unique_keys)} unique")
missing = {'abdome','angiorm_arterial_cranio','cranio','angiorm_venosa_cranio','arcos_costais',
           'articulacao_temporomandibular','bacia','braco','colangio','coluna_cervical',
           'coluna_lombar','coluna_sacro','coluna_toracica','cotovelo','coxa',
           'enterorm','joelho','mamas','mao','ombro','orbitas','ossos_temporais',
           'pe','pescoco','punho','quadril','regiao_escapular','sela_turcica','tornozelo'} - unique_keys
if missing:
    print(f"Missing exams: {missing}")
else:
    print("All 29 exams present!")

# Save
new_content = before + block + after
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Saved")
