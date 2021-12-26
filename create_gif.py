from glob import glob
import imageio
from tqdm import tqdm

DIR = "img"

images = [imageio.imread(f) for f in tqdm(sorted(glob(f"{DIR}/*png")))]
imageio.mimsave(f'{DIR}.gif', images, format="GIF-PIL", fps=5)

