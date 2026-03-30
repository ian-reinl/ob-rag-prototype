# OB-RAG: Ontology-Based Retrieval-Augmented Generation
### Project Summary

---

## The Problem

Large language models (LLMs) hallucinate. They generate plausible-sounding but factually incorrect outputs, particularly in specialized domains where precise terminology and formal relationships matter. Retrieval-augmented generation (RAG) partially addresses this by supplying relevant documents as context at inference time, but standard RAG retrieval is lexical: it matches keywords, not meaning. A query about biomes may retrieve documents that mention the right words but miss semantically related concepts that a domain expert would recognize as relevant.

This is a structural limitation. Lexical retrieval is blind to the formal relationships encoded in domain ontologies, including subsumption hierarchies, class definitions, and instance-level assertions that represent the actual knowledge structure of a field.

---

## The Approach

This project implements an ontology-based retrieval-augmented generation (OB-RAG) system for the biome domain. Instead of retrieving document chunks, the system queries a SPARQL endpoint backed by the Environment Ontology (ENVO) and instance data from the MGnify metagenomics database. Retrieved triples are formally structured, semantically grounded facts that get passed as context to a large language model, which generates an answer constrained by the ontology's structure.

The core insight is that ontology-grounded retrieval raises the semantic ceiling of RAG. By exploiting class hierarchies and formal definitions at retrieval time, the system can surface relevant knowledge that keyword search would miss.

---

## The System

The pipeline has four stages:

1. The user submits a natural language query
2. The query is translated into a SPARQL query that exploits ENVO's class hierarchy
3. Apache Jena Fuseki retrieves relevant triples from the ontology and instance data
4. Retrieved triples are passed as structured context to the Anthropic Claude API, which generates a grounded natural language answer

The system is implemented in Python using SPARQLWrapper, the requests library, and the Anthropic SDK.

---

## The Research Contribution

This prototype is the foundation for an academic paper examining the theoretical limits of OB-RAG as a hallucination mitigation strategy. The central argument is that while grounding retrieval in a formal ontology meaningfully reduces hallucination, it cannot eliminate it. The LLM's inference step remains formally unconstrained: even with perfectly grounded context, the model must interpret, summarize, and express retrieved triples in natural language, and that process introduces opportunities for error.

The paper draws on formal hallucination theorems from Xu et al., empirical RAG benchmarks from Zhao et al. (MedRAG), and knowledge graph-based RAG work from Gao et al. (DR.KNOWS) to support this argument.

---

## Skills Demonstrated

- Formal ontology engineering (OBO Foundry, ENVO, BFO)
- SPARQL query design and triple store management (Apache Jena Fuseki)
- RDF data modeling and Turtle serialization
- API integration (MGnify, Anthropic)
- Python development for knowledge graph applications
- Applied research in ontology-based AI systems

---

## About

Developed by Ian Reinl as part of the MS in Applied Ontology program at the University at Buffalo. Research interests include formal ontology, knowledge representation, and the intersection of OWL/description logics with applied AI systems.

GitHub: https://github.com/ian-reinl/ob-rag-prototype
