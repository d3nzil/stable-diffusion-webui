from loopgen import Prompt, run_prompts

# This whole thing works by first creating one or more prompts first and then running them afterwards.
# I did it this way mostly so I could better organize things

# To create prompt, create Prompt object and store it in variable, for example:
druid_princess = Prompt(
    name="druid_princess",
    prompt="texhnolyze and lain style, young druid princess, plant dress, bathing in forest, dark fantasy art, hyper detailed, artstation, sharp focus, symmetric eyes, cute face",
    seed=94,
    height=640,
)
# The "name" part is extra compared to normal use and determines the location and naming for the images.
# Once ran, you can find the output in outputs\loop\<prompt name>\

# Other required parameters are the "prompt" and "seed".
# Since I use this to generating more images of known seeds, random seeds are not directly supported,
# but it is possible to use random.randing from standard Python library to generate such seed.

# Size is by default 512x512, but can be overriden using "width" and "height" parameters.
# The defauls for this and other settings can be overriden in the loopgen.py file.

# Default sampler is "k_euler_a" as I use it most, can be changed using "sampler" parameter.
# Other names should be same as in the web interface, though exact name might be bit different is some cases.
# You might need to look at the other python files to get exact names... :(

# Scale is 7.5 by default and can be changed using "cfg_scale" parameter


# It is also possible to generate multiple variants of prompt, for example with different seed:
# (or do other variations if you know Python)
multiple_druid_princesses = [
    Prompt(
        name="druid_princess",
        prompt="texhnolyze and lain style, young druid princess, plant dress, bathing in forest, dark fantasy art, hyper detailed, artstation, sharp focus, symmetric eyes, cute face",
        seed=s,
        height=640,
    )
    for s in [87, 88, 94]
]


# Finally to run the prompts and generate the images use:
run_prompts(11, 101, 10, druid_princess)

# The numbers have following meanings, in order:
# 1. number - how many steps should be used for first image, here the first image will have 11 steps done
# 2. number - how many steps should be used for last image (where it should end)
# 3. number - how many steps should be between each image
# So for this example the generated images will have 11, 21, 31...101 steps
# And finally parameter is one or more prompts
# Note that if multiple prompts are generated, it has to be written like (note the * before name):
# run_prompts(11, 101, 10, *multiple_druid_princesses)


# Finally to run the whole thing you need to have terminal open and
# to have conda environment active, usually done running:
# conda activate ldm

# After that just run this python file using:
# python use_loopgen.py
# And wait for it to finish
