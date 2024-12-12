from flask import Flask, Response, jsonify, request, make_response
import time

app = Flask(__name__)

# Метрики
metrics = {
    "request_count": 0,
    "total_response_time": 0.0
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/metrics", methods=["GET"])
def metrics_endpoint():
    avg_response_time = (
        metrics["total_response_time"] / metrics["request_count"]
        if metrics["request_count"] > 0
        else 0
    )
    prometheus_metrics = (
        f"# HELP request_count Total number of requests\n"
        f"# TYPE request_count counter\n"
        f"request_count {metrics['request_count']}\n"
        f"# HELP avg_response_time Average response time in seconds\n"
        f"# TYPE avg_response_time gauge\n"
        f"avg_response_time {avg_response_time}\n"
    )
    response = make_response(prometheus_metrics, 200)
    response.mimetype = "text/plain"
    return response

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    if request.endpoint != "metrics":
        metrics["request_count"] += 1
        metrics["total_response_time"] += time.time() - request.start_time
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
