from flask import  Flask,request
import json
from graphene import ObjectType ,Argument,Schema,String,Field
from flask_graphql import GraphQLView
app = Flask(__name__)
class Query(ObjectType):
      hello = String(name = String(default_value = "stranger"))
      def resolve_hello(root, info, name):
        return f'Hello {name}!'
schema = Schema(query=Query)
@app.route("/graphql/",methods=['POST'])
def graphql():
    data=json.loads(request.data)
    print(data)
    return json.dumps(schema.execute(data['query']).data)



if __name__ == '__main__':
    app.run(port=3000, debug=True)



