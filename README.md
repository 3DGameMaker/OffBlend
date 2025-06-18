# OffBlend
Live off axis projection with head tracking for blender

Thanks to https://github.com/calcoloergosum/blender-off-axis-projection/  for the original code
Requirements: 

Git (install at https://objects.githubusercontent.com/github-production-release-asset-2e65be/23216272/a1a32cf7-fc3c-48d3-9066-be664b463f9b?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250618%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250618T211050Z&X-Amz-Expires=300&X-Amz-Signature=cf3c67fd8a158f8c761edd08016931423035388b87bf1747e8df8d9c68255a86&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DGit-2.50.0-64-bit.exe&response-content-type=application%2Foctet-stream)

Python 3.11

Blender 2.93 - 3.0

Pip

How to use:
Open command prompt (write cmd in start menu)

Run "git clone https://github.com/3DGameMaker/OffBlend/"

Run "cd OffBlend"

Run "pip install -r requirements.txt"

Run "python background.py"

Open Blender, then make a new project.

Go into the "Scripting" tab and press "Open"

Choose blender.py

Now make a plane called "Plane"

And keep your camera's name as "Camera"

Now set the plane's X scale to 2.93373

And the plane's Y scale to 1.65022

Now put as many objects on the plane as you want.

Now you can press Alt+P, then Space.

Go into the camera's view and you can see it tracks your head with off axis projection.
