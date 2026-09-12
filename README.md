# AI-Powered-Women

- Materials for "How to Train Your Own Neural Network", a hands-on tutorial by Isabella Douzoglou on September 12, 2026
- Attendees see what a convolutional neural network sees when it looks at a photo, using a cat from the Oxford-IIIT Pet dataset

## Contents

- `AI-Powered-Women_IsabellaDouzoglou_Tutotiral.ipynb`: the notebook attendees work through
  - Images as tensors, starting from a small tensor typed in by hand
  - A cat photo at high and low resolution, then split into its red, green and blue values
  - The same photo as a 24 × 24 greyscale matrix, with a 5 × 5 patch zoomed in
  - Labels for the task: 0 is cat, 1 is dog
  - Convolution one step at a time: worked out by hand, checked against `F.conv2d`, and animated as a GIF
- `AI-Powered-Women.key`: Keynote slides for the short lecture that opens the session
- `.vscode/settings.json`: shows the notebook's text in the Urbanist font

## Running the notebook

- Needs Python 3 with `torch`, `torchvision`, `numpy`, `matplotlib`, `Pillow` and Jupyter
- Download the Oxford-IIIT Pet dataset (about 775 MB) into `data/` before running the image cells

  ```bash
  python -c "from torchvision.datasets import OxfordIIITPet; OxfordIIITPet('data', download=True)"
  ```

- The first image cell downloads the Urbanist font into `data/fonts/` for the plot titles
