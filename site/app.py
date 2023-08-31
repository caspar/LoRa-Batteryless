from flask import Flask, request, jsonify, render_template_string
import base64

app = Flask(__name__)

current_adc = "N/A"
current_voltage = "N/A"
current_resistance = "N/A"
current_water_level = "N/A"

@app.route('/')
def index():
    return render_template_string("""
        <h1>ADC: {{ adc }}</h1>
        <h1>Voltage: {{ voltage }} V</h1>
        <h1>Resistance: {{ resistance }} ohms</h1>
        <h1>Water Level: {{ water_level }} cm</h1>
    """, adc=current_adc, voltage=current_voltage, resistance=current_resistance, water_level=current_water_level)

@app.route('/receive_ttn_data', methods=['POST'])
def receive_ttn_data():
    global current_adc, current_voltage, current_resistance, current_water_level
    try:
        print(request.json)
        encoded_payload = request.json.get('uplink_message', {}).get('frm_payload', '')
        decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
        print(f"Decoded Payload: {decoded_payload}")

        adc, voltage, resistance, water_level = decoded_payload.split(",")

        current_adc = adc.strip()
        current_voltage = voltage.strip()
        current_resistance = resistance.strip()
        current_water_level = water_level.strip()

        return "Data processed successfully."
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process the request."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
