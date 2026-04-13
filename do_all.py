#!/usr/bin/env python3
import re

with open('/home/hal9000/Projects/Medscaner_prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def me(key, title, a, b, c, d):
    parts = [key + ': `<b>' + title + ' — TRIAGEM E PROTOCOLO</b><br><br>']
    parts.append('<b>1. INFORMAÇÕES PARA AGENDAMENTO:</b><br>')
    for x in a: parts.append('• ' + x + '<br>')
    parts.append('<br><b>2. PERGUNTAS PARA ANAMNESE (Enfermagem):</b><br>')
    for x in b: parts.append('• ' + x + '<br>')
    parts.append('<br><b>3. TRIAGEM DE PATOLOGIAS (Enfermagem):</b><br>')
    for x in c: parts.append('• ' + x + '<br>')
    parts.append('<br><b>4. RECOMENDAÇÕES AO TÉCNICO (Protocolo):</b><br>')
    for x in d: parts.append('• ' + x + '<br>')
    parts.append('`,')
    return ''.join(parts)

entries = {}

entries['abdome'] = me('abdome','RESSONÂNCIA MAGNÉTICA DE ABDOME',
    ['Jejum de 4–6 horas antes do contraste (diretriz ACR 2024)','Perguntar sobre implantes metálico-eletrônicos (bomba de insulina, neuroestimulador) — contraindicação relativa','Informar tempo médio de exame: 30–45 minutos','Perguntar sobre claustrofobia — RM aberta ou sedação podem ser necessárias','Não é necessário suspender medicações habituais','Confirmar ausência de marca-passo convencional (contraindicação absoluta)','Avaliar função renal (creatinina) se uso de gadolínio planejado (risco de NSF)','Perguntar sobre nefropatia ou transplante renal prévio','Orientar que gel de ultrassom pode ser usado na superfície abdominal'],
    ['Qual a indicação clínica principal? (lesão focal hepática, pancreática, adrenal?)','Hepatopatia conhecida ou ferritina elevada? (sobrecarga hepática)','História de doença renal ou diálise?','Cirurgias abdominais prévias? (adesões podem limitar avaliação)','Sintomas: dor, icterícia, perda de peso, alteração do hábito intestinal?','Reação prévia a gadolínio?'],
    ['Lesões hepáticas focais — hemangioma, adenoma, carcinoma hepatocelular (CHC), metástases','Esteatose hepática — quantificação com espectroscopia RM quando disponível','Lesões pancreáticas — neoplasia sólida vs. cística (IPMN, serosa), pancreatite crônica','Lesões adrenais — adenoma (wash-out), feocromocitoma, metástases','Vias biliares — colangite, dilatação, estenoses obstrutivas','Linfonodomegalias retroperitoneais e mesentéricas, ascite'],
    ['Bobina phased-array sobre o abdome + bobina corporal','Sequências: T2 HASTE/coronal, T2 SPAIR/STIR, T1 Dixon (in-phase/opposed-phase), difusão (DWI b=50,400–800)','Contraste dinâmico: gadolínio 0,1 mmol/kg, fase arterial tardia (15–20s), portal (60–70s), hepática (180s)','Avaliar hepatoesplenomegalia, ascite, adenopatias','Cortes axiais e coronais oblíquos, espessura ≤5mm para lesões pequenas'])

entries['joelho'] = me('joelho','RESSONÂNCIA MAGNÉTICA DE JOELHO',
    ['Não é necessário jejum','Tempo de exame: 25–40 minutos','Claustrofobia geralmente mínima para esta região','Confirmar ausência de implantes metálicos (próteses, parafusos) — artefactos','Avaliar função renal se contraste será usado (tumores, infecções)','Informar que o joelho será posicionado em ligera flexão (10–15 graus)','Perguntar sobre lesões prévias, cirurgias ou artroscopia','Roupas sem elementos metálicos na região inferior'],
    ['Qual a indicação? (trauma, dor, instabilidade, tumor, infecção?)','Mecanismo do trauma (torção, impacto direto, hiperextensão)?','Bloqueio articular, falsejo ou instabilidade?','Derrame articular palpável?','Dor em linha articular medial ou lateral, ou retropatelar?','Histórico de ligamentoplastia ou meniscectomia prévia?','Sintomas de bloqueio mecânico vs. dor inflamatória?'],
    ['Lesões meniscais — lágrima horizontal, vertical, radial, em alça de balde (root tear)','Lesões ligamentares — LCA (mais comum), LCP, LCM, LLI','Lesões condrais — classificação de Outerbridge, osteocondrite dissecante (OCD)','Cisto de Baker — coleção poplítea, comunicar com articulação','Gonartrose — osteófitos, edema subcondral (Modic-like), pinçamento articular','Tumores — osteossarcoma, condroblastoma, tumor de células gigantes (TCG)'],
    ['Bobina de joelho dedicada ou bobina de superfície phased-array','Sequências: PD FS e T2 FS (sagital e coronal) para meniscos e ligamentos','T1 sagital e coronal para anatomia óssea e gordura','GRE (gradient echo) 3D para cartilagem (MapChange ou VIBE)','Contraste com gadolínio 0,1 mmol/kg para tumores, infecções, sinovite','DWI para caracterização de lesões tumorais e infecção','Posicionamento: ligera flexão 10–15 graus, pé em rotação externa','Cortes: sagital 4mm, coronal 3mm, axial 4mm quando necessário'])

entries['mamas'] = me('mamas','RESSONÂNCIA MAGNÉTICA DE MAMAS',
    ['Marcar entre dia 7 e 14 do ciclo menstrual (fase proliferativa) para reduzir contraste de fundo (ACR)','Não é necessário jejum','Tempo de exame: 20–35 minutos mais mamografia convencional se simultânea','Claustrofobia — toda a região torácica anterior dentro do imã','Confirmar ausência de marca-passo e avaliar função renal se gadolínio','Trazer mamografias e ultrassonografias anteriores para comparação','Perguntar sobre antecedentes de neoplasia de mama e status de BRCA','Implantes mamários — informar tipo (salineira vs. silicone) para protocolo','Confirmar ausência de gestação (contraindicação relativa no 1º trimestre)'],
    ['Qual a indicação? (rastreio em alto risco, estadiamento, avaliação de resposta neoadjuvante?)','Data da última mamografia e resultado?','Mutação de BRCA1/BRCA2 conhecida?','Histórico pessoal de neoplasia de mama ou ovário?','Terapia hormonal atual ou prévia (TRH)?','Status menopausal?','Implantes mamários — tempo de colocação, tipo, ruptura prévia?'],
    ['Neoplasia de mama — carcinoma ductal invasivo (CDI), carcinoma lobular invasivo (CLI)','Lesões precursoras — LCIS, DCIS de alto grau (não calcificadas na RM)','Implantes mamários — ruptura intracapsular ou extracapsular, contractura','Resposta ao tratamento neoadjuvante — redução do tamanho, mudança de cinética','Lesões occultas na mamografia — lesões apenas visíveis em RM','Linfonodos axilares — avaliação de comprometimento metastático'],
    ['Bobina de mama dedicada (biomarray) em posição prona','Sequências: T2 SPAIR/STIR (avaliar edema, implantes), T1 pré-contraste','Contraste dinâmico: gadolínio 0,1 mmol/kg, séries multiphase (pré, pós 1min, 2min, 3min, 4min)','Subtração de imagens para evaluar realce','Avaliação de cinética de realce (Kaiser Score ou BI-RADS)','DWI (b=0,750) para caracterização adicional','Cortes: axial 2–3mm, coronal ou sagittal quando necessário','Incluir cadeia axilar e mamária interna se indicada'])

entries['coluna_lombar'] = me('coluna_lombar','RESSONÂNCIA MAGNÉTICA DE COLUNA LOMBAR',
    ['Não é necessário jejum','Tempo de exame: 20–35 minutos','Claustrofobia geralmente moderada para esta região','Confirmar ausência de marca-passo e avaliar função renal se contraste','Informar que será necessário ficar em decúbito dorsal, pode haver leve desconforto','Perguntar sobre próteses de quadril — artefactos metálicos podem prejudicar avaliação','Claustrofobia pode requerer RM aberta para pacientes muito ansiosos','Aplicar almofada sob os joelhos para conforto e redução da lordose'],
    ['Qual a indicação? (dor lombar, ciatalgia, estenose, avaliação pós-operatória?)','Dor com irradiação para membros inferiores? (padrão radicular L4, L5, S1)','Déficit motor, sensitivo ou alterações de esfíncter? (sinais de alarme)','Histórico de cirurgia de coluna prévia? (qual nível, qual procedimento?)','Febre, perda de peso ou dor noturna? (red flag para neoplasia/infecção)','Atividade física ou trauma precipitante?','Neoplasia conhecida em outra localização?'],
    ['Hérnia discal — protrusão/extrusão em L4–L5 e L5–S1, compressão radicular','Estenose do canal vertebral — central e/ou foráminal, degenerativa ou congênita','Espondilolistese — degenerativa ou ístmica, olisthesis vertebral, instabilidade','Modic changes — Tipo I (edema/inflamação), Tipo II (gordura), Tipo III (esclerose)','Cisto sinovial facetário — causa de estenose lateral e dor radicular','Fratura de estresse — edema vertebral, comum em osteoporose ou esportistas','Espondilodiscite / abscesso epidural — realce discal e de partes moles epidural','Neoplasia — metástases, mieloma múltiplo ("punched out"), hemangioma agressivo'],
    ['Bobina de coluna lombar ou body-array coil','Sequências: T1 sagital, T2 sagital (SPAIR), T2* GRE para discos degenerados, difusão (DWI) para fraturas e tumors','Contraste com gadolínio 0,1 mmol/kg para infecção, tumor, cisto sinovial e pós-operatório','Incluir de T11–L1 até o sacro; junção tóraco-lombar Included for T12 fratures','Cortes axiais (4mm) nos níveis de interesse (L3–L4, L4–L5, L5–S1)','Avaliar: discos, forames neurais, articulações facetárias, medula (até cone medular em L1–L2)'])

entries['coluna_cervical'] = me('coluna_cervical','RESSONÂNCIA MAGNÉTICA DE COLUNA CERVICAL',
    ['Não é necessário jejum','Tempo de exame: 25–40 minutos','Claustrofobia relevante — cabeça e pescoço dentro do imã','Confirmar ausência de marca-passo (contraindicação absoluta), stents coronarianos geralmente compatíveis','Avaliar função renal se contraste será usado (tumores, infecções)','Informar que será necessário ficar imóvel e que o pescoço pode ficar levemente estendido','Perguntar sobre trauma cervical recente — pode requerer RX antes para excluir fratura instável','Implantes metálicos cervicais (placas, parafusos) — avaliar artefactos'],
    ['Qual a indicação? (hérnia discal, mielopatia, tumor, infecção, trauma?)','Dor cervical com irradiação para membros superiores? (padrão radicular C5–T1)','Déficit motor ou sensitivo nos membros?','Disfunção de esfíncter vesical/anal? (sinal de alarme para mielopatia)','Febre ou suspeita de infecção (espondilodiscite)?','Neoplasia conhecida com risco de metástase?','Histórico de artrite reumatoide ou espondiloartrite (risco de subluxação)?'],
    ['Hérnia discal cervical — C5–C6, C6–C7 mais comuns, compressão radicular ou medular','Mielopatia compressiva — sinal intramedular em T2, espondilose com osteófitos posteriores','Espondilolistese degenerativa — avaliação de olisthesis e canal medular','Tumor intradural — meningioma, schwannoma, ependimoma (realce homogêneo vs. heterogêneo)','Metástases vertebrais — lesão expansiva com destruição óssea, compressão medular','Espondilodiscite — osteomielite, abscesso epidural, disco com hipersinal T2 e realce'],
    ['Bobina de crânio + neck-array coil','Sequências: T1 sagital, T2 sagital (SPIR/SPAIR), T2* GRE (avaliar calcificação discal), DWI para tumor/infecção','Contraste com gadolínio 0,1 mmol/kg para tumor, infecção, mielite','Incluir de C1 a T1, com cobertura de junção crânio-cervical','Cortes sagitais (3mm) e axiais (4mm) centrados nos discos e forames','Avaliar medula espinhal, raízes, discos, forames neurais e corpos vertebrais'])

entries['coluna_toracica'] = me('coluna_toracica','RESSONÂNCIA MAGNÉTICA DE COLUNA TORÁCICA',
    ['Não é necessário jejum','Tempo de exame: 30–45 minutos','Claustrofobia relevante — toda a região torácica dentro do imã','Confirmar ausência de marca-passo (avaliar tipo — MR-conditional podem existir)','Avaliar função renal se contraste será usado','Perguntar sobre implantes ortopédicos torácicos (instrumentação de Harrington, barras)','Informar que será necessário controle respiratório (apneias curtas)','Perguntar sobre prurido intenso nas costas (patologia a investigar)'],
    ['Qual a indicação? (deformidade, mielopatia, tumor, infecção, dor?)','Dor torácica ou dorsal com padrão radicular (dor em faixa)?','Déficit motor ou sensitivo nos membros inferiores?','Disfunção esfincteriana vesical/anal?','Febre persistente, sudorese noturna, perda de peso?','Neoplasia conhecida (mama, pulmão — risco de metástase vertebral)?','Escoliose ou deformidade torácica conhecida?'],
    ['Metástases vertebrais — compressão medular, destruição do corpo vertebral','Mieloma múltiplo — lesões "punched out", compressão patológica','Nódulos de Schmorl (hérnia intra-óssea) — comune, geralmente incidental','Hemangioma vertebral — tipicamente T1/T2 hiperintenso, incidental','Osteomielite / espondilodiscite — disco e vértebras com edema, realce, abscesso epidural','Deformidade (escoliose, cifose) — avaliação rotacional dos corpos vertebrais','Tumor intradural — meningioma (hiperintenso em T2), schwannoma, metástase leptomeníngea'],
    ['Bobina de superfície torácica ou body-array coil','Sequências: T1 sagital, T2 SPIR/STIR sagital, DWI para tumor/infecção','Contraste com gadolínio 0,1 mmol/kg para neoplasia e espondilodiscite','Gating respiratório ou apneias para minimizar artefatos','Incluir de C7 a L1, com cobertura completa da coluna torácica','Cortes sagitais 3mm, axiais 4mm perpendiculares ao eixo vertebral','Avaliar: medula espinhal torácica, discos, corpos vertebrais, costelas adjacentes'])

entries['crânio'] = me('crânio','RESSONÂNCIA MAGNÉTICA DE CRÂNIO',
    ['Não é necessário jejum para estudo sem contraste','Com contraste: jejum de 4 horas (prevenir náuseas/aspiração)','Avaliar função renal se gadolínio será usado (NSF)','Tempo de exame: 25–45 minutos','Claustrofobia — a cabeça fica totalmente dentro do imã','Confirmar ausência de marca-passo convencional (contraindicação absoluta)','Perguntar sobre implantes metálicos intracranianos (clipes de aneurisma, stents, bobina de estimulação)','Implantes cocleares — verificar compatibilidade com RM antes do exame'],
    ['Qual a indicação? (cefaleia, AVC, tumor, epilepsia, demência?)','Cefaleia de início recente, súbita ou com sinais neurológicos?','Déficits neurológicos focais (motor, sensitivo, linguagem)?','Crises convulsivas? Quando foram as últimas?','Perdas de consciência ou alterações de memória?','Histórico de neoplasia sistêmica com risco de metástase cerebral?','Doenças desmielinizantes conhecidas (esclerose múltipla)?'],
    ['Lesões expansivas intracranianas — glioma, meningioma, metástases, linfoma','Doenças desmielinizantes — placas de EM (periventricular, juxtacortical, infratentorial)','AVC isquêmico — avaliação de fase aguda (DWI), penumbra, core isquêmico','Hemorragia intracraniana — epidural, subdural, subaracnóidea, intraparenquimatosa','Malformações developmentais — Chiari, agenesia de corpo caloso, polimicrogiria','Hidrocefalia — dilatação ventricular, causa obstrutiva vs. comunicante'],
    ['Bobina de crânio phased-array','Sequências: FLAIR, DWI (b=0,1000), T1 spin-echo, T2 TSE, SWI (susceptibilidade)','Contraste: T1+MPRAGE pós-gadolínio 0,1 mmol/kg para lesões tumorais e inflamatórias','Avaliar fossa posterior e junção crânio-cervical para Chiari','Incluir órbitas e base do crânio na avaliação','Cortes axiais 5mm, coronais e sagitais quando indicado','SWI para micro-hemorragias, cavernoma, petéquias'])

# Now do replacements - use regex to find and replace each entry
for key, new_entry in entries.items():
    # Find the exam entry pattern: key: `...`
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
