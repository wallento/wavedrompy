#%% [markdown]
# The current working directory must be in
# the `test` folder.  Even though this file resides in the `test` folder, VSCode starts the kernel in the "opened" folder by default, which is the root of the GitHub project.
#%%
import os

if not os.getcwd()[-4:] == 'test':
    os.chdir('./test')

#%% [markdown]
# # Test Case Selection and Configuration
# Change `file` to the .json that should be rendered and tested
#%%
#The json file to render with `wavedrompy` and `wavedrom`, then compare the results
file = './files/issue_14.json'

#The directory where the SVG and PNG files will be saved
tmpdir = './tmp'
wavedromdir = './tmp/wavedrom'

#%% from `test_render.py`
import subprocess
from os.path import splitext, basename

import wavedrom
from diff import diff_raster
from diff import main as diff

#%% [markdown]
# # Upstream Setup
# Uncomment these two lines if the environment needs to have wavedrom downloaded and installed
#%% from `test_render.py`, `wavedromdir(tmpdir_factory)`

#subprocess.check_call("git clone https://github.com/wavedrom/wavedrom.git {}".format(wavedromdir), shell=True)
#subprocess.check_call("npm install", cwd=str(wavedromdir), shell=True)

#%% [markdown]
# # Generate SVGs, Determine XML Differences, and Calculate Raster Difference
#%% from `test_render.py`, `test_upstream(tmpdir,wavedromdir,file)`
from IPython.display import SVG, display

test_name = splitext(basename(file))[0]
f_out_js = "{}/{}_js.svg".format(tmpdir, test_name)
f_out_py = "{}/{}_py.svg".format(tmpdir, test_name)

subprocess.check_call("node {}/bin/cli.js -i {} > {}".format(wavedromdir, file, f_out_js), shell=True)
wavedrom.render_file(file, f_out_py, strict_js_features=True)

display('wavedrom:')
display(SVG(f_out_js))
display('wavedrompy:')
display(SVG(f_out_py))

unknown = diff(f_out_js, f_out_py)

if len(unknown) > 0:
    msg = "{} mismatch(es)\n".format(len(unknown))
    msg += "js file: {}\npy file: {}\n".format(f_out_js, f_out_py)
    msg += "\n".join([str(action) for action in unknown])
    #pytest.fail(msg)
    display(msg)

raster_difference = diff_raster(f_out_js, f_out_py)

#%% [markdown]
# # Analyze Raster Difference
# This cell does some analysis on the difference between the two images generarted by rasterizing the SVG output by *wavedrom* and *wavedrompy*.  The cell saves several channel-specific differences to images so the differences can be visualized.
# 
# The process should work with differences in all four channels of an RGBA image.  It will not work with L (grayscale) images.  This has only been tested with RGBA images that have differences in either:
# - The RGB channels only
# - The alpha channel only
#%%
from IPython.display import display
from PIL import Image, ImageChops, ImageOps

differentBands = '' #To be appened with bands that have at least one different pixel

if raster_difference.getbbox() is None: #The images are identical
    print('Wavedrom and Wavedrompy rendered to indentical PNG images')
else:
    #Check which individual bands are different, and add bands with differences to `differentBands`
    for bandName, band in zip(raster_difference.getbands(), raster_difference.split()):
        if band.getbbox() is not None:
            differentBands += bandName
            print('Difference in ' + bandName + ' channel')

#Display differences in color bands, ignoring alpha
if 'R' in differentBands or 'G' in differentBands or 'B' in differentBands:
    print('Difference of RGB:')
    noAlpha = Image.merge('RGB', raster_difference.split()[0:3])
    noAlphaEnhanced = ImageOps.autocontrast(noAlpha)
    display(noAlphaEnhanced)
    noAlphaEnhanced.save('./tmp/' + test_name + '_noAlphaDiff.png')

#Display differences in alpha band as grayscale image
if 'A' in differentBands:
    print('Difference of alpha:')
    alphaOnly = raster_difference.split()[-1]
    alphaOnlyEnhanced = ImageOps.autocontrast(alphaOnly)
    display(alphaOnlyEnhanced)
    alphaOnlyEnhanced.save('./tmp/' + test_name + '_alphaOnlyDiff.png')

#%% Compose the original and difference images
import cairosvg, io

noAlphaCopy = noAlphaEnhanced.copy()

with open(f_out_js, encoding="utf-8") as fileObj_svg_js:
    svg_js = fileObj_svg_js.read()

png_js = cairosvg.svg2png(svg_js)
orig = Image.open(io.BytesIO(png_js))
origCopy = orig.copy()

#Compose the two images, 
noAlphaCopy.putalpha(255)
origCopy.putalpha(64)
noAlphaCopy.alpha_composite(origCopy)

#Use original transparency from wavedrom image
noAlphaCopy.putalpha(orig.split()[-1])

display(noAlphaCopy)
noAlphaCopy.save('./tmp/' + test_name + '_differenceAndOriginalComposed.png')
