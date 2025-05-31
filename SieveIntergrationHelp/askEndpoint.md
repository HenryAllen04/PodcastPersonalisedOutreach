Get Started
1
Setup
Install the Sieve Python client.


pip install sievedata
pip install sievedata
2
Authentication
Choose your preferred authentication method:

Terminal
Environment Variable
Authenticate with the Sieve CLI and follow the prompts to set up your credentials. Your API key can be found in the settings tab.


sieve login
sieve login
3
Push Job
Synchronous
Asynchronous
Use the following Python code to run the function in the background. This uses .push() instead of .run(), which submits a job and gets its results asynchronously as a concurrent.futures.future object. Note that push does not block, but calling .result() does.


import sieve

video = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/3c956311-a16b-41dc-9201-9e61fa4e9118/469da6d4-dc8e-4163-ac58-836716905e73-input-video.mp4")
prompt = "Generate a summary of the main narratives of the first and second halves of the game. Cite 3 specific moments from each half. Also include details about how each half ends."
start_time = 0
end_time = -1
backend = "sieve-fast"
output_schema = [object Object]

ask = sieve.function.get("sieve/ask")
output = ask.push(video, prompt, start_time, end_time, backend, output_schema)
print('This is printing while a job is running in the background!')
print(output.result())
import sieve

video = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/3c956311-a16b-41dc-9201-9e61fa4e9118/469da6d4-dc8e-4163-ac58-836716905e73-input-video.mp4")
prompt = "Generate a summary of the main narratives of the first and second halves of the game. Cite 3 specific moments from each half. Also include details about how each half ends."
start_time = 0
end_time = -1
backend = "sieve-fast"
output_schema = [object Object]

ask = sieve.function.get("sieve/ask")
output = ask.push(video, prompt, start_time, end_time, backend, output_schema)
print('This is printing while a job is running in the background!')
print(output.result())
For more production integration options, check out our documentation about webhooks.

Schema
Inputs
video sieve.File

The video to query.
prompt str

Question/instruction used to generate text based on the contents of the video.
start_time float

Start analysis at this timestamp (in seconds). Default is 0 (start of video).
end_time float

End analysis at this timestamp (in seconds). Default is -1 (end of video).
backend "sieve-fast" | "sieve-contextual"

Choose a backend model to process the video. Details in README.
output_schema dict

(Optional) A valid openapi schema to be enforced on the output.
Outputs
output Union

