from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate_elo(a_rating, b_rating, winner, k=32):
    a_outcome = 1 / (1 + (10 ** ((b_rating - a_rating)/400)))
    b_outcome = 1 / (1 + (10 ** ((a_rating - b_rating)/400)))

    if winner == "A":
        score_a = 1
        score_b = 0

    elif winner == "B":
        score_a = 0
        score_b = 1

    elif winner == "D":
        score_a = 0.5
        score_b = 0.5

    else:
        print("Error.")

    a_new_rating = round(a_rating + (k * (score_a - a_outcome)))
    b_new_rating = round(b_rating + (k * (score_b - b_outcome)))

    return a_new_rating, b_new_rating


@app.route('/calculate_ratings', methods=['POST'])
def calculate_ratings():
    # Get JSON data from POST request.
    data = request.json
    a_rating = data.get('a_rating')
    b_rating = data.get('b_rating')
    winner = data.get('winner').upper()
    # Validate input
    if a_rating is None or b_rating is None or winner not in ["A", "B", "D"]:
        return jsonify({"error": "Invalid input"}), 400

    # Call Elo calculation function
    a_new_rating, b_new_rating = calculate_elo(a_rating, b_rating, winner)

    # Return new ratings as a JSON response
    return jsonify({
        "a_new_rating": a_new_rating,
        "b_new_rating": b_new_rating
    })


if __name__ == '__main__':
    app.run(debug=True)