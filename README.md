# EnvBuilder

EnvBuilder is a tool designed to analyze Python and Jupyter files to extract dependencies and create virtual environments. It helps Python programmers manage their project dependencies efficiently.

## Features

- Analyze Python (`.py`) and Jupyter (`.ipynb`) files to extract dependencies.
- Generate `requirements.txt` for pip or `environment.yml` for conda.
- Create virtual environments with the extracted dependencies.
- User-friendly GUI with configuration options.
- Automatically maps popular import aliases (e.g., `cv2`, `plt`, `np`) to real package names.

> 🗂️ **Note**: The environment file is saved in the **same directory as the analyzed file** by default. This path can be changed through the GUI settings.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Elishah-John/EnvBuilder.git

2. Navigate to the project directory:

   ```bash
   cd EnvBuilder

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

## Usage
1. Run the application:
   
   ```bash
   python envbuilder.py
    ```
2. Use the GUI to select a Python or Jupyter file.
3. Choose the output type ( pip or conda ) and generate the environment file.
4. Save the generated environment file or create a virtual environment directly from the application.

## 📂 Output Examples

### `requirements.txt`
```ini
numpy==1.24.2
matplotlib==3.6.3
opencv-python==4.5.5.64
```

### `environment.yml`
```yaml
name: env
channels:
  - conda-forge
dependencies:
  - numpy=1.24.2
  - matplotlib=3.6.3
  - opencv=4.5.5.64
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the Apache 2.0 license. See the LICENSE file for details.

## Contact
For any questions or suggestions: elishahjohn9@gmail.com
   

