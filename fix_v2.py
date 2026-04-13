#!/usr/bin/env python3
"""Simple targeted replacements for each exam."""
import re

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_exam(key, new_content, data):
    """Replace a single exam entry in the HTML."""
    # Find the pattern: key: `<...> where the content starts
    # We need to find the entry boundary
    # Each exam entry ends before the next exam key
    pattern = key + r':\s*`[^`]*`'
    m = re.search(pattern, data)
    if m:
        data = data[:m.start()] + new_content + data[m.end():]
        print(f"  Replaced {key} ({m.end()-m.start()} chars)")
    else:
        print(f"  WARNING: {key} not found")
    return data

# The strategy: use the OLD generic content as unique search strings to identify each exam
# Then replace with the correct new content

# Since the original HTML had GENERIC content for all 29 exams (same template),
# I need to find a way to identify each one.

# The simplest approach: use the EXAM TITLE in the content to identify each entry.
# Each entry has: key: `<b>RESSONÂNCIA MAGNÉTICA DE {EXAM_TITLE} — TRI...
# The EXAM_TITLE is unique for each exam.

# So I can use: "RESSONÂNCIA MAGNÉTICA DE {EXAM_TITLE}" as the search pattern
# and replace the ENTIRE entry from that pattern to the next exam

def replace_by_title(title_pattern, key, new_entry, data):
    """Replace an exam by finding its title in content."""
    # Find where this title appears
    idx = data.find(title_pattern)
    if idx == -1:
        print(f"  WARNING: title '{title_pattern}' not found")
        return data
    
    # Find the start of this entry (go back to find key: `)
    # We need to find the key that precedes this title
    # Search backwards from idx for "keyname: `"
    search_start = max(0, idx - 200)
    preceding = data[search_start:idx]
    key_match = re.search(r'\n\s+(\w+):\s*`', preceding)
    if key_match:
        actual_key = key_match.group(1)
        if actual_key != key:
            print(f"  WARNING: found key '{actual_key}' for title '{title_pattern}', expected '{key}'")
    
    # Find where this entry starts
    entry_start = search_start + key_match.start() if key_match else idx - 5
    # entry_start = position of "key: `"
    
    # Find where this entry ends (at the next top-level key)
    remaining = data[entry_start + 10:]
    next_key_match = re.search(r'\n\s+\w+:\s*`', remaining)
    if next_key_match:
        entry_end = entry_start + 10 + next_key_match.start()
    else:
        entry_end = len(data)
    
    old_entry = data[entry_start:entry_end]
    print(f"  Replacing entry for '{key}' ({len(old_entry)} chars) with new content ({len(new_entry)} chars)")
    return data[:entry_start] + new_entry + data[entry_end:]

# Build new entries as simple strings (no backtick issues)
# Each new entry: "key: `<b>TITLE — TRIAGEM E PROTOCOLO</b><br>..." followed by `,
def make_entry(key, title, agend, anam, triag, prot):
    lines = [f"{key}: `<b>{title} — TRIAGEM E PROTOCOLO</b><br><br>"]
    lines.append("<b>1. INFORMAÇÕES PARA AGENDAMENTO:</b><br>")
    for x in agend:
        lines.append(f"• {x}<br>")
    lines.append("<br><b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>")
    for x in anam:
        lines.append(f"• {x}<br>")
    lines.append("<br><b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>")
    for x in triag:
        lines.append(f"• {x}<br>")
    lines.append("<br><b>4. RECOMENDAÇÕES AO TÉCNICO (Protocolo):</b><br>")
    for x in prot:
        lines.append(f"• {x}<br>")
    lines.append("`,")
    return ''.join(lines)

# Now build all 29 entries and replace them

entries = {}

entries['abdome'] = make_entry('abdome', 'RESSONÂNCIA MAGNÉTICA DE ABDOME',
    ['Jejum de 4–6 horas antes do contraste (diretriz ACR 2024)',
     'Perguntar sobre implantes metálico-eletrônicos (bomba de insulina, neuroestimulador) — contraindicação relativa',
     'Informar tempo médio de exame: 30–45 minutos',
     'Perguntar sobre claustrofobia — RM aberta ou sedação podem ser necessárias',
     'Não é necessário suspender medicações habituais',
     'Confirmar ausência de marca-passo convencional (contraindicação absoluta)',
     'Avaliar função renal (creatinina) se uso de gadolínio planejado (risco de NSF)',
     'Perguntar sobre nefropatia ou transplante renal prévio',
     'Orientar que gel de ultrassom pode ser usado na superfície abdominal'],
    ['Qual a indicação clínica principal? (lesão focal hepática, pancreática, adrenal?)',
     'Hepatopatia conhecida ou ferritina elevada? (sobrecarga hepática)',
     'História de doença renal ou diálise?',
     'Cirurgias abdominais prévias? (adesões podem limitar avaliação)',
     'Sintomas: dor, icterícia, perda de peso, alteração do hábito intestinal?',
     'Reação prévia a gadolínio?'],
    ['Lesões hepáticas focais — hemangioma, adenoma, carcinoma hepatocelular (CHC), metástases',
     'Esteatose hepática — quantificação com espectroscopia RM quando disponível',
     'Lesões pancreáticas — neoplasia sólida vs. cística (IPMN, serosa), pancreatite crônica',
     'Lesões adrenais — adenoma (wash-out), feocromocitoma, metástases',
     'Vias biliares — colangite, dilatação, estenoses obstrutivas',
     'Linfonodomegalias retroperitoneais e mesentéricas, ascite'],
    ['Bobina phased-array sobre o abdome + bobina corporal',
     'Sequências: T2 HASTE/coronal, T2 SPAIR/STIR, T1 Dixon (in-phase/opposed-phase), difusão (DWI b=50,400–800)',
     'Contraste dinâmico: gadolínio 0,1 mmol/kg, fase arterial tardia (15–20s), portal (60–70s), hepática (180s)',
     'Avaliar hepatoesplenomegalia, ascite, adenopatias',
     'Cortes axiais e coronais oblíquos, espessura ≤5mm para lesões pequenas'])

entries['cranio'] = make_entry('cranio', 'RESSONÂNCIA MAGNÉTICA DE CRÂNIO',
    ['Não é necessário jejum para estudo sem contraste',
     'Com contraste: jejum de 4 horas (prevenir náuseas/aspiração)',
     'Avaliar função renal se gadolínio será usado (NSF)',
     'Tempo de exame: 25–45 minutos',
     'Claustrofobia — a cabeça fica totalmente dentro do imã',
     'Confirmar ausência de marca-passo convencional (contraindicação absoluta)',
     'Perguntar sobre implantes metálicos intracranianos (clipes de aneurisma, stents, bobina de estimulação)',
     'Implantes cocleares — verificar compatibilidade com RM antes do exame'],
    ['Qual a indicação? (cefaleia, AVC, tumor, epilepsia, demência?)',
     'Cefaleia de início recente, súbita ou com sinais neurológicos?',
     'Déficits neurológicos focais (motor, sensitivo, linguagem)?',
     'Crises convulsivas? Quando foram as últimas?',
     'Perdas de consciência ou alterações de memória?',
     'Histórico de neoplasia sistêmica com risco de metástase cerebral?',
     'Doenças desmielinizantes conhecidas (esclerose múltipla)?'],
    ['Lesões expansivas intracranianas — glioma, meningioma, metástases, linfoma',
     'Doenças desmielinizantes — placas de EM (periventricular, juxtacortical, infratentorial)',
     'AVC isquêmico — avaliação de fase aguda (DWI), penumbra, core isquêmico',
     'Hemorragia intracraniana — epidural, subdural, subaracnóidea, intraparenquimatosa',
     'Malformações developmentais — Chiari, agenesia de corpo caloso, polimicrogiria',
     'Hidrocefalia — dilatação ventricular, causa obstrutiva vs. comunicante'],
    ['Bobina de crânio phased-array',
     'Sequências: FLAIR, DWI (b=0,1000), T1 spin-echo, T2 TSE, SWI (susceptibilidade)',
     'Contraste: T1+MPRAGE pós-gadolínio 0,1 mmol/kg para lesões tumorais e inflamatórias',
     'Avaliar fossa posterior e junção crânio-cervical para Chiari',
     'Incluir órbitas e base do crânio na avaliação',
     'Cortes axiais 5mm, coronais e sagitais quando indicado',
     'SWI para micro-hemorragias, cavernoma, petéquias'])

# Find resonance block
start = content.find('resonancia: {')
end = content.find('},        tomografia: {')
before = content[:start]
block = content[start:end]
after = content[end:]

print(f"Block has {len(block)} chars")

# Replace each exam
for key, new_entry in entries.items():
    block = replace_by_title(None, key, new_entry, block)

# Save
new_content = before + block + after
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")
