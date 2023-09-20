# super-duper-disco
This document should help users set up their environment with the necessary configuration in order to run the MemorializedMe AI project locally.

**NOTE**: the following instructions are made for Windows users, so some commands may vary slightly based on your command line and/or OS.

# Environment Setup
Follow the appropriate sections of these [instructions (may need to be updated)](https://docs.google.com/document/d/1uYu-kk7q7z2wjNTK4PK_p4P8bZZrmPgu-_e_ZylhbRI/edit) for installing the respective versions of the packages required for this project.
1. Install Anaconda and the packages mentioned in the instructions under "Install Anaconda" and "Install Flask"; refer to the instructions linked above.
2. Upon verifying the successful installation of the various packages, navigate to the directory where you'd like to clone the project, clone *this* directory, and navigate to the new directory.

	In this example, I'm navigating to the `test` folder to clone the project:
```shell
cd test
git clone https://github.com/mkazemiv/super-duper-disco.git
cd super-duper-disco
```
3. Now, create a new Batch script (`.bat` extension) inside the `super-duper-disco` folder with the specifications below. You can write this script using any text editor.

	In this example, I'll be naming my script `chicken.bat`:
```shell
@echo off

REM Set the variables
set SUPABASE_URL=YOUR_SUPABASE_URL
set SUPABASE_KEY=YOUR_SUPABASE_API_KEY
set APP_SECRET_KEY=boop
set FLASK_APP=hello.py
```

If you initially write and save the script somewhere else (using a text editor like Notepad, for example), make sure to move it into the `super-duper-disco` folder before proceeding.

4. Write another Batch script for running the application. This script will need to be placed in a **different directory**.

	In this example, I'll be naming my script `start_project.bat` (but you may name yours as you wish):
```shell
@echo off

REM Activate the conda environment
call conda activate flask_env3_11_4

REM Navigate to project directory (this may be different 
cd test\super-duper-disco

REM Run the 'chicken.bat' script (replace with the actual script name if you chose a different name)
call chicken.bat

REM Display a message
echo Running Memorialized AI Project

REM Run the Flask application
flask run --host=0.0.0.0
```
**NOTE**: When launching the app via Anaconda (shown later in the instructions), Anaconda uses your user home folder as the default directory. In this script, the line that says `cd test\super-duper-disco` **should navigate from *your specific user* folder directly to the *project* folder**. So, make sure to confirm that the path specified in this line of the script successfully changes directories as stated.

- Some clarification in case you're confused: In my case, for example, my user folder is `C:\Users\mkazemiv` and the `test` folder (where the project is) is located directly in my user directory, which makes navigation easy. So, from my user folder, I can simply run `cd test\super-duper-disco` and reach the project folder from my user folder.

*If you're unsure about the path you're using for this line of the script and would like to test it*:
- start a new CMD.exe prompt or Powershell window (I'm using a CMD.exe prompt here but the commands are exactly the same for Powershell)
- navigate to the `Users` directory 
```shell
C:\Windows\System32> cd /Users
```
- navigate to *your **personal** user folder*
```shell
C:\Users> cd randomGithubUser
```
- then run the `cd` command with the specified path and confirm that it works (I'm making up a hypothetical path for example)
```shell
C:\Users\randomGithubUser> cd Desktop
```
- if you run `dir` at this point (or `ls` for Powershell), the project files should be displayed and you'll know that the path you have is good

5. as

# Supabase Setup
