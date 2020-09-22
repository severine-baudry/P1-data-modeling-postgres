export PGPASSWORD=student
psql -U student -h 127.0.0.1 -d sparkifydb -c "SELECT * FROM songs LIMIT 5;"
