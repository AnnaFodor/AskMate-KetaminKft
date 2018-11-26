from flask import Flask, render_template, request, redirect
import data_manager
import util

app = Flask(__name__)


@app.route("/")
def login_user():
    return render_template("login_page.html", action="login")


@app.route("/registration", methods=["GET", "POST"])
def register_new_user():
    if request.method == "POST":
        usr_input = request.form.to_dict()
        usr_input["password"] = util.hash_password(usr_input["password"])
        data_manager.register_user(usr_input)
        return redirect("/")
    return render_template("login_page.html", action="new_user")






@app.route("/index", methods=["POST", "GET"])
def route_list():
    if request.method == "GET":
        questions = data_manager.show_questions()
        return render_template('list.html', questions=questions, action=None)
    else:
        questions = data_manager.show_questions_by_order(request.form['direction'],
                                                         request.form["order_type"])
        return render_template('list.html', questions=questions, action=None)


@app.route("/ask-question", methods=["GET", "POST"])
def route_ask_question():
    if request.method == "GET":
        return render_template('ask-question.html')
    else:
        new_question = {
            "question_subject": request.form["question_subject"],
            "question_text": request.form["question_text"],
            "url": request.form["url"]
        }

        data_manager.add_new_question(new_question)
        return redirect("/index")


@app.route("/question/<id>", methods=["GET", "POST"])
def route_question(id):
    if request.method == "GET":
        questions = data_manager.get_question_details(id)
        answers = data_manager.get_answer_details(id)
        comments = data_manager.get_comments(id)
        tags = data_manager.get_question_tags(id)
        all_tags = data_manager.get_all_tags()
        return render_template("question.html", question=questions, answers=answers, comments=comments, tags=tags, all_tags=all_tags)


@app.route("/search_question", methods=["POST"])
def search_question():
    search_parameter = request.form["search_parameter"]
    search_result = data_manager.search_question(search_parameter)
    return render_template("list.html", results=search_result, action="search")




@app.route("/question/vote_up/<id>", methods=["POST"])
def route_question_voting_up(id):
    vote = "Vote up"
    data_manager.change_vote_number(vote, id)
    return redirect("/index")


@app.route("/question/vote_down/<id>", methods=["POST"])
def route_question_voting_down(id):
    vote = "Vote down"
    data_manager.change_vote_number(vote, id)
    return redirect("/index")



@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def route_edit_answer(answer_id):
    answer_detail = data_manager.get_the_answer(answer_id)
    if request.method == "GET":
        return render_template('answer.html', answer_detail=answer_detail)
    else:
        new_message = request.form["edit_answer_text"]
        data_manager.get_current_answer_details(answer_id, new_message)
        print(answer_detail)
        return redirect("/question/" + str(answer_detail['question_id']))


@app.route("/add_answer/<id>", methods=["POST"])
def route_add_answer(id):
    new_answer = {
        "question_id": id,
        "answer_text": request.form["answer_text"]
    }
    data_manager.add_answer(new_answer)
    return redirect("/index")


@app.route("/add_comment/<id>", methods=["POST"])
def add_comment(id):
    comment = request.form["comment_text"]
    data_manager.add_comment(id, comment)
    return redirect("/question/" + str(id))


@app.route("/question/<id>/add_tag", methods=["GET", "POST"])
def add_new_tag(id):
    if request.method == "GET":
        tags = data_manager.get_all_tags()
        return render_template("addtag.html", tags=tags, question_id=id)

    new_tag_name = request.form["new_tag_name"]
    data_manager.create_new_tag(new_tag_name)
    return redirect("question/" + str(id))


@app.route("/question/add_new_tag_to_question/<id>", methods=["POST"])
def add_new_tag_to_question(id):
    tag_to_add = request.form["available_tags"]
    tag_id = data_manager.fetch_tag_id_by_tag_name(tag_to_add)
    data_manager.add_tag_to_current_question(id, tag_id["id"])
    return redirect("/question/" + str(id))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )


