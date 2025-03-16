# Check Root
```
curl http://127.0.0.1:8000
```


# Get Agent KG (Static)

```
curl http://127.0.0.1:8000/agent/kg/dump
```

#Search for an agent (e.g., FireAgent):

```
curl -X POST http://127.0.0.1:8000/agent/kg/search \
     -H "Content-Type: application/json" \
     -d '{"agent_name":"FireAgent"}'
```
If you try RescueAgent, MedicalAgent, or DroneCoordinator you get their RDF snippet.

# Environment KG (Dynamic)
Dump the entire environment KG:

```
curl http://127.0.0.1:8000/environment/kg/dump
```
If nothing has been updated yet, it should contain just the base ontology data from wildfire_ontology.ttl.


# Send a Drone Report: (What the drone sees)

```
curl -X POST http://127.0.0.1:8000/environment/drone_report \
     -H "Content-Type: application/json" \
     -d '{
           "location": "RedwoodForest",
           "severity": "HighSeverity",
           "fireSpreadRate": 8.5,
           "airQuality": 210,
           "visibleFlames": 15.3
         }'
```
Dump again to see the newly added event

```
curl http://127.0.0.1:8000/environment/kg/dump
```
Now you should see a new resource like :Fire_RedwoodForest with properties fireSpreadRate, airQuality, and visibleFlames.


# ADDONS for future use
- Agent Registration
If you want to register a new agent (not in the static ontology, but tracked dynamically by agent_manager.py), do something like:

```
curl -X POST "http://127.0.0.1:8000/agent/register?name=AlphaBot&agent_type=ReconDrone"
```