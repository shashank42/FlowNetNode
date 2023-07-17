
# from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import StableDiffusionPipeline
import torch
import requests
from PIL import Image
import os
from GPUtil import showUtilization as gpu_usage
from numba import cuda
import random as rand

import os
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
device = "cuda"

import inspect
import warnings
from typing import List, Optional, Union
from pinatapy import PinataPy


def clearGPU():
    print("Initial GPU Usage")
    gpu_usage()                             

    torch.cuda.empty_cache()

    cuda.select_device(0)
    cuda.close()
    cuda.select_device(0)

    print("GPU Usage after emptying the cache")
    gpu_usage()
    
    torch.cuda.empty_cache()
    print(torch.cuda.memory_summary(device=None, abbreviated=False))

# This can be anything that the node operator desirs
model_path = "runwayml/stable-diffusion-v1-5"
def dummy(images, **kwargs): return images, False

pipe = None

def get_pinata_object():
     with open('pinata.txt') as f:
        lines = f.readlines()
        api_key = lines[0]
        # api_key = api_key.decode("utf-8")
        secret_api_key = lines[1]
        # secret_api_key = secret_api_key.decode("utf-8")
        
        api_key = api_key.split("\n")[0]
        secret_api_key = secret_api_key.split("\n")[0]
        
        # api_key = api_key.split("'")[1]
        # secret_api_key = secret_api_key.split("'")[1]
        
        print(api_key, secret_api_key)
        
        pinata = PinataPy(api_key, secret_api_key)
        return pinata

def infer(prompt, request_id, strength=.75, num_inference_steps=70, guidance_scale=11, num_images_per_prompt=1):
    global pipe
    if (pipe is None):
        # clearGPU()
        if not os.path.exists("pretrained/model"):
            pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16).to(device)                                    #safety_checker=dummy
            newpath = "pretrained"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            pipe.save_pretrained("pretrained/model")
        else:
            pipe = StableDiffusionPipeline.from_pretrained("pretrained/model", torch_dtype=torch.float16).to(device)                            #safety_checker=dummy
        
        
        
    
    generator = torch.Generator(device=device).manual_seed(1024)
    image = pipe(prompt=prompt, guidance_scale=10, num_inference_steps=70, generator=generator).images[0]

    image.save("test.png")
    
    pinata = get_pinata_object()
    
    file_ipfs = pinata.pin_file_to_ipfs("test.png")
    
    metadata_json = {
        "name": "FlowNet AI Inference",
        "description": prompt,
        "image": file_ipfs["IpfsHash"],
        "attributes": [
            {
                "trait_type": "Model",
                "value": "runwayml/stable-diffusion-v1-5"
            },
            {
                "display_type": "number",
                "trait_type": "guidance_scale",
                "value": 10
            },
            {
                "display_type": "number",
                "trait_type": "num_inference_steps",
                "value": 70
            },
            {
                "display_type": "number",
                "trait_type": "generator_seed",
                "value": 1024
            }
        ]
    }
    
    metadata_ipfs = pinata.pin_json_to_ipfs(metadata_json)

    
    if os.path.isfile("test.png"):
            os.remove("test.png")
    else:
        pass
    
    
    
    return metadata_ipfs["IpfsHash"]


