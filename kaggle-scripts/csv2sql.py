import pandas
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://p2d2:p2d2@localhost/module4')
conn = engine.connect()
df = pandas.read_csv('something')

df.to_sql('something', conn, index=False)

# psql --username=p2d2
# p2d2
# \c module4
# \d something
