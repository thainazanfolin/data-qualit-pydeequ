# Data Quality com PyDeequ

Este repositório acompanha o artigo sobre Pydeequ escrito para a disciplina de Qualidade de Software da FATEC Araras. O artigo apresenta:

- Conceitos e dimensões de **data quality**  
- Ferramentas Deequ (Scala/Spark) e PyDeequ (Python + Spark)  
- Estudo de caso prático com pré-processamento em pandas e verificações declarativas em Spark  

---

## 🚀 Projeto Prático

O projeto prático combina pré-processamento em pandas com validação de qualidade em Spark, utilizando PyDeequ. <br><br>Após carregar e limpar dados de vagas de IA (remoção de valores ausentes, conversão de datas e padronização de categorias) em pandas, o DataFrame foi convertido para Spark. Em Spark, aplicaram-se regras de **data quality** — como unicidade de `job_id`, completude de campos críticos, verificação de intervalos de salário, conformidade de domínios categóricos e padrões de formato de data — usando PyDeequ. <br><br>O resultado é um relatório que indica, para cada regra, se foi atendida ou quantos registros violaram a constraint, permitindo identificar rapidamente os pontos que precisam de correção antes de prosseguir com análises ou modelos downstream.
