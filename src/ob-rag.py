import requests
import anthropic

# --- Step 1: Query Fuseki ---
def query_fuseki(keyword):
    sparql_query = f"""
    PREFIX obo: <http://purl.obolibrary.org/obo/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?label ?definition
    WHERE {{
        ?class a owl:Class .
        ?class rdfs:label ?label .
        ?class obo:IAO_0000115 ?definition .
        FILTER(LANG(?label) = "en")
        FILTER(CONTAINS(LCASE(STR(?label)), "{keyword.lower()}"))
    }}
    LIMIT 5
    """
    response = requests.get(
        "http://localhost:3030/envo/query",
        params={"query": sparql_query},
        headers={"Accept": "application/sparql-results+json"}
    )
    results = response.json()
    bindings = results["results"]["bindings"]
    return [(b["label"]["value"], b["definition"]["value"]) for b in bindings]

def query_samples(biome_keyword):
    sparql_query = f"""
    SELECT ?sample ?name ?biome ?lat ?lon
    WHERE {{
        ?sample <http://www.w3.org/2000/01/rdf-schema#label> ?name .
        ?sample <http://example.org/property/biome> ?biome .
        OPTIONAL {{ ?sample <http://example.org/property/latitude> ?lat }}
        OPTIONAL {{ ?sample <http://example.org/property/longitude> ?lon }}
        FILTER(CONTAINS(LCASE(STR(?biome)), "{biome_keyword.lower()}"))
    }}
    LIMIT 5
    """
    response = requests.get(
        "http://localhost:3030/envo/query",
        params={"query": sparql_query},
        headers={"Accept": "application/sparql-results+json"}
    )
    results = response.json()
    bindings = results["results"]["bindings"]
    return [(
        b["name"]["value"],
        b["biome"]["value"],
        b.get("lat", {}).get("value", "unknown"),
        b.get("lon", {}).get("value", "unknown")
    ) for b in bindings]

# --- Step 2: Build grounding context ---
def build_context(ontology_results, sample_results):
    lines = []
    
    if ontology_results:
        lines.append("ONTOLOGY DEFINITIONS:")
        for label, definition in ontology_results:
            lines.append(f"- {label}: {definition}")
    
    if sample_results:
        lines.append("\nREAL WORLD SAMPLES:")
        for name, biome, lat, lon in sample_results:
            lines.append(f"- Sample '{name}' collected from {biome} at lat:{lat} lon:{lon}")
    
    if not lines:
        return "No relevant ontology terms or samples found."
    
    return "\n".join(lines)


# --- Step 3: Ask Claude ---
def ask_claude(user_question, context):
    client = anthropic.Anthropic()
    prompt = f"""You are an environmental science assistant. 
Use ONLY the following ontology definitions to answer the question.
If the answer isn't in the definitions, say so.

ONTOLOGY CONTEXT:
{context}

QUESTION: {user_question}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


# --- Main loop ---
def main():
    print("OB-RAG demo — type a question about environments (or 'quit' to exit)")
    while True:
        question = input("\nYour question: ")
        if question.lower() == "quit":
            break
        keyword = input("Keyword to search ontology (e.g. 'lake', 'marine', 'soil'): ")
        
        print("\nQuerying Fuseki...")
        ontology_results = query_fuseki(keyword)
        sample_results = query_samples(keyword)
        context = build_context(ontology_results, sample_results)
        
        print(f"\nContext retrieved:\n{context}")
        
        print("\nAsking Claude...")
        answer = ask_claude(question, context)
        print(f"\nClaude's answer:\n{answer}")

main()