from flask import Flask, render_template, request, redirect, url_for
from database import Base, engine, db_session
from models import Debate
from services_ai import ai_service


app = Flask(__name__)
Base.metadata.create_all(engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        topic = request.form.get("topic")
        side = request.form.get("side")
        argument = request.form.get("argument")

        if topic and side and argument:
            debate = Debate(
                topic=topic,
                side=side,
                argument=argument
            )
            db_session.add(debate)
            db_session.commit()
            return redirect(url_for("list_debates"))

    return render_template("create.html")


@app.route("/debates")
def list_debates():
    debates = db_session.query(Debate).all()
    return render_template("list.html", debates=debates)


@app.route("/debate/<int:id>")
def detail(id):
    debate = db_session.get(Debate, id)
    return render_template("detail.html", debate=debate)

@app.route("/ai/<int:id>", methods=["POST"])
def ai_action(id):
    debate = db_session.get(Debate, id)

    counter, feedback, rating = ai_service.generate_ai(
        debate.argument,
        debate.side
    )

    debate.ai_counter = counter
    debate.ai_feedback = feedback
    debate.rating = rating

    if debate.scores:
        debate.scores += f",{rating}"
    else:
        debate.scores = str(rating)

    db_session.commit()
    return redirect(url_for("detail", id=id))


@app.route("/counter/<int:id>", methods=["POST"])
def counter_ai(id):
    debate = db_session.get(Debate, id)

    user_counter = request.form.get("user_counter")

    reply, feedback, rating = ai_service.generate_counter_ai(
        debate.argument,
        user_counter
    )

    debate.user_counter = user_counter
    debate.ai_reply = reply
    debate.ai_counter_rating = rating
    debate.ai_feedback = feedback

    if debate.scores:
        debate.scores += f",{rating}"
    else:
        debate.scores = str(rating)

    db_session.commit()
    return redirect(url_for("detail", id=id))


@app.route("/end/<int:id>", methods=["POST"])
def end_debate(id):
    debate = db_session.get(Debate, id)

    nums = []

    if debate.rating is not None:
        nums.append(debate.rating)

    if debate.ai_counter_rating is not None:
        nums.append(debate.ai_counter_rating)

    if debate.scores:
        for x in debate.scores.split(","):
            x = x.strip()
            if x.isdigit():
                nums.append(int(x))

    if nums:
        debate.average_score = round(sum(nums) / len(nums), 2)
    else:
        debate.average_score = 0

    db_session.commit()
    return redirect(url_for("detail", id=id))



if __name__ == "__main__":
    app.run(debug=True)
