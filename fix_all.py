#!/usr/bin/env python3
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('resonancia: {')
end = content.find('},        tomografia: {')
before = content[:start]
block = content[start:end]
after = content[end:]

# Build correct content for each key
# Key -> (title, agendamento, anamnese, triagem, protocolo)
exams = {
    'abdome': ('RESSONÂNCIA MAGNÉTICA DE ABDOME',
        'Jejum de 4–6 horas antes do exame quando contraste for utilizado (diretriz ACR 2024)',
        [], [], []),
}

# I'll just rebuild the whole resonance block using the correct content
# Since I know the structure, let me replace the entire resonance block

# Correct entries for the exams that have WRONG content:
# - angiorm_venosa_cranio: has CRANIO content -> needs ANGIORM VENOSA content
# - cranio (second): duplicate, has CRANIO content -> needs REMOVED
# - sela_turcica: has CRANIO content -> needs SELA TURCICA content

# Find and fix angiorm_venosa_cranio
import re

# Find angiorm_venosa_cranio entry
aavc_idx = block.find('angiorm_venosa_cranio:')
# Next key after it
next_keys = ['\n            arcos', '\n            articulacao', '\n            bacia']
aavc_end = len(block)
for k in next_keys:
    pos = block.find(k, aavc_idx+10)
    if pos != -1 and pos < aavc_end:
        aavc_end = pos
aavc_entry = block[aavc_idx:aavc_end]
print(f'angiorm_venosa_cranio entry ({len(aavc_entry)} chars): {repr(aavc_entry[:100])}')

# Correct angiorm_venosa content
correct_aavc = (
    "angiorm_venosa_cranio: `<b>RESSONÂNCIA MAGNÉTICA DE ANGIORM VENOSA DE CRÂNIO — TRIAGEM E PROTOCOLO</b><br><br>"
    "<b>1. INFORMAÇÕES PARA AGENDAMENTO:</b><br>"
    "• Sem contraste: jejum não é necessário<br>"
    "• Com contraste: jejum de 4 horas<br>"
    "• Avaliar função renal (creatinina) se uso de gadolínio<br>"
    "• Perguntar sobre trombose venosa prévia ou fatores de risco (trombofilia, anticoncepcionais)<br>"
    "• Informar tempo de exame: 20–35 minutos<br>"
    "• Claustrofobia — explicar que a cabeça fica dentro do imã<br>"
    "• Confirmar ausência de marca-passo convencional, DIU de cobre é compatível<br>"
    "• Alertar que contraste será injetado para opacificar as veias<br><br>"
    "<b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>"
    "• Qual a indicação? (cefaleia, trombose venosa cerebral, avaliação de seios venosos?)<br>"
    "• Cefaleia de início recente ou com padrão atípico?<br>"
    "• Histórico de trombose venosa profunda ou superficial?<br>"
    "• Episódios de convulsões, déficit neurológico focal?<br>"
    "• Uso de anticoncepcionais orais, terapia hormonal (risco de TVC)?<br>"
    "• Neoplasia ocultada (síndrome de Trousseau)?<br>"
    "• Infecção sinusal recente ou mastoidite (risco de trombose de seio lateral)?<br><br>"
    "<b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>"
    "• Trombose venosa cerebral (TVC) — seios sagital superior, lateral, reto, jugular<br>"
    "• Vedadores venosos (seios) — aplasia ou hipoplasia, causa de HTIC benigna<br>"
    "• Mass effect sobre seios venosos por processos expansivos<br>"
    "• Tromboflebite intracraniana — extensão de processo infeccioso<br>"
    "• Colaterais venosos desenvolvidos — resultado de hipertensão intracraniana<br>"
    "• Infartos venosos — padrão hemorrágico cortical, edema vasogênico<br><br>"
    "<b>4. RECOMENDAÇÕES AO TÉCNICO (Protocolo):</b><br>"
    "• 2D/3D TOF venografia ou contraste com gadolínio 0,1 mmol/kg<br>"
    "• 3D T1 + saturação de gordura pós-contraste para avaliar trombose vs. recanalização<br>"
    "• Sequências parenquimatosas: FLAIR, DWI para excluir infarto venoso<br>"
    "• Incluir seios: sagital superior, lateral, reto, jugular<br>"
    "• Reconstruções MIP e multiplanar para avaliar continuidade venosa<br>"
    "• Avaliar edema, hemorragia ou infarto venoso associado`,\n"
)

if aavc_entry in block:
    block = block.replace(aavc_entry, correct_aavc, 1)
    print('angiorm_venosa_cranio fixed')
else:
    print('ERROR: angiorm_venosa_cranio entry not found')

# Find and remove duplicate cranio (the second one with CRANIO content, at pos ~31313)
# Find second cranio
cranio_positions = [m.start() for m in re.finditer(r'\n\s+cranio:', block)]
print(f'cranio positions: {cranio_positions}')
if len(cranio_positions) >= 2:
    # Remove the second cranio entry
    second_start = cranio_positions[1]
    # Find end of second cranio entry
    next_key = re.search(r'\n\s+\w+:\s*`', block[second_start+5:])
    if next_key:
        second_end = second_start + 5 + next_key.start()
        second_cranio = block[second_start-2:second_end]  # include \n\n
        block = block.replace(second_cranio, '', 1)
        print(f'Removed duplicate cranio ({len(second_cranio)} chars)')
    else:
        print('Could not find end of second cranio')

# Find and fix sela_turcica
st_idx = block.find('sela_turcica:')
if st_idx != -1:
    next_keys_st = ['\n            tornozelo']
    st_end = len(block)
    for k in next_keys_st:
        pos = block.find(k, st_idx+20)
        if pos != -1 and pos < st_end:
            st_end = pos
    st_entry = block[st_idx:st_end]
    print(f'sela_turcica entry ({len(st_entry)} chars): {repr(st_entry[:100])}')
    
    correct_st = (
        "sela_turcica: `<b>RESSONÂNCIA MAGNÉTICA DE SELA TURCICA — TRIAGEM E PROTOCOLO</b><br><br>"
        "<b>1. INFORMAÇÕES PARA AGENDAMENTO:</b><br>"
        "• Não é necessário jejum para estudo sem contraste<br>"
        "• Com contraste: jejum de 4 horas<br>"
        "• Tempo de exame: 25–40 minutos<br>"
        "• Claustrofobia relevante — a cabeça fica dentro do imã<br>"
        "• Avaliar função renal se gadolínio será usado (NSF)<br>"
        "• Confirmar ausência de marca-passo convencional (contraindicação absoluta)<br>"
        "• Perguntar sobre alterações hormonais, alterações visuais, galactorreia<br>"
        "• Informar que será usado contraste paramagnético para avaliar a hipófise<br><br>"
        "<b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>"
        "• Qual a indicação? (adenoma hipofisário, craniofaringioma, avaliação hormonal?)<br>"
        "• Alterações visuais — hemianopsia bitemporal, diplopia?<br>"
        "• Alterações hormonais — galactorreia, amenorreia, disfunção erétil, gigantismo/acromegalia?<br>"
        "• Cefaleia persistente ou atípica?<br>"
        "• Histórico de neoplasia sistêmica (risco de metástase hipofisária)?<br>"
        "• Cirurgias hipofisárias prévias ou radioterapia?<br>"
        "• Uso de bromocriptina, cabergolina ou outros análogos de dopamina?<br><br>"
        "<b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>"
        "• Adenoma hipofisário — macroadenoma (>10mm) vs. microadenoma (<10mm), realce<br>"
        "• Prolactinoma — mais comum, hipersinal em T2, responde a dopaminérgicos<br>"
        "• Craniofaringioma — cístico com calcificações (T1 variável), sólido, realce<br>"
        "• Hipofisite — realce difuso da hipófise, mais comum em mulheres pós-parto<br>"
        "• Cisto de Rathke — cisto na linha média, hipersinal em T1, sem realce<br>"
        "• Metástases — geralmente em contexto de neoplasia sistêmica conhecida<br><br>"
        "<b>4. RECOMENDAÇÕES AO TÉCNICO (Protocolo):</b><br>"
        "• Bobina de crânio phased-array<br>"
        "• Sequências: T1 sagital e coronal pré-contraste (finura 2–3mm na hipófise)<br>"
        "• T2 coronal para adenoma e cistos<br>"
        "• Contraste dinâmico com gadolínio 0,1 mmol/kg: séries precoces (30s, 60s, 90s, 120s)<br>"
        "• FLAIR e DWI para caracterização de lesões<br>"
        "• Incluir hipotálamo, quiasma óptico, seios cavernosos<br>"
        "• Cortes coronais e sagitais 2–3mm centrados na sela turca`,\n"
    )
    
    if st_entry in block:
        block = block.replace(st_entry, correct_st, 1)
        print('sela_turcica fixed')
    else:
        print('ERROR: sela_turcica entry not found')

# Save
new_content = before + block + after
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('File saved')

# Verify
with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    v = f.read()
blk = v[v.find('resonancia: {'):v.find('},        tomografia: {')]
keys = re.findall(r'\n\s+(\w+):\s*\`', blk)
print(f'Exams: {len(set(keys))} unique keys')
print('Keys:', list(dict.fromkeys(keys)))
