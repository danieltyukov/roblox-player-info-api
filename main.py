from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import urllib.request, json

app = Flask(__name__)
CORS(app)

# http://127.0.0.1:5000/get-user-info?id=79826037
@app.route("/get-user-info")
@cross_origin(origin='*')
def getUserInfo():
    user_id = request.args.get("id")
    if user_id is None:
        return jsonify({"error": "No user id provided."})
    else:
        # https://games.roblox.com/v2/users/[user_id]/games?accessFilter=2&amp;limit=10&amp;sortOrder=Asc
        url = "https://games.roblox.com/v2/users/" + user_id + "/games?accessFilter=2&limit=10&sortOrder=Asc"
        response = urllib.request.urlopen(url)
        user_data = json.loads(response.read())

        game_ids = []
        for game in user_data["data"]:
            game_ids.append(game["id"])

        if len(game_ids) == 0:
            return jsonify({"error": "No games found."})
        else:
            return_data = []
            for game_id in game_ids:
                url = "https://games.roblox.com/v1/games/" + str(game_id) + "/game-passes?limit=100&sortOrder=Asc"
                response = urllib.request.urlopen(url)
                game_data = json.loads(response.read())

                if len(game_data["data"]) == 0:
                    continue
                else:
                    for game_pass in game_data["data"]:
                        if game_pass["sellerId"] is not None:
                            return_data.append(game_pass)

            return jsonify(return_data)

if __name__ == '__main__':
	app.config['SESSION_TYPE'] = 'filesystem'
	app.debug = True
	app.run(host='127.0.0.1', port=5000, debug = True)
        
# EXAMPLE RETURN DATA FOR ABPVE ID:
# [
#   {
#     "displayName": "VIP",
#     "id": 11770774,
#     "isOwned": false,
#     "name": "VIP",
#     "price": 150,
#     "productId": 1087324611,
#     "sellerId": 79826037,
#     "sellerName": "u_5g"
#   },
#   {
#     "displayName": "Radio",
#     "id": 11787967,
#     "isOwned": false,
#     "name": "Radio",
#     "price": 100,
#     "productId": 1087324630,
#     "sellerId": 79826037,
#     "sellerName": "u_5g"
#   },
#   {
#     "displayName": "Rainbow Carpet",
#     "id": 11788063,
#     "isOwned": false,
#     "name": "Rainbow Carpet",
#     "price": 500,
#     "productId": 1087324651,
#     "sellerId": 79826037,
#     "sellerName": "u_5g"
#   },
#   {
#     "displayName": "Radio",
#     "id": 11211040,
#     "isOwned": false,
#     "name": "Radio",
#     "price": 25,
#     "productId": 1070953522,
#     "sellerId": 79826037,
#     "sellerName": "u_5g"
#   },
#   {
#     "displayName": "Teddy Bear",
#     "id": 11225548,
#     "isOwned": false,
#     "name": "Teddy Bear",
#     "price": 5,
#     "productId": 1072229726,
#     "sellerId": 79826037,
#     "sellerName": "u_5g"
#   }
# ]