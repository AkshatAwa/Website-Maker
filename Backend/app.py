from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

def process_with_ollama(prompt):
    try:
        full_prompt = f"""
        You are a senior frontend developer and UI/UX designer.

        Generate a beautiful and fully responsive **modern landing page** using **TailwindCSS**.

        ✅ Must include:
        - A full-screen hero section with a catchy heading, subheading, and image or illustration
        - Animated call-to-action buttons
        - Glassmorphism cards with hover effects
        - Gradient or blurred background
        - Responsive layout (mobile + desktop)
        - A professional looking footer with social media icons
        - Clean and minimalistic design

        ❌ Do NOT return markdown formatting, explanations, or code fencing (no ```html or similar).

        Return **only raw HTML** code with Tailwind utility classes.
        User Request: {prompt}
        """

        result = subprocess.run(
            ["ollama", "run", "codellama:7b"],
            input=full_prompt,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Ollama error: {e}")
        return None


@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    html_output = process_with_ollama(prompt)

    if html_output:
        print(html_output)  # Log the generated HTML to the console
        return jsonify({"html": html_output})
    else:
        return jsonify({"error": "HTML generation failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
