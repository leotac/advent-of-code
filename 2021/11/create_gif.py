from glob import glob
import imageio
from tqdm import tqdm

DIR = "img2"

images = [imageio.imread(f) for f in tqdm(sorted(glob(f"{DIR}/0*png")))]
imageio.mimsave(f'{DIR}.gif', images, format="GIF-PIL", fps=30)

images = [imageio.imread(f) for f in tqdm(sorted(glob(f"{DIR}/state*.png")))]
imageio.mimsave(f'{DIR}_phase.gif', images, format="GIF-PIL", fps=30)

