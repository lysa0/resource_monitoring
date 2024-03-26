# Tool for monitoring CPU and RAM for remote servers  

**DB** &mdash; Some mongodb instance (need docker installed and running);  
**Agent** &mdash; Agent, collecting current CPU and RAM metrics and return it by REST API /ram and /cpu endpoints;  
**Exporter** &mdash; Exporter, collecting metrics from REST API requests from Agent and export his in DB;  
**Client** &mdash; Dashboard that collects metrics from the DB and creates graphs at /plot endpoint.  

To use it:  
0. Set up some variables in env.sh;
1. Run mongodb instance (db/rund.sh) and create user (script contains in utils/prepare.sh);
2. Copy agent for each node (utils/rsync.sh $HOST or use utils/prepare.sh) and run them (cd agent; bash run.sh);
3. Run Exporter (cd exporter; bash run.sh), run Client (cd client; bash run.sh).  

Every app running in venv, requirement libraries downloading in run.sh scripts.  

After completing these steps, the dashboard will be available at http://localhost:15001/plot. 
