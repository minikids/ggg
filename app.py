from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Encoding map (character -> encoded string)
encoding_map = {
    'a': '=dsfkjhgw',
    'b': '=371432=324234=32504585400450-05495',
    'c': '=sdfkewufhwehfuewhdsads',
    'd': '=f5563635463',
    'e': '=dsfjiwnfwijnfdjsfj-ewfwejfh',
    'f': '=sdkhuewfhewf_fenwfwednfjewifejfiwjfwew',
    'g': '=jdshfjsfdfds_fwenjewfjnfwje',
    'h': '=sdfwuefhweihuskdjwnfweushdifenwdsjfnewuihwfiwefdnjwksiuefhwfe',
    'i': '=sdfdsfsdfsdf',
    'j': '=43sdfdsfdsfsdf7h',
    'k': '=437dfsgregerjnkgrgeregh',
    'l': '=437hgregergerg',
    'm': '=437hergreg',
    'n': '=437hregregreg',
    'o': '=437rgergeregregh',
    'p': '=437hregrgegafdsfdsfsdfdsfdsfsf',
    'q': '=43gvvsdv7h',
    'r': '=437fsdfgegh',
    's': '=43dsfasdas=7h',
    't': '=437sdfdskjfwejiweh',
    'u': '=43bcbbcbcbcbcbcbc7h',
    'v': '=437dfsjksdflalkjasldaskmdh',
    'w': '=sdfkalksadsamlmaklm',
    'x': '=asfasklmdalksm',
    'y': '=asdjkaslmdmaskldmlasmdlaskmlmasmdlaksmd',
    'z': '=kasldlsakldkasdk'
}

# Decoding map (encoded string -> character)
decoding_map = {v: k for k, v in encoding_map.items()}

# HTML template with JavaScript for AJAX
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Encoder/Decoder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .container {
            display: flex;
            gap: 20px;
        }
        .panel {
            flex: 1;
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h2 {
            margin-top: 0;
            color: #444;
        }
        textarea, input {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 15px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 4px;
            word-wrap: break-word;
            min-height: 20px;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <h1>Secret Encoder/Decoder</h1>
    
    <div class="container">
        <div class="panel">
            <h2>Encoder</h2>
            <form id="encodeForm">
                <input type="text" id="encodeInput" placeholder="Enter text to encode" required>
                <button type="button" onclick="encodeText()">Encode</button>
            </form>
            <div id="encodeResult" class="result hidden">
                <strong>Encoded result:</strong><br>
                <span id="encodedOutput"></span>
            </div>
        </div>
        
        <div class="panel">
            <h2>Decoder</h2>
            <form id="decodeForm">
                <input type="text" id="decodeInput" placeholder="Enter encoded string" required>
                <button type="button" onclick="decodeText()">Decode</button>
            </form>
            <div id="decodeResult" class="result hidden">
                <strong>Decoded result:</strong><br>
                <span id="decodedOutput"></span>
            </div>
        </div>
    </div>

    <script>
        function encodeText() {
            const input = document.getElementById('encodeInput').value;
            if (!input) return;
            
            fetch('/encode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text: input})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('encodedOutput').textContent = data.result;
                document.getElementById('encodeResult').classList.remove('hidden');
            })
            .catch(error => console.error('Error:', error));
        }

        function decodeText() {
            const input = document.getElementById('decodeInput').value;
            if (!input) return;
            
            fetch('/decode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({encoded_text: input})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('decodedOutput').textContent = data.result;
                document.getElementById('decodeResult').classList.remove('hidden');
            })
            .catch(error => console.error('Error:', error));
        }

        // Allow pressing Enter to submit
        document.getElementById('encodeInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                encodeText();
            }
        });

        document.getElementById('decodeInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                decodeText();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/encode', methods=['POST'])
def encode():
    data = request.get_json()
    text = data.get('text', '').lower()
    encoded_chars = []
    
    for char in text:
        if char in encoding_map:
            encoded_chars.append(encoding_map[char])
        else:
            encoded_chars.append(char)  # Keep non-alphabet characters as-is
    
    return jsonify({'result': ''.join(encoded_chars)})

@app.route('/decode', methods=['POST'])
def decode():
    data = request.get_json()
    encoded_text = data.get('encoded_text', '')
    decoded_chars = []
    i = 0
    n = len(encoded_text)
    
    while i < n:
        matched = False
        # Try to match the longest possible code first
        for code in sorted(decoding_map.keys(), key=len, reverse=True):
            if encoded_text.startswith(code, i):
                decoded_chars.append(decoding_map[code])
                i += len(code)
                matched = True
                break
        if not matched:
            # If no code matched, keep the character as-is
            decoded_chars.append(encoded_text[i])
            i += 1
    
    return jsonify({'result': ''.join(decoded_chars)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
