from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Sample graph represented as an adjacency matrix
# 0 represents no path between nodes, use a high value to represent "infinity" where there is no direct path
INF = float('inf')
graph = [
    [0, 10, INF, INF, INF, 5],
    [10, 0, 3, INF, INF, 2],
    [INF, 3, 0, 1, INF, INF],
    [INF, INF, 1, 0, 4, INF],
    [INF, INF, INF, 4, 0, 6],
    [5, 2, INF, INF, 6, 0]
]

# List of hospital locations
hospitals = [0, 4]

# Coordinates for each node (latitude, longitude)
coordinates = [
    (40.712776, -74.005974),  # Node 0
    (34.052235, -118.243683),  # Node 1
    (41.878113, -87.629799),  # Node 2
    (29.760427, -95.369804),   # Node 3
    (39.739236, -104.990251),  # Node 4
    (32.715736, -117.161087)   # Node 5
]

# Number of vertices in the graph
V = len(graph)

# Function to run the Floyd-Warshall algorithm
def floyd_warshall(graph):
    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))

    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# Precompute shortest paths between all pairs of nodes
shortest_paths = floyd_warshall(graph)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to get the nearest hospital
@app.route('/nearest_hospital', methods=['GET'])
def nearest_hospital():
    try:
        # Get current location from query parameters
        current_location = int(request.args.get('current_location'))

        if current_location < 0 or current_location >= V:
            return jsonify({'error': 'Invalid current location'}), 400

        # Find the nearest hospital
        min_distance = INF
        nearest_hospital = -1
        for hospital in hospitals:
            if shortest_paths[current_location][hospital] < min_distance:
                min_distance = shortest_paths[current_location][hospital]
                nearest_hospital = hospital

        if nearest_hospital == -1:
            return jsonify({'error': 'No hospital found'}), 404

        return jsonify({
            'nearest_hospital': nearest_hospital,
            'distance': min_distance,
            'hospital_coordinates': coordinates[nearest_hospital],
            'current_coordinates': coordinates[current_location]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
