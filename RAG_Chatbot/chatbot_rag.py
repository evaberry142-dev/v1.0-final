import rdflib
import requests
import re

# 1) CONFIGURATION 
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma:2b"
FILE_PATH = "knowledge_base_filtered.nt"

def ask_local_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return response.json().get('response', '').strip()
    except Exception as e:
        return f"Error: {e}"

# 2) SCHEMA SUMMARY 
def get_schema_summary(g):
    predicates = sorted(set(str(p) for s, p, o in g))
    summary = "AVAILABLE PREDICATES IN THE GRAPH:\n"
    for p in predicates:
        summary += f"- <{p}>\n"
    return summary

# 3) SPARQL GENERATION 
def generate_sparql(question, schema, error_message=None):
    prompt = f"""You are a SPARQL expert. Use this schema summary:
    {schema}
    
    EXAMPLES:
    Question: "Show me Beirut"
    Query: SELECT ?s ?p ?o WHERE {{ ?s ?p ?o . FILTER(CONTAINS(LCASE(STR(?s)), "beirut") || CONTAINS(LCASE(STR(?o)), "beirut")) }}
    
    Question: "Information about Museum"
    Query: SELECT ?s ?p ?o WHERE {{ ?s ?p ?o . FILTER(CONTAINS(LCASE(STR(?s)), "museum") || CONTAINS(LCASE(STR(?o)), "museum")) }}

    RULES:
    - DO NOT use 'wdt:' or 'wd:' prefixes.
    - Use full URIs in < > or use variables ?s ?p ?o.
    - Output ONLY the SPARQL code.
    """
    
    if error_message:
        prompt += f"\nYOUR PREVIOUS ATTEMPT FAILED WITH ERROR: {error_message}. PLEASE FIX IT."

    ai_response = ask_local_llm(f"{prompt}\nQuestion: {question}\nQuery:")
    match = re.search(r"SELECT.*?\}", ai_response, re.DOTALL | re.IGNORECASE)
    return match.group(0) if match else ai_response

# 4) EXECUTION / REPAIR LOOP 
def execute_with_repair(g, question, schema):
    query = generate_sparql(question, schema)
    for attempt in range(3):
        query = re.sub(r"wdt:\w+", "?p", query)
        query = re.sub(r"wd:\w+", "?o", query)
        
        print(f"\n[Attempt {attempt+1}] Executing:\n{query}")
        try:
            return g.query(query), query, None
        except Exception as e:
            err_msg = str(e)
            print(f"Error: {err_msg}")
            query = generate_sparql(question, schema, error_message=err_msg)
    return None, query, "Failed to generate a valid query"

# 5) ANSWER GENERATION WITH RAG
def answer_with_rag(question, results):
    if not results or len(results) == 0:
        return "No data found in the knowledge graph for this query."
    
    facts = []
    for row in list(results)[:15]:
        subject_label = str(row[0]).split('/')[-1].replace('_', ' ')
        predicate_label = str(row[1]).split('/')[-1].split('#')[-1]
        object_value = str(row[2])
        facts.append(f"Entity: {subject_label} | Property: {predicate_label} | Value: {object_value}")

    context = "\n".join(facts)
    prompt = f"""You are a data reporting assistant. Answer based ONLY on the following RDF triples.
    
    RDF DATA:
    {context}
    
    USER QUESTION: {question}
    
    INSTRUCTIONS:
    - List the information found.
    - Include the corresponding Wikidata link (URL) for each fact.
    - Do not use your own internal knowledge.
    ANSWER:"""
    return ask_local_llm(prompt)

# 6) BASELINE ANSWER 
def answer_no_rag(question):
    """Direct answer from LLM without looking at the RDF graph."""
    prompt = f"Answer the following question as best as you can using your general knowledge: {question}"
    return ask_local_llm(prompt)

# MAIN LOOP 
if __name__ == "__main__":
    g = rdflib.Graph()
    print(f"Loading {FILE_PATH}...")
    g.parse(FILE_PATH, format="nt")
    print(f"Loaded {len(g)} triples.")
    
    schema_info = get_schema_summary(g)
    
    while True:
        user_input = input("\nYour question (or 'exit'): ").strip()
        if user_input.lower() in ['exit', 'quit']: break
        
        print("\n--- BASELINE (LLM only, no KG) ---")
        baseline = answer_no_rag(user_input)
        print(baseline)

        print("\n--- RAG (With your Knowledge Graph) ---")
        print("Processing SPARQL...")
        results, last_query, error = execute_with_repair(g, user_input, schema_info)
        
        if error:
            print(f"{error}")
        else:
            print("\nFinal Answer (Grounded):")
            print(answer_with_rag(user_input, results))