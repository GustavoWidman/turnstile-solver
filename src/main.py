from DrissionPage.common import Settings
from sanic import Sanic, json
from sanic.request import Request
from sanic_cors import CORS

from turnstile import turnstile

Settings.set_language("en")


app = Sanic("CloudflareTurnstileSolver")
CORS(app)


@app.post("/")
async def turnstile_endpoint(request: Request):
	if not request.json:
		return json({"error": "Missing JSON body"}, status=400)

	# check if json has only url key
	if "url" not in request.json or len(request.json) != 1:
		return json(
			{"error": "Invalid JSON body, pleas provide only a 'url' key"}, status=400
		)

	url = request.json["url"]

	try:
		token = turnstile(url)
		return json({"token": token})
	except Exception as e:
		return json({"error": str(e)}, status=500)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000, single_process=True)
