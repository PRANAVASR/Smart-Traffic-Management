import os
from pathlib import Path
import matplotlib.pyplot as plt

# Get the folder containing saved graphs
BASE_DIR = Path(__file__).resolve().parent
folder = BASE_DIR / "traffic_analysis_outputs"

# Check whether folder exists
if not folder.exists():
    raise FileNotFoundError("Traffic analysis output folder not found!")

# Get all graph images
images = [
    f for f in os.listdir(folder)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

images.sort()

print("Total graphs found:", len(images))

# Display all graphs
for image in images:
    path = folder / image

    img = plt.imread(path)

    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.title(image)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

print("DATA VISUALIZATION COMPLETED SUCCESSFULLY!")