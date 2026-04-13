# Medscaner_prep v2.0

**Sistema de Gestão de Preparo para Exames de Imagem**

---

## 📋 Descrição

Landing page interativa para triagem e preparo de exames de Ressonância Magnética e Tomografia Computadorizada. Desenvolvido para centros de diagnóstico por imagem, permite que a equipe de enfermagem colete informações essenciais do paciente antes do exame.

---

## 🏥 Funcionalidades

### Seleção de Tipo de Exame
- **Ressonância Magnética**: 29 modalidades disponíveis
- **Tomografia Computadorizada**: 4 modalidades disponíveis

###每 exame contém 4 seções padronizadas:
1. **Informações para Agendamento** — perguntas de segurança para o momento do agendamento
2. **Perguntas para Anamnese** — levantamento do histórico clínico do paciente
3. **Triagem de Patologias** — identificação de condições que podem afectar o exame
4. **Recomendações ao Técnico** — orientações técnicas e de protocolo

### Recursos
- Interface responsiva e intuitiva
- Editor de texto integrado para customization
- Dados salvos em localStorage (persistem após fechar o navegador)
- Visualização em tempo real do conteúdo

---

## 📂 Estrutura do Projeto

```
Medscaner_prep/
├── index.html          # Landing page completa
├── server.js            # Servidor Node.js (porta 5007)
├── package.json        # Configuração do projeto Node
├── start.sh            # Script de inicialização
├── restart.sh          # Script de reinicialização
├── logo-medscaner.png  # Logotipo do projeto
└── README.md           # Este arquivo
```

---

## 🚀 Como Usar

### Instalação

```bash
npm install
```

### Iniciar o Servidor

```bash
node server.js
```

A aplicação estará disponível em: **http://localhost:5007**

### Scripts Disponíveis

- `start.sh` — inicia o servidor em background
- `restart.sh` — reinicia o servidor

---

## 📊 Quantidade de Exames

### Ressonância Magnética (29)
Abdome, AngioRM Arterial de Crânio, AngioRM Venosa de Crânio, Arcos Costais, Articulação Temporo-mandibular, Bacia, Braço, ColangioRM, Coluna Cervical, Coluna Lombar, Coluna Sacro-coccígea, Coluna Torácica, Cotovelo, Coxa, Crânio, EnteroRM, Joelho, Mamas, Mão, Órbitas, Ombro, Ossos Temporais, Pé, Pescoço, Punho, Quadril, Região Escapular, Sela Turcica, Tornozelo

### Tomografia (4)
Próstata, Sacro-ilíaca, Pelve Rotina, RM Cardíaca

---

## 🛠️ Tecnologias

- HTML5, CSS3, JavaScript (Vanilla)
- Node.js (servidor local)
- localStorage API (persistência)
- Google Fonts (tipografia)

---

## 👨‍💻 Autor

Desenvolvido por **Rafael Laguardia** / **Delphus**

---

## 📝 Licença

MIT License