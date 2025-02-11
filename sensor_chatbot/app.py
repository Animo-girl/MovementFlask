from flask import Flask, render_template, request, jsonify
import random
from openai import OpenAI

app = Flask(__name__)
#add your api-key here
client = OpenAI(
  api_key=""""""
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    name = data.get('name', 'User')
    acc = tuple(data.get('acc', (0, 0, 0)))
    gry = tuple(data.get('gry', (0, 0, 0)))
    gps = data.get('gps', 0)
    gender = data.get('gender', 'Unknown')
    weight = data.get('weight', '0 kgs')
    temp = data.get('temp', '0 degrees celsius')
    age = data.get('age', 0)
       
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
        {"role": "user", "content": f"""
    You are an advanced AI system designed to analyze human movement using a GenAI model. 
    Your task is to monitor the user's physical activity through a smartphone that is constantly with them. 
    Your primary objectives are:

    1. **Movement Detection**: Accurately identify the user's movement type (walking, running, or climbing stairs) using real-time data from the smartphone's sensors (accelerometer, gyroscope, etc.) Do not include the numbers in answers.

    2. **User Profiling**: Utilize the following user data to enhance your analysis:
    - Age
    - Gender
    - Weight
    - Location (considering environmental factors such as terrain)
    - Temperature (current weather conditions)

    3. **Safety Assessment**: Based on the detected movement type and user profile, provide timely, context-aware suggestions or alerts at regular intervals (e.g., every 5 minutes). This includes:
    - Evaluating if the current activity is safe considering the user's age and health profile.
    - Advising whether the user should take a break or adjust their activity (speed/type).
    - Offering insights on potential risks associated with their current movement (e.g., fatigue, environmental hazards).

    4. **Human-like Interaction**: Generate responses that are empathetic, informative, and relevant to the user's situation. Ensure the language and tone reflect a supportive virtual assistant that prioritizes the user's well-being.

    **Output Requirements**:
    - The response should be structured to include a clear analysis of the user's current activity, a safety assessment based on the provided user data, and actionable recommendations.
    - Maintain a friendly and encouraging tone in the generated responses to foster a positive user experience.

    **Example Scenario**: 
    User profile: 30 years old, male, 180 lbs, currently in a hot location. 
    Detected movement: Running for 15 minutes. 
    Response should assess if running in the heat is appropriate, suggest hydration, 
    and advise on pacing based on the user's weight and temperature.

    Utilize this framework to create an interactive and supportive system that enhances user safety and promotes healthy 
    activity levels through continual assessment and guidance.

    The Users name is {name} who is a {gender} the movement right now from accelerometer is {acc} and gryoscope is {gry} and GPS is {gps}, the users age is {age} and weight is {weight} and {name} is currently in {temp} temperature."""}
    ]
    )

    print(completion.choices[0].message);

    return jsonify({'response': str(completion.choices[0].message.content)})

if __name__ == '__main__':
    app.run(debug=True)
