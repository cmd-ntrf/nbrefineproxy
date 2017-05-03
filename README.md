# nbrefineproxy

**nbrefineproxy** provides Jupyter server and notebook extensions to proxy an OpenRefine refine.

![Screenshot](screenshot.png)

If you have a JupyterHub deployment, nbrefineproxy can take advantage of JupyterHub's existing authenticator and spawner to launch RStudio in users' Jupyter environments. You can also run this from within Jupyter. Requires [nbserverproxy](https://github.com/jupyterhub/nbserverproxy).

## Installation

Install the library:
```
pip install git+https://github.com/cmd-ntrf/nbrefineproxy
```

Either install the extensions for the user:
```
jupyter serverextension enable  --py nbrefineproxy
jupyter nbextension     install --py nbrefineproxy
jupyter nbextension     enable  --py nbrefineproxy
```

Or install the extensions for all users on the system:
```
jupyter serverextension enable  --py --sys-prefix nbrefineproxy
jupyter nbextension     install --py --sys-prefix nbrefineproxy
jupyter nbextension     enable  --py --sys-prefix nbrefineproxy
```
