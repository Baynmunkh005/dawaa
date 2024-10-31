from flask import Flask, render_template
from neo4j import GraphDatabase

# Initialize Flask app
app = Flask(__name__)

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
username = "neo4j"              # Replace with your Neo4j username
password = "asdf1234"           # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

# Define a function to retrieve movies
def get_movies():
    with driver.session() as session:
        result = session.run("MATCH (m:Movie) RETURN m.title AS title, m.released AS year")
        return [{"title": record["title"], "year": record["year"]} for record in result]

# Define a function to retrieve persons
def get_persons():
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p.name AS name")
        return [{"name": record["name"]} for record in result]

# Flask route for movie list
@app.route('/movies')
def movie_list():
    movies = get_movies()
    return render_template("movie.html", movies=movies)

# Flask route for person list
@app.route('/persons')
def person_list():
    persons = get_persons()
    return render_template("person.html", persons=persons)

# Flask route for the home page
@app.route('/')
def home():
    return '''
        <h1>Welcome to the movie web app</h1>
        <a href="/movies">Movie list</a><br>
        <a href="/persons">Person list</a>
    '''

# Close the driver when the app stops
@app.teardown_appcontext
def close_driver(exception):
    driver.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
