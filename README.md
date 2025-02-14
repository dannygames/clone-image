Image Clone Tool
A Python tool that analyzes images using OpenAI's GPT-4 and generates similar images with a Replicate model.

Features
Image Analysis: Encodes images to Base64 and generates descriptive prompts via GPT-4.
Image Generation: Creates new images using the Replicate model.
Batch Processing: Automatically processes all supported images in the images/ folder.
Requirements
Python 3.6+
Libraries: openai, replicate, requests
Setup
Clone the Repository:

bash
Copy
git clone https://github.com/dannygames/clone-image.git
cd image-clone-tool
Install Dependencies:

bash
pip install openai replicate requests
Set Environment Variables:

bash
export OPENAI_API_KEY="your_openai_api_key_here"
export REPLICATE_API_TOKEN="your-replicate-token"
Directory Structure
bash
images/                # Input images
analysis_results/      # Analysis text files
generated_images/      # Generated images
main.py                # Main script
Usage
Place images in the imsages/ folder (supported: .png, .jpg, .jpeg, .gif, .webp).

Run the script:

bash
Copy
python main.py
Results are saved in the analysis_results/ and generated_images/ folders.