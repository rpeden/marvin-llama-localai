# Running Marvin on LLaMA

This repo contains a couple of hacks to help [Marvin](https://askmarvin.ai) run against a LLaMA model instead of OpenAI or Anthropic.

It's certainly not production ready, but it might be useful if you want to experiment a little! 

## Background

I knew [LocalAI](https://localai.io/) could wrap a LLaMA model in an OpenAI-compatible REST API, but until recently it didn't support function calling, so newer versions of Marvin didn't work. 

LocalAI recently added function calling, using llama.cpp's new-ish [ability to constrain samping](https://github.com/ggerganov/llama.cpp/pull/1773) using a BNF-like grammar.

So, I decided to try running Marvin against it. 

It failed pretty quickly, because LocalAI supports JSON schemas that refer to definitions using the `$defs` property. Marvin uses Pydantic v1 to generate JSON schemas, and it uses `definitions` instead of `$defs` (Pydantic 2 outputs `$defs`).

To see if Marvin would work after overcoming this small obstacle, I edited some of LocalAI's Go code to make it accept either `$defs` or `$definitions`. Fortunately, it's easy to trigger a rebuild when running LocalAI in Docker, so I set up a Docker Compose file, copies in the updated code, and rebuilds LocalAI on startup.

# What Works
- AI Functions
- AI Models

# What Doesn't Work
- AI Applications. 
  - The code LocalAI uses to transform a JSON schema into a grammar llama.cpp understands can't currently handle an `array` or `object` as one of the items in a `oneOf` or `anyOf`. This isn't an insurmountable obstacle, but it prevents Marvin `AIApplications`s from working right now.

# Requirements

- Python 3.10+
- Docker

# Usage Instructions

- Clone this repository.
- Create a new Python venv or Conda environment.
- Run `pip install -r requirements.txt`
- Download a GGML model into the `models` subdirectory. 
  - You can find plenty of them on [TheBloke's HuggingFace page](https://huggingface.co/TheBloke). 30B or larger models work best, but many 13B models and are much faster if you're running on CPU (or a GPU without a ton of VRAM), and even some 7B models seem to give decent results with Marvin. I've seen good results with `wizardlm-33b-v1.0-uncensored`, but I recommend trying several.
- Look at `models/gpt-4.yaml`. It's called `gpt-4` because that's the OpenAI model Marvin uses by default. So, LocalAI will take requests for `gpt-4` and route them to the LLaMA model you specify in `gpt-4.yaml`.
- Update the `model` attribute in `gpt-4.yaml` to match the filename of the GGML model you downloaded.
  - Note that you can also adjust model parameters in the same section of the YAML. Experiment a bit and see what works for you. Optimal settings will vary between LLaMA-based models. Read the [LocalAI advanced configuration docs](https://localai.io/advanced/) to learn more about all the options you can configure here.
- Next, take a look in `docker-compose.yaml`. Note that I've set it up to pull the CPU-only LocalAI image because it's smaller. If you intend to use CPU only, you don't need to change anything.
  - If you have an Nvidia GPU and you're running Linux, either on its own or in Windows via WSL2, I recommend using one of the CUDA versions of LocalAI. The images for CUDA 11 and 12 are both in the Compose file, but commented out. Pick the appropriate one depending on which version of CUDA you have installed, uncomment it, and comment out the CPU-only image.
  - You'll need to set up the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for Docker GPU support to work.
  - If you're running Linux via WSL2 you'll need to follow [these instructions](https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl).
  - Finally, you'll need to uncomment the entire `deploy` section in `docker-compose-yaml` to enable the GPU in Docker.
- Open a terminal, change to the directory where you cloned this repository, and run `docker compose up`.
- The first time you run this, it'll take a while to completely rebuild llama.cpp and LocalAI. Subsequent startups will be much faster.
- Run `python marvin_function.py` or `python marvin_model.py` to try one of the demo apps I've included.
- Have fun testing your own Marvin functions and models against different LLaMA models!
