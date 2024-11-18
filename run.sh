cd src && python3 -m gunicorn main:app -b 0.0.0.0:9819 --log-level debug --access-logfile - --error-logfile -
