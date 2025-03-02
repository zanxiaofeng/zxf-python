# Python Virtual Env
- suto apt install python3-venv
- python3 -m venv venv3
- source venv3/bin/activate

# Install Package
- pip install scapy
- pip install notebook
- pip install matplotlib
- pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Setup Requirements.txt
- pip freeze > requirements.txt
- pip install -r requirements.txt

# Process
- 1. Loading data in PyTorch. https://pytorch.org/tutorials/beginner/basics/data_tutorial.html
- 2. Building neural networks in PyTorch. https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
- 3. Training your model. https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
- 4. Saving & Loading your model. https://pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html