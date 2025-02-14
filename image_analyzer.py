import os
from openai import OpenAI
import base64
from pathlib import Path
import replicate
import requests
from io import BytesIO

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(client, image_path):
    base64_image = encode_image_to_base64(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image? Please provide a detailed description that could be used as a prompt for generating a similar image. Make it descriptive but concise."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content

def generate_image(prompt, output_path, original_filename):
    input_data = {
        "prompt": prompt
    }
    
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input=input_data
    )
    
    base_filename = os.path.splitext(original_filename)[0]
    
    for index, item in enumerate(output):
        image_path = os.path.join(output_path, f"{base_filename}_generated_{index}.webp")
        response = requests.get(item)
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"Generated image saved to {image_path}")

def main():

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    image_folder = "images"
    results_folder = "analysis_results"
    generated_folder = "generated_images"
    
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    
    Path(results_folder).mkdir(exist_ok=True)
    Path(generated_folder).mkdir(exist_ok=True)
    
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(image_folder, filename)
            print(f"\nAnalyzing {filename}...")
            
            try:
                description = analyze_image(client, image_path)
                
                result_path = os.path.join(results_folder, f"{filename}_analysis.txt")
                with open(result_path, 'w', encoding='utf-8') as f:
                    f.write(f"Analysis for {filename}:\n\n{description}")
                
                print(f"Analysis saved to {result_path}")
                
                print(f"Generating new image based on analysis...")
                generate_image(description, generated_folder, filename)
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main() 