# Virtual MCU

The Virtual MCU is a python app made to manage the resources the STM32 simulator uses.
This will be in a package.

HOW TO USE AND CREATE PACKETS IN VMCU_PACKAGE

To use the vmcu__package there are two ways.
To have the package in editable mode, go to the VMCU repository root.
create a virtual enviromment:
sudo apt update
sudo apt install python3.X-venv // X = your python version
source venv/bin/activate

pip install -e .

If you want to create a new package of the VirtualMCU you have to first add the token to your .pypirc:

nano ~/.pypirc

add this in the file:
[distutils]
index-servers =
testpypi
pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = token
password = <API_TOKEN>

write the API Key that is in the google drive of the Hyperloop Team:
Avionics/firmware/api_token.txt

for safety .pypirc only available for your user:
chmod 600 ~/.pypirc

then you have to create the new package make sure you have install build (pip install build),
IMPORTANT: change the version of the package before doing this:
python3 -m build

python3 -m pip install --upgrade twine //only first time
python3 -m twine upload --repository testpypi dist/*

If you want to use the Package only as User:
pip install -i https://test.pypi.org/simple/ vmcu