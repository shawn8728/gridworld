from flask import Flask, render_template, request, jsonify
from QLearning import q_learning
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/square', methods=['POST'])
def square():
    n = int(request.form['size'])
    square_list = [[j for j in range(1, n+1)] for i in range(n)]
    return render_template('square.html', square_list=square_list)


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()

    size = data.get('size')
    start = data.get('start')    
    end = data.get('end')
    blocked = data.get('blocked')
    
    # Learning rate
    alpha = data.get('alpha') if data.get('alpha') else 0.1
    # Discount factor
    gamma = data.get('gamma') if data.get('gamma') else 0.9
    # Exploration probability
    epsilon = data.get('epsilon') if data.get('epsilon') else 1.0
    # Number of episodes to run the algorithm
    num_episodes = data.get('episodes') if data.get('episodes') else 1000

    # Parse the input parameters
    start = tuple(start)
    end = tuple(end)
    blocked = [tuple(block) for block in blocked]

    # Update the Q-values using the Q-learning algorithm
    # alpha = 0.1  # Learning rate
    # gamma = 0.9  # Discount factor
    # epsilon = 1.0  # Exploration probability
    # num_episodes = 1000  # Number of episodes to run the algorithm

    # print(gamma, file = sys.stderr)

    # Run the Q-learning algorithm
    path = q_learning(size, alpha, gamma, epsilon, num_episodes, start, end, blocked)
    return path
    

    
if __name__ == '__main__':
    app.run(debug=True)
