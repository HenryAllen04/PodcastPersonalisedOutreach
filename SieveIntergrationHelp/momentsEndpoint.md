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

video = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/9ce2165b-d3fa-4e36-9cc6-8a2aba124493/c709fd8c-151e-42ff-a0ba-2376d9571aae-input-video.mp4")
query = "red car"
min_clip_length = 3
start_time = 0
end_time = -1
render = True

moments = sieve.function.get("sieve/moments")
output = moments.push(video, query, min_clip_length, start_time, end_time, render)
print('This is printing while a job is running in the background!')
for output_object in output.result():
    print(output_object)
import sieve

video = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/9ce2165b-d3fa-4e36-9cc6-8a2aba124493/c709fd8c-151e-42ff-a0ba-2376d9571aae-input-video.mp4")
query = "red car"
min_clip_length = 3
start_time = 0
end_time = -1
render = True

moments = sieve.function.get("sieve/moments")
output = moments.push(video, query, min_clip_length, start_time, end_time, render)
print('This is printing while a job is running in the background!')
for output_object in output.result():
    print(output_object)
For more production integration options, check out our documentation about webhooks.

Schema
Inputs
video sieve.File

The video to extract moments from.
query str

Description of what to search the video for.
min_clip_length float

Minimum clip/moment length in seconds allowed in output.
start_time float

Process the video starting at this time (in seconds).
end_time float

Process the video up to this time (in seconds).
render bool

Whether to render extracted clips and include in outputs.
Outputs
output Any

