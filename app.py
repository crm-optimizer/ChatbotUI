from flask import Flask, render_template, request
import sys, json
from sentence_transformers import SentenceTransformer

from astrapy import DataAPIClient

app = Flask(__name__)



client = DataAPIClient("AstraCS:PymAJEaUNxADeRliMYDbMoOs:1ce519e1291d8eef05c4f447447a1e37db92c974c12e0ab9856c68e1dbd17c1f")
db = client.get_database_by_api_endpoint(
  "https://31985f08-265d-4c68-ac28-94ab534cab2f-us-east-2.apps.astra.datastax.com"
)
collection_name = "test_from_python"


def ask(query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode(query).tolist()
    collection0 = db.get_collection(collection_name)
    results = collection0.find({}, sort={"$vector": query_vector}, limit=5)
    output = ""
    for res in results:
        j = eval(res['text'].split('|')[1][7:])
        #import ipdb;ipdb.set_trace()
        output += f"<li>{j['Borrower Name']}<json-viewer>{json.dumps(j)}</json-viewer></li>"
        # for key in j.keys():
        #     entry = f"<td>{j[key]}</td>"
        #     output += entry
        # entry = f"<tr>{entry}</tr>"
    return f"<ul>{output}</ul>"
    return f"<table><tbody>{output}</tbody></table>"

class Object:
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    return ask(query)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=54321)
