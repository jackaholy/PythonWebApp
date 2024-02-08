from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)


@app.route("/submit_score", methods=["post"])
# When the user submits a new score
def new_score():
    score = request.form["data"]
    # Add score to the csv file
    with open("scores.csv", "a") as file:
        file.write(score + "\n")
    return redirect("/")


@app.route("/")
# Run the actual page
def run_page():
    # Get total number of entries
    total_entries = get_total_entries()
    # Get mean score
    mean_score = get_mean()
    # Get median score
    median_score = get_median()
    # Get best and worst scores
    best_score, worst_score = get_best_and_worst_scores()
    scores = open_file("scores.csv")
    # Tie together the python and html
    return render_template("index.html", mean_score=mean_score, median_score=median_score, best_score=best_score,
                           worst_score=worst_score,
                           scores=scores, total_entries=total_entries)


# Open and read the file returning each of the scores
def open_file(file):
    with open(file, "r") as file:
        # Created with the help of chat.openai.com
        scores = [int(score.strip()) for score in file if score.strip().isdigit()]
    return scores


# Get the average of all the scores in the file
def get_mean():
    scores = open_file("scores.csv")

    # If the file is empty
    if not scores:
        return None

    # Calculate mean score
    total = 0
    for score in scores:
        total += score
    mean = total / len(scores)

    return mean


def get_median():
    scores = open_file("scores.csv")

    # If the file is empty
    if not scores:
        return None

    # Calculate median of scores
    sorted_scores = sorted(scores)
    n = len(sorted_scores)

    if n % 2 == 0:
        # If the number of scores is even, calculate the average of the middle two scores
        middle1 = sorted_scores[n // 2 - 1]
        middle2 = sorted_scores[n // 2]
        median = (middle1 + middle2) / 2
    else:
        # If the number of scores is odd, take the middle score
        median = sorted_scores[n // 2]

    return median


def get_best_and_worst_scores():
    scores = open_file("scores.csv")

    # If the file is empty
    if not scores:
        return None, None
    # Sort the scores to find the highest and lowest number in file
    sorted_scores = sorted(scores)
    best_score = sorted_scores[-1]  # Last element is the highest score
    worst_score = sorted_scores[0]  # First element is the lowest score

    return best_score, worst_score


def get_total_entries():
    scores = open_file("scores.csv")
    total = len(scores)

    return total


if __name__ == "__main__":
    app.run(port=4000)
