from typing import List

class WildfireReasoner:
    """
    A naive reasoning engine that checks if there's a HighSeverity Wildfire 
    and then suggests actions.
    """
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph

    def recommend_actions(self, event_id: str) -> List[str]:
        """
        For demonstration: If the event is a HighSeverity wildfire, 
        recommend urgent actions; if moderate, recommend different actions, etc.
        We'll do a SPARQL query to find the severity of the event.
        """
        query_str = f"""
        PREFIX wf: <http://example.org/wildfire#>
        SELECT ?sev WHERE {{
            wf:{event_id} wf:hasSeverity ?sev .
        }}
        """
        results = self.kg.query_sparql(query_str)
        severity_uri = None
        for row in results:
            severity_uri = str(row[0])  # e.g. http://example.org/wildfire#HighSeverity

        if severity_uri and "HighSeverity" in severity_uri:
            return [
                "Dispatch aerial firefighting units immediately.",
                "Evacuate surrounding areas within a 5-mile radius.",
                "Notify local authorities and emergency responders."
            ]
        elif severity_uri and "ModerateSeverity" in severity_uri:
            return [
                "Monitor fire spread and prepare evacuation if needed.",
                "Deploy ground-based fire crews.",
                "Coordinate with local park rangers."
            ]
        elif severity_uri and "LowSeverity" in severity_uri:
            return [
                "Contain the fire with minimal resources.",
                "Maintain surveillance for any escalation."
            ]
        else:
            # If severity wasn't found or event not recognized
            return ["No specific actions found. Possibly unclassified severity?"]
