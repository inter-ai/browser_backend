# app/knowledge_graph.py

import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from app.config import AGENT_ONTOLOGY_FILE, ENV_ONTOLOGY_FILE

class KnowledgeGraphManager:
    def __init__(self):
        # 1) Agent Graph (STATIC)
        self.agent_graph = Graph()
        self.agent_graph.parse(AGENT_ONTOLOGY_FILE, format="turtle")

        # 2) Environment Graph (DYNAMIC)
        self.env_graph = Graph()
        self.env_graph.parse(ENV_ONTOLOGY_FILE, format="turtle")

        self.AG = Namespace("http://example.org/emergency#")
        self.WF = Namespace("http://example.org/wildfire#")

    ################################################
    # Agent KG
    ################################################

    def search_agent_knowledge(self, agent_name: str) -> str:
        """
        SPARQL search for the given agent name in the Agent Graph.
        e.g. agent_name = "FireAgent"
        Returns a Turtle snippet with that agent's data.
        """
        # Build a SPARQL query
        query_str = f"""
        PREFIX er: <http://example.org/emergency#>
        SELECT ?p ?o
        WHERE {{
            er:{agent_name} ?p ?o .
        }}
        """
        results = self.agent_graph.query(query_str)

        # Build a temporary Graph of just this agent's info
        temp_g = rdflib.Graph()
        agent_uri = URIRef(f"http://example.org/emergency#{agent_name}")
        for row in results:
            temp_g.add((agent_uri, row.p, row.o))

        # Return as Turtle
        if len(temp_g) == 0:
            return ""  # no results
        return temp_g.serialize(format="turtle")

    def dump_agent_kg(self) -> str:
        """
        Entire Agent KG in Turtle.
        """
        return self.agent_graph.serialize(format="turtle")

    ################################################
    # Environment KG
    ################################################

    def dump_environment_kg(self) -> str:
        """
        Entire Env KG in Turtle.
        """
        return self.agent_graph.serialize(format="turtle")

    def update_environment_with_drone(self, data: dict):
        """
        data = {
          "location": "RedwoodForest",
          "severity": "HighSeverity",
          "fireSpreadRate": 7.5,
          "airQuality": 200,
          "visibleFlames": 10.0
        }
        """
        loc = data["location"]
        severity = data["severity"]

        event_uri = self.WF[f"Fire_{loc}"]
        # Mark it as a Wildfire
        self.env_graph.add((event_uri, RDF.type, self.WF["Wildfire"]))

        # e.g. "HighSeverity", "ModerateSeverity"
        sev_uri = self.WF[severity]
        self.env_graph.add((event_uri, self.WF["hasSeverity"], sev_uri))

        # Numeric data
        if "fireSpreadRate" in data:
            self.env_graph.add((event_uri, self.WF["fireSpreadRate"], 
                                Literal(data["fireSpreadRate"], datatype=XSD.float)))
        if "airQuality" in data:
            self.env_graph.add((event_uri, self.WF["airQuality"], 
                                Literal(data["airQuality"], datatype=XSD.integer)))
        if "visibleFlames" in data:
            self.env_graph.add((event_uri, self.WF["visibleFlames"], 
                                Literal(data["visibleFlames"], datatype=XSD.float)))
