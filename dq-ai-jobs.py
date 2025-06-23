import pandas as pd
from pyspark.sql import SparkSession
from pydeequ.checks import Check, CheckLevel
from pydeequ.verification import VerificationSuite
from pydeequ.analyzers import DataTypeInstances

# pré-processamento com pandas
url = "https://raw.githubusercontent.com/thainazanfolin/data-qualit-pydeequ/refs/heads/main/ai_job_dataset.csv"

# lê o dataset da URL
df = pd.read_csv(url)

# análise rápida do shape do dataset
print("Shape:", df.shape)
print(df.head())

#Análise inicial do dataset: como não conhecemos os dados, precisamos conhecê-los antes de criar regras de qualidade

print("Shape:", df.shape)
print("\nTipos de Colunas:\n", df.dtypes)
print("\nValores Ausentes por Coluna:\n", df.isna().sum())
print("\nEstatísticas Numéricas:\n", df.select_dtypes(include="number").describe())
print("\nTop 5 Valores Categóricos por Coluna:")
for col in df.select_dtypes(include="object").columns:
    print(f"{col}:\n{df[col].value_counts().head()}\n")

#Pré-processamento (tratamento inicial dos dados)
#Remover linhas sem job_id, salary_in_usd, posting_date 
df_clean = df.dropna(subset=["job_id", "salary_in_usd", "posting_date"])

#Converter posting_date para datetime e descartar erros
df_clean["posting_date"] = pd.to_datetime(pdf_clean["posting_date"], errors="coerce")
df_clean = df_clean.dropna(subset=["posting_date"])

# 3.3 Normalizar employment_type
df_clean["employment_type"] = df_clean["employment_type"].str.strip().str.title()

# 3.4 Exibir mudanças
print("\nApós pré-processamento:")
print("Shape:", df_clean.shape)
print("Valores Ausentes:\n", df_clean.isna().sum())

### Pydeequ
#criando sessão spark
spark = (SparkSession.builder
    .appName("AI Job Quality")
    .config("spark.jars.packages", "com.amazon.deequ:deequ:2.0.1-spark-3.1")
    .getOrCreate())

#Convertendo o dataframe para Spark
df = spark.createDataFrame(df)
df.printSchema()
df.show(5, truncate=False)

#### Começando as regras de data-quality

check = (Check(spark, CheckLevel.Error, "AI Job Data Quality")
    #Completude e unicidade de job_id (job_id não pode faltar e cada job_id deve ser único)
    .isComplete("job_id")
    .isUnique("job_id")

    # Completude de salário e faixa válida
    .isComplete("salary_usd")                           
    .hasMin("salary_usd", lambda x: x >= 10000)         
    .hasMax("salary_usd", lambda x: x <= 500000)        
    .isNonNegative("salary_usd")                        
    .hasDataType("salary_usd", DataTypeInstances.Fractional)

    #Domínios de emprego e modalidade remota
    .isContainedIn("employment_type",                  #apenas categorias previstas
        ["Full-Time", "Part-Time", "Contract", "Temporary"])
    .isContainedIn("remote_ratio",               
        [0, 50, 100])

    # 3.4 Completude e validade de data de postagem
    .isComplete("posting_date")                         
    .hasPattern("posting_date", r"^\d{4}-\d{2}-\d{2}$") 

    # 3.5 Tipo de dado correto em job_id e job_title
    .hasDataType("job_id", DataTypeInstances.String)    
    .hasPattern("job_title", r"^[A-Za-z0-9 ,.&-]+$")     
)


# executando os testes
result = (VerificationSuite(spark)
    .onData(df)
    .addCheck(check)
    .run()
)

result_df = VerificationSuite.checkResultsAsDataFrame(spark, result)
result_df.show(truncate=False)

#stop da sessão
#spark.stop()
