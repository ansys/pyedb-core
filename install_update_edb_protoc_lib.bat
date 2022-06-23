cd pyedb-core

set python_venv_interpreter=.\.venv\Scripts\python.exe

%python_venv_interpreter% -m ansys.tools.protos_generator protos\ansys\api\edb\v1
%python_venv_interpreter% -m pip install .\dist\ansys-api-edb-v1-0.0.0.tar.gz