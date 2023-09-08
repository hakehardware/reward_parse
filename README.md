# reward_parse
This parses the rewards from the state.sql file. There seems to be some limitation regarding how many records are stored in there. For coinbases with smaller nodes pointing at them it should be fine. But when querying the largest coinbases I'm only getting 137 or so records. 

## Install Dependencies
### Ubuntu Only
```
sudo apt install python3.10-venv
```

## Install Instructions
Start by cloning the repo

### Move into directory
```
cd reward_parse
```

### Create Virtual Env
```
python -m venv env
```

### Enter Virtual Env
##### Windows
```
source env/Scripts/activate
```

##### Linux
```
source env/bin/activate
```

##### Install requirements
```
pip install -r requirements.txt
```

## Usage

##### For opts
```
python main.py -h
```

##### Example
This will check rewards, for the coinbase provided, and export the data to a new folder in the current directory called "output"
```
python main.py -r -c yourcoinbase -o ./output
```