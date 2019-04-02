from flask import Flask, render_template, request, redirect
import config
import riotgamesapi


app = Flask(__name__, static_url_path="/static")


@app.route("/")
def index():
    reason = request.args.get("reason")  # get reason from url
    reasons = config.get_value("reasons")  # load error messages from config
    if reason in reasons:
        message = reasons[reason]  # get corresponding message
    else:
        message = False

    return render_template("index.html", message=message)


@app.route("/<region>/<summoner>")
def masteries(region, summoner):
    account = riotgamesapi.account(region, summoner)
    if account["success"]:
        summoner = account["response"]["name"]  # change to proper capitalization
        summoner_id = account["response"]["id"]  # needed to get mastery data
        masteries = riotgamesapi.masteries(region, summoner_id)
        if masteries["success"]:
            champions = riotgamesapi.parse(masteries["response"])
            return render_template(
                "masteries.html", summoner=summoner, champions=champions
            )
        else:
            return redirect("/?reason=a")  # redirect home with message
    else:
        return redirect("/?reason=m")  # redirect home with message


@app.errorhandler(404)
def notfound(e):
    return redirect("/?reason=404")


@app.errorhandler(505)
def internalerror(e):
    # TODO: log error message
    return redirect("?/reason=505")


if __name__ == "__main__":
    app.run()
