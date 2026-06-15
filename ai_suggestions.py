import ollama

def get_ai_suggestions(df):
    summary = f"""
    Rows: {df.shape[0]}
    Columns: {df.shape[1]}

    Missing Values:
    {df.isnull().sum()}

    Duplicate Rows:
    {df.duplicated().sum()}

    Data Types:
    {df.dtypes}
    """

    prompt = f"""
You are a data cleaning assistant.

Your job is to suggest DATA CLEANING ACTIONS only.

STRICT RULES:
- Do NOT repeat dataset summary
- Do NOT list column names again
- Do NOT show data types again
- Only give cleaning actions
- Use bullet points
- Keep answers short

Example Output:

Missing Values:
- Fill missing order_date with mean
- Fill missing City with mode

Duplicates:
- Remove duplicate rows

Column Names:
- Convert column names to lowercase
- Replace spaces with underscore

Data Types:
- Ensure order_id is numeric
- Ensure Total_amount, price and quantity are integers

Outliers:
- Check Total_amount column for outliers

Now analyze this dataset summary and give cleaning actions only:

{summary}
"""

    response = ollama.chat(
        model='gemma3:1b',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response['message']['content']
