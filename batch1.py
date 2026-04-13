
#!/usr/bin/env python3
import re

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def me(key, title, a, b, c, d):
    parts = [key + ': `<b>' + title + ' \xe2\x80\x94 TRIAGEM E PROTOCOLO</b><br><br>']
    parts.append('<b>1. INFORMA\xc3\x87\xc3\x95ES PARA AGENDAMENTO:</b><br>')
    for x in a: parts.append('\xe2\x80\xa2 ' + x + '<br>')
    parts.append('<br><b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>')
    for x in b: parts.append('\xe2\x80\xa2 ' + x + '<br>')
    parts.append('<br><b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>')
    for x in c: parts.append('\xe2\x80\xa2 ' + x + '<br>')
    parts.append('<br><b>4. RECOMENDA\xc3\x87\xc3\x95ES AO T\xc3\x89CNICO (Protocolo):</b><br>')
    for x in d: parts.append('\xe2\x80\xa2 ' + x + '<br>')
    parts.append('`,')
    return ''.join(parts)

entries = {}

entries['abdome'] = me('abdome','RESSON\xc3\x82NCIA MAGN\xcTICA DE ABDOME',
    ['Jejum de 4\xe2\x80\x936 horas antes do contraste (diretriz ACR 2024)','Perguntar sobre implantes met\xc3\xa1lico-eletr\xc3\xb4nicos (bomba de insulina, neuroestimulador) \xe2\x80\x94 contraindica\xc3\xa7\xc3\xa3o relativa','Informar tempo m\xc3\xa9dio de exame: 30\xe2\x80\x9345 minutos','Perguntar sobre claustrofobia \xe2\x80\x94 RM aberta ou sedacao podem ser necess\xc3\xa1rias','N\xc3\xa3o \xc3\xa9 necess\xc3\xa1rio suspender medica\xc3\xa7\xc3\xb5es habituais','Confirmar aus\xc3\xaancia de marca-passo convencional (contraindica\xc3\xa7\xc3\xa3o absoluta)','Avaliar fun\xc3\xa7\xc3\xa3o renal (creatinina) se uso de gadol\xc3\xadnio planejado (risco de NSF)','Perguntar sobre nefropatia ou transplante renal pr\xc3\xa9vio','Orientar que gel de ultrassom pode ser usado na superf\xc3.ad cie abdominal'],
    ['Qual a indica\xc3\xa7\xc3\xa3o cl\xc3\xadnica principal? (lesao focal hep\xe1 tica, pancre\xe1 tica, adrenal?)','Hepatopatia conhecida ou ferritina elevada? (sobrecarga hep\xe1 tica)','Hist\xc3\xb3ria de doen\xe7a renal ou di\xe1 lise?','Cirurgias abdominais pr\xc3\xa9vias? (ades\u00f5es podem limitar avalia\xe7\xe3o)','Sintomas: dor, icter\xe7cia, perda de peso, altera\xe7\xe3o do h\xe1bito intestinal?','Rea\xe7\xe3o pr\xe9via a gadol\xednio?'],
    ['Les\u00f5es hep\xe1ticas focais \xe2\x80\x94 hemangioma, adenoma, carcinoma hepatocelular (CHC), met\xe1stases','Esteatose hep\xe1tica \xe2\x80\x94 quantifica\xe7\xe3o com espectroscopia RM quando dispon\xe1vel','Les\u00f5es pancre\xe1ticas \xe2\x80\x94 neoplasia s\u00f3lida vs. c\u00edstica (IPMN, serosa), pancreatite cr\u00f4nica','Les\u00f5es adrenais \xe2\x80\x94 adenoma (wash-out), feocromocitoma, met\xe1stases','Vias biliares \xe2\x80\x94 colangite, dilata\xe7\xe3o, estenoses obstrutivas','Linfonodomegalias retroperitoneais e mesent\xe9ricas, ascite'],
    ['Bobina phased-array sobre o abdome + bobina corporal','Sequ\u00eancias: T2 HASTE/coronal, T2 SPAIR/STIR, T1 Dixon (in-phase/opposed-phase), difus\u00e3o (DWI b=50,400\u2013800)','Contraste din\u00e2mico: gadol\u00ednio 0,1 mmol/kg, fase arterial tardia (15\u201320s), portal (60\u201370s), hep\u00e1tica (180s)','Avaliar hepatoesplenomegalia, ascite, adenopatias','Cortes axiais e coronais obl\u00edquos, espessura \u22645mm para les\u00f5es pequenas'])

entries['joelho'] = me('joelho','RESSON\u00c3NCIA MAGN\u00c9TICA DE JOELHO',
    ['N\u00e3o \u00e9 necess\u00e1rio jejum','Tempo de exame: 25\u201340 minutos','Claustrofobia geralmente m\u00ednima para esta regi\u00e3o','Confirmar aus\u00eancia de implantes met\u00e1licos (pr\u00f3teses, parafusos) \u2014 artefactos','Avaliar fun\u00e7\u00e3o renal se contraste ser\u00e1 usado (tumores, infec\u00e7\u00f5es)','Informar que o joelho ser\u00e1 posicionado em ligera flex\u00e3o (10\u201315 graus)','Perguntar sobre les\u00f5es pr\u00e9vias, cirurgias ou artroscopia','Roupas sem elementos met\u00e1licos na regi\u00e3o inferior'],
    ['Qual a indica\u00e7\u00e3o? (trauma, dor, instabilidade, tumor, infec\u00e7\u00e3o?)','Mecanismo do trauma (tor\u00e7\u00e3o, impacto direto, hiperextens\u00e3o)?','Bloqueio articular, falsejo ou instabilidade?','Derrame articular palp\u00e1vel?','Dor em linha articular medial ou lateral, ou retropatelar?','Hist\u00f3rico de ligamentoplastia ou meniscectomia pr\u00e9via?','Sintomas de bloqueio mec\u00e2nico vs. dor inflamat\u00f3ria?'],
    ['Les\u00f5es meniscais \u2014 l\u00e1grima horizontal, vertical, radial, em al\u00e7a de balde (root tear)','Les\u00f5es ligamentares \u2014 LCA (mais comum), LCP, LCM, LLI','Les\u00f5es condrais \u2014 classifica\u00e7\u00e3o de Outerbridge, osteocondrite dissecante (OCD)','Cisto de Baker \u2014 cole\u00e7\u00e3o popl\u00edtea, comunicar com articula\u00e7\u00e3o','Gonartrose \u2014 oste\u00f3fitos, edema subcondral (Modic-like), pin\u00e7amento articular','Tumores \u2014 osteossarcoma, condroblastoma, tumor de c\u00e9lulas gigantes (TCG)'],
    ['Bobina de joelho dedicada ou bobina de superf\u00edcie phased-array','Sequ\u00eancias: PD FS e T2 FS (sagital e coronal) para meniscos e ligamentos','T1 sagital e coronal para anatomia \u00f3ssea e gordura','GRE (gradient echo) 3D para cartilagem (MapChange ou VIBE)','Contraste com gadol\u00ednio 0,1 mmol/kg para tumores, infec\u00e7\u00f5es, sinovite','DWI para caracteriza\u00e7\u00e3o de les\u00f5es tumorais e infec\u00e7\u00e3o','Posicionamento: ligera flex\u00e3o 10\u201315 graus, p\u00e9 em rota\u00e7\u00e3o externa','Cortes: sagital 4mm, coronal 3mm, axial 4mm quando necess\u00e1rio'])

for key, new_entry in entries.items():
    pattern = r'\n\s+' + re.escape(key) + r':\s*`[^`]*`'
    m = re.search(pattern, content)
    if m:
        old_len = m.end() - m.start()
        content = content[:m.start()] + '\n    ' + new_entry + content[m.end():]
        print(f'{key}: replaced ({old_len} -> {len(new_entry)} chars)')
    else:
        print(f'{key}: NOT FOUND')

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved!')
