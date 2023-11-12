---
lastmod: 2023-11-9
---

<div align='center'>

# NLP Lab
</div>

This program is designed to process and analyze natural language data, a subfield of artificial intelligence known as Natural Language Processing (NLP).

## Installation

### Build from source

To install this program from the source, follow these steps:

```sh
# Clone the repository to your local machine.
git clone https://github.com/uname/repo.git

# Navigate to the cloned repository.
cd repo

# Install the required dependencies.
pip install -r requirements.txt

# Build the program.
python setup.py 

# Alternatively, you can run the program directly.
python launch.py 
```

### Prerequisite
1. CUDA

    - Check if CUDA is already installed:

    ```
    ls /usr/local | grep cuda
    ```

1. CUDA Toolkit Driver

1. CUDA Toolkit

- https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=deb_local

1. CUDA Toolkit Driver


1.  RAPIDS  (instal with pip)

    RAPIDS is a suite of software libraries for executing end-to-end data science and analytics pipelines entirely on GPUs. Here’s how you can instal


    - If CUDA 12 is installed, use the following command to install RAPIDS:
    ```sh
    pip install \
        --extra-index-url=https://pypi.nvidia.com \
        cudf-cu12 dask-cudf-cu12 cuml-cu12 cugraph-cu12 cuspatial-cu12 cuproj-cu12 cuxfilter-cu12 cucim
    ```

    - To uninstall, use:
    ```
    pip uninstall cudf-cu12 dask-cudf-cu12 cuml-cu12 cugraph-cu12 cuspatial-cu12 cuproj-cu12 cuxfilter-cu12 cucim
    ```

    - If CUDA 11 is installed, use the following command to install RAPIDS:
    ```
    pip install \
        --extra-index-url=https://pypi.nvidia.com \
        cudf-cu11 dask-cudf-cu11 cuml-cu11 cugraph-cu11 cuspatial-cu11 cuproj-cu11 cuxfilter-cu11 cucim
    ```

    - To uninstall, use:
    ```
    pip uninstall cudf-cu11 dask-cudf-cu11 cuml-cu11 cugraph-cu11 cuspatial-cu11 cuproj-cu11 cuxfilter-cu11 cucim
    ```


    For more information, visit the RAPIDS documentation.

    - https://docs.rapids.ai/install#wsl2



## Trouble shootings

If you encounter any issues during the installation or running of the program, here are a few things you can check:

- Check your CUDA installation correctly:

    ```
    nvcc -V
    which nvcc 
    ```
    - https://docs.nvidia.com/cuda/wsl-user-guide/index.html#cuda-support-for-wsl2

- Check your Windows driver.
    
- Check your PATH variable. If you encounter an error like
    ` ImportError: libcuda.so.1: cannot open shared object file: No such file or directory`
    you might need to set your PATH variable in your shell configuration:

    - For fish shell
    
    ```fish
    sudo find /usr/ -name 'libcuda.so.*'

    set -gx CUDA_HOME /usr/local/cuda
    set -gx LD_LIBRARY_PATH /usr/lib/wsl/lib/
    set -gx NUMBAPRO_NVVM /usr/local/cuda/nvvm/lib64/libnvvm.so
    set -gx NUMBAPRO_LIBDEVICE /usr/local/cuda/nvvm/libdevice/
    ```

    - For bash shell:

    ```bash
    export CUDA_HOME=/usr/local/cuda
    export LD_LIBRARY_PATH=/usr/lib/wsl/lib/
    export NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
    export NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
    ```

    
### Acknowledgements

These providers make this project possible:

- https://huggingface.co/cyberagent/calm2-7b-chat

- https://huggingface.co/datasets/wikipedia
