import requests

# --- Step 1: Pull samples from MGnify API ---
def get_samples(page_size=25):
    url = "https://www.ebi.ac.uk/metagenomics/api/v1/samples"
    params = {"page_size": page_size, "format": "json"}
    response = requests.get(url, params=params)
    data = response.json()
    return data["data"]

# --- Step 2: Convert samples to RDF triples (Turtle format) ---
def samples_to_triples(samples):
    triples = []
    
    for sample in samples:
        attrs = sample.get("attributes", {})
        relationships = sample.get("relationships", {})
        sample_id = sample.get("id", "unknown")
        
        name = attrs.get("sample-name", "").replace('"', "'")
        desc = attrs.get("sample-desc", "").replace('"', "'")
        lat = attrs.get("latitude")
        lon = attrs.get("longitude")
        
        # Get biome from relationships
        biome_data = relationships.get("biome", {}).get("data", {})
        biome = biome_data.get("id", "") if biome_data else ""
        
        if not biome:
            continue

        safe_id = sample_id.replace("-", "_")
        subj = f"<https://www.ebi.ac.uk/metagenomics/samples/{safe_id}>"
        triples.append(f'{subj} <http://www.w3.org/2000/01/rdf-schema#label> "{name}" .')
        triples.append(f'{subj} <http://example.org/property/biome> "{biome}" .')
        if desc:
            triples.append(f'{subj} <http://example.org/property/description> "{desc}" .')
        if lat:
            triples.append(f'{subj} <http://example.org/property/latitude> "{lat}" .')
        if lon:
            triples.append(f'{subj} <http://example.org/property/longitude> "{lon}" .')

    return "\n".join(triples)


def load_into_fuseki(triples):
    url = "http://localhost:3030/envo/update"
    sparql_update = f"INSERT DATA {{ {triples} }}"
    response = requests.post(
        url,
        data={"update": sparql_update},
    )
    if response.status_code in (200, 201, 204):
        print("Successfully loaded into Fuseki!")
    else:
        print(f"Error loading into Fuseki: {response.status_code}")
        print(response.text)

# --- Main ---
def main():
    print("Fetching samples from MGnify...")
    samples = get_samples(25)
    print(f"Got {len(samples)} samples")

    import json
    print(json.dumps(samples[0], indent=2))
    
    print("Converting to RDF...")
    triples = samples_to_triples(samples)
    
    with open("samples.ttl", "w", encoding="utf-8") as f:
        f.write(triples)
    print("Saved to samples.ttl so you can inspect it")
    
    print("Loading into Fuseki...")
    load_into_fuseki(triples)


main()