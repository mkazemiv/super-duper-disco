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
```
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
```
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

- Some clarification in case you're confused: In my case, for example, my user folder is `C:\Users\mkazemiv` and the `test` folder (where the project is) is located directly in my user directory, which makes navigation easy. So, from my user folder, I can simply run `cd test\super-duper-disco` and reach the project folder.

*If you're unsure about the path you're using for this line of the script and would like to test it*:
- start a new CMD.exe prompt or Powershell window (I'm using a CMD.exe prompt here but the commands are exactly the same for Powershell)
- navigate to the `Users` directory 
```shell
C:\Windows\System32> cd \Users
C:\Users>
```
- navigate to *your **personal** user folder*
```shell
C:\Users> cd randomGithubUser
C:\Users\randomGithubUser>
```
- then run `cd` with the specified path (I'm making up a hypothetical path for this example)
```shell
C:\Users\randomGithubUser> cd Desktop\MemorializedMe
C:\Users\randomGithubUser\Desktop\MemorializeMe>
```
- if you run `dir` at this point (or `ls` for Powershell), the project files should be displayed and you'll know that the path you have is good
- if the last two steps did not produce the expected results, then the path you've specific is incorrect and needs to be adjusted

# Supabase Setup
As we use Supabase for the backend of our application, a properly configured Supabase project is required for the application to function as expected. This part of the setup involves creating a new Supabase project, grabbing the project URL and API key from the project settings, configuring a few tables in our database, and site URL configuration.

1. Open [Supabase](https://supabase.com/dashboard/projects) and create a new project with a reasonable name and region.

2. After Supabase sets up the project (may take a few minutes), you'll be redirected to your project home screen. From there, go to the "Project Settings" page using the gear-shaped button at the bottom of the navigation menu on the far left.
<img alt="project_settings" src="https://i.imgur.com/9y2yCbm.png">

3. Click the "API" button to reach the API Settings page for your project.
<img alt="api_settings" src="https://i.imgur.com/DvWFAGn.png">

4. From this page, we need two items that will be copy-pasted into the `chicken.bat` script from [step 3 of the Environment Setup instructions](https://github.com/mkazemiv/super-duper-disco/#environment-setup): the *Project URL* and a *Project API key*.
	
- The Project URL is the first item from the top in the API Settings screen. Copy this link and paste it in place of the "YOUR_SUPABASE_URL" string from the script.
```
set SUPABASE_URL=>>>YOUR_SUPABASE_URL<<<
```
- The Project API keys will be just below the Project URL. Although which key you use has some security implications for your database, for now use the censored secret key (further documentation to be added later regarding this distinction!!). To capture this key, simply click the "Reveal" button once and then click the same button to "Copy". Then, paste this key in place of the "YOUR_SUPABASE_API_KEY" string in the next line of the script
```
set SUPABASE_KEY=>>>YOUR_SUPABASE_API_KEY<<<
```
Upon completing these two copy-paste operations, your `chicken.bat` script (or whatever you called it) should look something like this:
```
@echo off

REM Set the variables
set SUPABASE_URL=https://abcdabcdabcd.supabase.co
set SUPABASE_KEY=eyJhbGciOieyJhJh.234iOieyJhbGciOi...................................... (the key is usually very long)
set APP_SECRET_KEY=boop
set FLASK_APP=hello.py
```
5. Click the "SQL Editor" button on the far left menu and then on the SQL Editor page, create three tables using the "New query" button at the top left with the queries provided below
<img alt="sql_editor" src="https://i.imgur.com/WwO5wxG.png">

 - users table
```
create table
  public.users (
    id bigint generated by default as identity,
    created_at timestamp with time zone null default now(),
    full_name character varying null,
    phone character varying null,
    email character varying null,
    verified boolean default false,
    address character varying null,
    education character varying null,
    skill character varying null,
    interest character varying null,
    words_of_wisdom character varying null,
    gender character varying null,
    date_of_birth character varying null,
    contact_name character varying null,
    contact_phone character varying null,
    contact_relation character varying null,
    constraint users_pkey primary key (id)
  ) tablespace pg_default;
```
- files table
```
create table
  public.files (
    id bigint generated by default as identity,
    created_at timestamp with time zone null default now(),
    output_file character varying null,
    user_id bigint null,
    audio_file character varying null,
    image_file character varying null,
    constraint files_pkey primary key (id)
  ) tablespace pg_default;
```
- wishlist table
```
create table
  public.wailist (
    id bigint generated by default as identity,
    created_at timestamp with time zone null default now(),
    email character varying null,
    user_id bigint null,
    constraint wailist_pkey primary key (id)
  ) tablespace pg_default;
```
- Confirm that all three tables were successfully added by navigating to the "Table editor" screen using the button on the far left menu
<img alt="table_editor" src="https://i.imgur.com/edpEbS6.png">
<img alt="tables_added" src="https://i.imgur.com/SoUSzKS.png">

6. Lastly, we need to set our site & redirect URLs. To do this, go to the Authentication page of your project:
<img alt="auth" src="https://github.com/mkazemiv/super-duper-disco/assets/47222610/dcb289d6-f0e5-4467-90cd-32fcb190daf9">

- Then, click the "URL Configuration" link on the menu that appears
<img alt="url_config" src="https://github.com/mkazemiv/super-duper-disco/assets/47222610/3b98c149-6d77-4ade-ad8f-6ef861a814b7">

- On this page you'll see an editable field labeled "Site URL". Edit this field to `http://localhost:5000/home`. This is the URL you'll be routed to after a successful login.
- Then, in the "Redirect URLs" section located lower on the same page, click the green "Add URL" button and add `http://localhost:5000` as a redirect URL. This is the URL you'll be routed to after logging out of your account.

# Running Application
At this point, all basic setup is complete and you are ready to run the application on your local machine.

1. Open the "Anaconda Navigator" app, which we installed [earlier](https://github.com/mkazemiv/super-duper-disco/#environment-setup)
2. From the Home page of this app, launch a CMD.exe or Powershell Prompt (makes no difference). This should open a window with a prompt very similar to
```
(base) C:\Users\mkazemiv>
```
- Note that as mentioned earlier, the default directory of this window is your user folder, so proper placement of the second script comes into play at this step.

3. All that's left to do is to run the `start_project.bat` script (by entering its name) and the application will start.
```
(base) C:\Users\mkazemiv> start_project.bat
```
- If the app starts on a port other than 5000, you should go back to [step 6 of Supabase Setup](https://github.com/mkazemiv/super-duper-disco/#supabase-setup) and change the port numbers in the URLs.
