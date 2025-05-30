# Django Online Shopping System Demo Project
This is a Django online shopping system demo project, made by group A13, who study Database System Course in FengChia University, Taiwan.
## Use Instruction
* See [plain mysql scripts](https://github.com/ethan-devlab/HahaLife/blob/main/mysql/new_scripts.txt) for login account information.
* See LICENSE to use this project in your work.
# Install and Run
## Install MySQL
1. Go to [MySQL](https://dev.mysql.com/downloads/mysql/) to download **MySQL Community Server 9.3.0 Innovation**
If you use macOS and have homebrew installed, you can also use either
```
brew install mysql
``` 
or
```
brew install mysql-client
```
2. Download database file `new_scripts.txt` from [here](https://github.com/ethan-devlab/HahaLife/blob/main/mysql/new_scripts.txt), then run
```
mysql -u root -p < <path-to-file>/new_scripts.txt
```
or copy the content of `new_scripts.txt` and paste it into MySQL command line interface.
3. Or download [shopping.sql](https://github.com/ethan-devlab/HahaLife/blob/main/mysql/shopping.sql), and run
```
mysql -u root -p
```
```
mysql> CREATE DATABASE IF NOT EXISTS shopping;
mysql> USE shopping;
mysql> SOURCE <path-to-file>/shopping.sql
```
see [Executing SQL Statements from a Text File](https://dev.mysql.com/doc/refman/8.4/en/mysql-batch-commands.html) for more details.

## Set up Python environment
### For Windows:
```
python -m venv django_project
```
In the same directory, run the script in terminal
```
./django_project/Scripts/Activate
```
or run the following script in CMD instead
```
.\django_project\Scripts\Activate.bat
```
Make sure you have done the actions above to get into virtual environment, you will see something like `(django_project) C:\<Your Path>...` in your terminal or CMD.

Next, clone the project and install required packages.
```
git clone git@github.com:ethan-devlab/HahaLife.git
```
or
```
git clone https://github.com/ethan-devlab/HahaLife.git
```
then run
```
cd HahaLife
pip install -r requirements.txt
```
Finally, run
```
python manage.py runserver
```
The default url will be `127.0.0.1:8000/`


### For Linux/macOS
```
python3 -m venv django_project
```
In the same directory, run the script in terminal
```
source ./django_project/bin/activate
```
Make sure you have done the actions above to get into virtual environment, you will see something like `(django_project) <Your Path>...%` in your terminal.

Next, clone the project and install required packages.
```
git clone git@github.com:ethan-devlab/HahaLife.git
```
or
```
git clone https://github.com/ethan-devlab/HahaLife.git
```
then run
```
cd HahaLife
pip3 install -r requirements.txt
```
Finally, run
```
python3 manage.py runserver
```
The default url will be `127.0.0.1:8000/`
