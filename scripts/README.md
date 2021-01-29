Visit [Kaggle Python API](https://github.com/Kaggle/kaggle-api) to install the dependency for ```crawl-kaggle.py```, check how to store credentials for authentication.

To convert all the .ipynb to .py
```shell
cd <folder-name>
shopt -s globstar
for f in **/*.ipynb; do
    jupyter nbconvert --to script $f
done
```
