"""Text-only procedural engineering fixtures. These are NOT GPT/person footage."""
from pathlib import Path
import argparse
import wave
import numpy as np
from PIL import Image, ImageDraw, GifImagePlugin


def background(width=90, height=160):
    y, x = np.mgrid[:height, :width]
    rng = np.random.default_rng(731)
    noise = rng.integers(0, 14, (height, width))
    return np.stack(((x*3+y+noise)%180+20, (y*2+noise)%160+30,
                     (x+y+noise)%150+40), axis=2).astype('uint8')


def motion_frames(count=30, width=90, height=160):
    bg = background(width, height)
    frames = []
    for i in range(count):
        im = Image.fromarray(bg)
        x = round(width*.3+i)
        ImageDraw.Draw(im).ellipse((x, height*.42, x+14, height*.42+20), fill=(240, 40, 50))
        frames.append(np.array(im))
    return frames


def save_gif(frames, path, durations=None):
    ims = [Image.fromarray(x) for x in frames]
    ims[0].save(path, save_all=True, append_images=ims[1:],
                duration=durations or [170]*len(ims), disposal=1, optimize=False)


def disposal_fixture(path, disposal):
    """Full white base, local green patch disposed, local blue patch displayed."""
    palette = [255,255,255, 255,0,0, 0,255,0, 0,0,255] + [0]*756
    base = Image.new('P', (64, 96), 0); base.putpalette(palette)
    green = Image.new('P', (12, 12), 2); green.putpalette(palette)
    blue = Image.new('P', (12, 12), 3); blue.putpalette(palette)
    with Path(path).open('wb') as f:
        blocks, _ = GifImagePlugin.getheader(base)
        blocks[0] = b'GIF89a'+blocks[0][6:]
        for b in blocks: f.write(b)
        for image, offset, disp, duration in [(base,(0,0),1,100),(green,(10,20),disposal,200),(blue,(40,60),1,300)]:
            for b in GifImagePlugin.getdata(image, offset=offset, disposal=disp, duration=duration): f.write(b)
        f.write(b';')


def transparent_fixture(path):
    palette = [0,0,0, 255,0,0, 0,255,0] + [0]*759
    ims = []
    for i in range(3):
        im = Image.new('P', (64,96), 0); im.putpalette(palette)
        ImageDraw.Draw(im).rectangle((8+i*5,20,18+i*5,30),fill=1+i%2)
        ims.append(im)
    ims[0].save(path,save_all=True,append_images=ims[1:],duration=[100,200,300],
                transparency=0,disposal=2,optimize=False)


def make_all(directory):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    frames = motion_frames()
    save_gif(frames, directory/'fixed.gif')
    save_gif([np.roll(background(), i*3, axis=0) for i in range(12)], directory/'scroll.gif')
    # Deliberate grid/slice failure: abrupt alternating independent panels.
    rng = np.random.default_rng(924)
    grid = []
    for i in range(8):
        frame = background() if i%2 == 0 else rng.integers(0,256,(160,90,3),dtype=np.uint8)
        grid.append(frame)
    save_gif(grid, directory/'grid_slip.gif')
    save_gif(motion_frames(3), directory/'variable.gif', [100, 700, 200])
    disposal_fixture(directory/'disposal2.gif', 2)
    disposal_fixture(directory/'disposal3.gif', 3)
    transparent_fixture(directory/'transparent.gif')
    Image.fromarray(background()).save(directory/'static.gif')
    with wave.open(str(directory/'tone.wav'), 'wb') as f:
        rate = 24000
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate)
        f.writeframes((np.sin(np.arange(rate)*2*np.pi*440/rate)*4000).astype('<i2').tobytes())
    return directory


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path)
    print(make_all(p.parse_args().out))
