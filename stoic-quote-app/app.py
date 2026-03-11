import random
import datetime
from flask import Flask, render_template, request, make_response
from all_meditations_quotes import quotes

app = Flask(__name__)

def get_quote(index):
    return quotes[index]

@app.route("/", methods=["GET"])
def home():

    total_quotes = len(quotes)

    # Daily quote
    if request.args.get("daily") == "1":
        today = datetime.date.today().toordinal()
        index = today % total_quotes

    # Random quote
    elif request.args.get("random") == "1":
        index = random.randint(0, total_quotes - 1)

    else:

        raw_index = request.args.get("index", type=int)

        if raw_index is not None:
            index = max(0, min(raw_index - 1, total_quotes - 1))

        else:
            cookie_index = request.cookies.get("last_index")

            if cookie_index and cookie_index.isdigit():
                index = int(cookie_index)
            else:
                index = 0

    quote = get_quote(index)

    next_index = (index + 1) % total_quotes
    prev_index = (index - 1) % total_quotes

    resp = make_response(render_template(
        "index.html",
        quote=quote,
        index=index,
        next_index=next_index,
        prev_index=prev_index,
        total_quotes=total_quotes
    ))

    resp.set_cookie("last_index", str(index), max_age=60*60*24*30)

    return resp


if __name__ == "__main__":
    app.run(debug=True)