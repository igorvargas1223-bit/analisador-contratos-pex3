import streamlit as st
import re
from pypdf import PdfReader

st.set_page_config(page_title="Tradutor Jurídico e LGPD", page_icon="📄", layout="centered")

st.title("📄 Leitor Inteligente de Contratos e Termos (LGPD)")
st.markdown("Envie um **contrato em PDF** ou cole o texto abaixo para identificar cláusulas importantes de **Direitos Trabalhistas** e **Proteção de Dados (LGPD)** em linguagem simples.")

aba1, aba2 = st.tabs(["📂 Enviar Arquivo PDF", "✍️ Colar Texto do Contrato"])

texto_contrato = ""

with aba1:
    arquivo_pdf = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])
    if arquivo_pdf is not None:
        try:
            leitor = PdfReader(arquivo_pdf)
            paginas_texto = [pagina.extract_text() or "" for pagina in leitor.pages]
            texto_contrato = "\n".join(paginas_texto)
            st.success(f"PDF lido com sucesso! ({len(leitor.pages)} página(s) extraída(s)).")
        except Exception as e:
            st.error("Não foi possível ler este PDF. Tente colar o texto na aba ao lado.")

with aba2:
    texto_colado = st.text_area(
        "Cole aqui o trecho do contrato ou termo de consentimento:",
        height=180,
        placeholder="Ex: O CONTRATADO autoriza o compartilhamento de seus dados pessoais e biométricos com terceiros parceiros, bem como renuncia ao pagamento de horas extras..."
    )
    if texto_colado.strip():
        texto_contrato = texto_colado

def analisar_contrato(texto):
    texto_lower = texto.lower()
    achados_lgpd =
    achados_trabalho =
    dicionario_encontrado =

    # 1. Regras de LGPD (Lei 13.709/2018)
    regras_lgpd = [
        (r"compartilhamento|terceiros|parceiros comerciais", "🔄 **Compartilhamento com Terceiros:** O texto menciona repassar seus dados para outras empresas. Verifique se há opção de recusar."),
        (r"biom[ée]tric|digital|facial|sa[úu]de|religi[ãa]o|ra[çc]a", "🧬 **Dados Pessoais Sensíveis:** Envolve dados protegidos com rigor máximo pela LGPD (biometria, saúde, etc.). Exige consentimento específico."),
        (r"irrevog[áa]vel|irretrat[áa]vel", "⚠️ **Cláusula de Irrevogabilidade:** Pela LGPD (Art. 8º, § 5º), você tem o direito de revogar seu consentimento a qualquer momento."),
        (r"encarregado|dpo|controlador|titular", "🛡️ **Conformidade LGPD Identificada:** O documento cita papéis oficiais da Lei Geral de Proteção de Dados.")
    ]

    for padrao, explicacao in regras_lgpd:
        if re.search(padrao, texto_lower):
            achados_lgpd.append(explicacao)

    # 2. Regras Trabalhistas e Contratuais
    regras_trabalho = [
        (r"hora[s]? extra[s]?|banco de horas|compensa[çc][ãa]o de jornada", "⏰ **Jornada e Horas Extras:** Atenção às regras de compensação de horário e pagamento de horas extras."),
        (r"multa|penalidade|rescis[ãa]o|aviso pr[ée]vio", "💸 **Multa e Rescisão:** Existem regras financeiras caso uma das partes quebre ou encerre o contrato antes do prazo."),
        (r"exclusividade|n[ãa]o concorr[êe]ncia|sigilo|confidencialidade", "🔒 **Exclusividade ou Sigilo:** Pode impedir você de prestar serviços para outras empresas ou divulgar informações internas."),
        (r"ren[úu]ncia|abre m[ãa]o", "🚨 **Alerta de Renúncia de Direitos:** Cuidado! Direitos trabalhistas básicos (como férias e FGTS) não podem ser anulados por contrato.")
    ]

    for padrao, explicacao in regras_trabalho:
        if re.search(padrao, texto_lower):
            achados_trabalho.append(explicacao)

    # 3. Tradutor de Termos Jurídicos ("Juridiquês" -> Linguagem Simples)
    termos_juridicos = {
        "foro de eleição": "Define em qual cidade/tribunal será resolvido qualquer processo judicial sobre este contrato.",
        "ônus": "Obrigação, dever ou responsabilidade que fica por conta de uma das partes.",
        "solidariamente": "Quando duas ou mais pessoas/empresas respondem juntas pela mesma dívida ou obrigação.",
        "anuidade": "Concordância, aprovação ou autorização formal.",
        "anuência": "Concordância, aprovação ou autorização formal.",
        "resilição": "Cancelamento do contrato por vontade de uma ou ambas as partes.",
        "inadimplemento": "Falta de pagamento ou descumprimento de alguma obrigação combinada."
    }

    for termo, traducao in termos_juridicos.items():
        if termo in texto_lower:
            dicionario_encontrado.append(f"**{termo.capitalize()}:** {traducao}")

    return achados_lgpd, achados_trabalho, dicionario_encontrado

if st.button("Analisar Documento", type="primary"):
    if not texto_contrato.strip():
        st.warning("Por favor, envie um PDF ou cole um texto antes de clicar em analisar.")
    else:
        lgpd, trabalho, glossario = analisar_contrato(texto_contrato)
        palavras = len(texto_contrato.split())

        st.markdown("---")
        st.subheader("📊 Resumo da Análise Computacional")
        col1, col2, col3 = st.columns(3)
        col1.metric("Palavras Analisadas", palavras)
        col2.metric("Alertas LGPD", len(lgpd))
        col3.metric("Pontos Trabalhistas", len(trabalho))

        st.markdown("### 🛡️ Proteção de Dados (LGPD)")
        if lgpd:
            for item in lgpd:
                st.info(item)
        else:
            st.write("Nenhuma cláusula crítica de LGPD detectada neste trecho.")

        st.markdown("### ⚖️ Direitos Trabalhistas e Obrigações")
        if trabalho:
            for item in trabalho:
                st.warning(item)
        else:
            st.write("Nenhuma cláusula trabalhista crítica detectada neste trecho.")

        if glossario:
            st.markdown("### 📖 Tradutor de Termos Jurídicos")
            for termo in glossario:
                st.markdown(f"- {termo}")

st.markdown("---")
st.caption("Projeto de Extensão (PEX III) - Ciência da Computação | Ferramenta gratuita de educação digital e leitura contratual para a comunidade.")
