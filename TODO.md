# TODO: Make Lifestyle Data Analytics Platform Workable Website

## Completed Steps
- [x] Check Python version (3.13.9 installed)
- [x] Create virtual environment (venv created)
- [x] Set execution policy for PowerShell scripts
- [x] Activate virtual environment
- [x] Install dependencies (pip install -r requirements.txt) - IN PROGRESS (large packages like pandas, numpy, plotly)
- [x] Update config.py to use SQLite database

## Pending Steps
- [ ] Wait for pip install to complete (currently installing plotly and other large packages)
- [ ] Run `python app.py` to initialize database and create sample data
- [ ] Run `python app.py` to start the Flask server on localhost:5000
- [ ] Open browser to http://localhost:5000 to verify the website loads
- [ ] Test basic functionality (register, login, dashboard)

## Notes
- Database changed from MySQL to SQLite for simplicity (config.py updated)
- Existing SQLite DB file exists in instance/lifestyle_analytics.db
- App will run on http://localhost:5000 with debug=True
