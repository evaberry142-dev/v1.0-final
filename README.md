# v1.0-final
Web datamining project Eva BERRY and Charles AYOUB TD DIA1

## How to run the project ?

The full implementation is available in the section: 'notebook/Project_final_Eva_BERRY_Charles_Ayoub_DIA1/`. Indeed, in this folder, you have the notebook nammed "project_final_Eva_BERRY_Charles_Ayoub_DIA1.ipynb" as well as the outputs of the notebook and all the generated files of the notebook. Moroever, this folder also contains a copy of the chatbot implementation in the python file "chatbot_rag.py".

Step 1 : check that the Ollama application is available and open on your laptop (you must have the version "gemma:2b").

Step 2 : open the notebook and run all the cells. (The run of all the project take a lot of time). Therefore, all the outputs recquired for the LLM fonctionning are already generated and you can find them in the GitHub repisitory. 
(Note that : All the files that the notebook generates are already available, so that you don't need to run all the notebook).

Step 3 : Go to the chatbpt_rag.py file (available in the folder of the full implementation as well as in the folder RAG_Chatbot) and open a terminal and launch the command "python chatbot_rag.py". Note that the final RDF Graph "knowledge_base_filtered.nt" must be in the same folder.

Step 4 : You can now ask whatever you want to the LLM.

## Content of the notebook 
(Every part is explained and commented in the notebook)

The project is structured into seven phases:

**Phase 1 : Web Crawling and Cleaning**  
   Collecting web data and extracting of the data.

**Phase 2 : Information Extraction**  
   Identifying entities and relations from the collected data.

**Phase 3 : Build the Initial Private Knowledge Base**  
   Build of the initial RDF knowledge graph.

**Phase 4 : Entity Linking with Open knowledge Base**  
   Alignement of the extracted entities with Wikidata.

**Phase 5 : Predicate Alignment Using SPARQL**  
   Mapping and Predicate alignement to Wikidata.

**Phase 6 : Knowledge Base Expansion via SPARQ**  
   Enriching the graph using one-hop and two-hop expansion.

**Phase 7 : Knoswledge reasoning with SWRL**  
   Applying logical rules to infer new knowledge.

**Phase 8 : Knowledge Graph Embedding**  
   Embedding preprocessing and models, Size-sensitivity, Nearest neighbors and t-SNE.

**Phase 9: Retrieval-Augmented Generation (RAG) with RDF/SPARQL and a Local Small LLM**  
   Querying the knowledge graph using SPARQL an local LLM Ollama.
