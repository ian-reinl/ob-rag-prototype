Ontology-Based Retrieval-Augmented Generation (OB-RAG)
A working prototype of an ontology-grounded retrieval-augmented generation system for marine microbiome and environmental science queries. Built as part of graduate research in Applied Ontology at the University at Buffalo.

Overview
Standard retrieval-augmented generation (RAG) systems reduce large language model (LLM) hallucination by retrieving relevant documents and passing them as context at inference time. However, lexical retrieval ignores the semantic structure of a domain. It cannot exploit class hierarchies, subsumption relationships, or formal definitions.
This prototype addresses that limitation by grounding retrieval in a formal ontology. Instead of retrieving text chunks, the system queries a SPARQL endpoint backed by the Environment Ontology (ENVO) and instance data from the MGnify marine microbiome database. Retrieved triples, which are structured, semantically grounded facts, are passed as context to a large language model, which generates an answer constrained by the ontology's formal structure.
The system is the basis for ongoing research arguing that OB-RAG reduces but cannot eliminate LLM hallucination, drawing on formal hallucination theorems and empirical benchmarks from the biomedical RAG literature.

Architecture
```
User query (natural language)
        │
        ▼
SPARQL query construction
        │
        ▼
Apache Jena Fuseki (triple store)
  └── ENVO (Environment Ontology)
  └── MGnify instance data (marine microbiome samples)
        │
        ▼
Retrieved triples (structured ontology context)
        │
        ▼
Anthropic Claude API (LLM generation)
        │
        ▼
Grounded natural language answer
```

| Component | Technology |
|---|---|
| Triple store | Apache Jena Fuseki |
| Domain ontology | ENVO (Environment Ontology) |
| Instance data | MGnify API (marine microbiome) |
| Query language | SPARQL 1.1 |
| LLM | Anthropic Claude (via API) |
| Language | Python 3 |
| Key libraries | `SPARQLWrapper`, `requests`, `anthropic` |

Repository Structure
```
ob-rag-prototype/
├── README.md
├── src/
│   └── (pipeline scripts)
├── sparql/
│   └── (SPARQL query templates)
├── data/
│   └── (sample ontology fragments and instance data)
└── docs/
    └── (architecture notes and research context)
```

Setup
Prerequisites

Python 3.9+
Apache Jena Fuseki (download at jena.apache.org)
An Anthropic API key
ENVO ontology file (available at obofoundry.org)

Installation
bashgit clone https://github.com/ianre-reinl/ob-rag-prototype.git
cd ob-rag-prototype
pip install -r requirements.txt
Running Fuseki
bash# Start Fuseki with an in-memory dataset
fuseki-server --mem /ds

# Or with a persistent dataset
fuseki-server --update --loc=./data/fuseki /ds
Environment Variables
Create a .env file in the root directory:
ANTHROPIC_API_KEY=your_api_key_here
FUSEKI_ENDPOINT=http://localhost:3030/ds/sparql

Research Context
This prototype supports a research paper examining the theoretical limits of ontology-based retrieval-augmented generation as a hallucination mitigation strategy. The paper draws on:

- **Gao et al.** — DR.KNOWS: knowledge graph-based RAG for clinical decision support
- **Zhao et al.** — MedRAG: retrieval-augmented generation benchmarks in the biomedical domain
- **Xu et al.** — formal theorems establishing the conditions under which RAG systems can and cannot eliminate hallucination

The central argument is that while grounding retrieval in a formal ontology raises the semantic ceiling of RAG, enabling subsumption-aware retrieval and structured context, it cannot guarantee hallucination-free generation because the LLM's inference step remains formally unconstrained.

About
Developed by Ian Reinl as part of the MS in Applied Ontology program at the University at Buffalo. Research interests include formal ontology, knowledge representation, and the intersection of OWL/description logics with applied AI systems.

License
MIT License — see LICENSE for details.