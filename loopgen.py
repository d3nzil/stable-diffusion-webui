from pathlib import Path
from pprint import pformat

from scripts.webui import txt2img, txt2img_defaults


TEST_MODE = False
OVERWRITE_EXISTING = False


class Prompt:
    # Defaults, change if you consistently use different values
    _width = 512
    _height = 512
    _sampler = "k_euler_a"
    _cfg_scale = 7.5

    def __init__(
        self,
        name: str,
        prompt: str,
        seed: int,
        sampler=None,
        width=None,
        height=None,
        cfg_scale=None,
    ):
        self.prompt = prompt
        self.name = name
        self.seed = seed
        self.sampler = sampler or self._sampler
        self.cfg_scale = cfg_scale or self._cfg_scale
        self.width = width or self._width
        self.height = height or self._height


def run_prompts(start: int, end: int, step: int, *prompts: Prompt):
    prompt_count = len(prompts)
    for prompt in prompts:
        print(
            f"Running prompt {prompts.index(prompt)+1}/{prompt_count} named: {prompt.name}"
        )
        process_prompt(start, end, step, prompt)


def process_prompt(start, end, step, prompt: Prompt):
    if end <= start:
        print("end_iter must be higher than start_iter")
        exit(1)

    out_loop_dir = Path(__file__).parent / "outputs" / "loop"
    print(out_loop_dir.resolve())

    out_loop_dir = out_loop_dir / prompt.name
    try:
        out_loop_dir.mkdir(parents=True)
    except FileExistsError:
        pass

    # args are mostly copied from webui.py
    args = {
        "prompt": prompt.prompt,
        "seed": prompt.seed,
        "ddim_steps": 1,
        "sampler_name": prompt.sampler,
        "n_iter": 1,
        "batch_size": 1,
        "cfg_scale": prompt.cfg_scale,
        "height": prompt.height,
        "width": prompt.width,
        "realesrgan_model_name": None,
        "fp": None,
        "toggles": [1, 2],
        "ddim_eta": 0.0,
        "variant_amount": 0.0,
    }

    if TEST_MODE:
        start = end

    with open(out_loop_dir / f"{prompt.name}_{prompt.seed}.cfg", "w") as cfg_file:
        cfg_file.write(pformat(args))

    for i in range(start, end + 1, step):
        args["ddim_steps"] = i
        out_file = out_loop_dir / f"{prompt.name}_{prompt.seed}_{i:03}.png"
        if out_file.exists() and not OVERWRITE_EXISTING:
            print(f"File for iteration {i} alrady exists, skipping")
            continue
        print(f"Running iteration: {i}")
        output_images, _seed, _info, _stats = txt2img(**args)
        for j, image in enumerate(output_images):
            print(f"Saving to: {out_file.resolve()}")
            image.save(out_file)

    print("Prompt processing finished")
