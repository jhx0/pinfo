# pinfo
**pinfo** is a simple python script to show information about a specific **PID** and your **system** in general.

**NOTE:** The script needs to be run with **root** privileges - since most information in **/proc** requires root permissions for a given **PID**.

## Example output:


## Usage
```
$ ./pinfo PID
```

## Install
1. Clone/Download the code in this repository
2. Install the necessary dependencies
```
$ pip install -r requirements.txt
```
3. Execute pinfo with a PID of your choosing
```
$ ./pinfo 1
```

## Note
Two **dependencies** are needed to run pinfo: **psutil** and **colorama**, which can be found in most distributions repositories.
For example on **Debian / Ubuntu**:
```
# apt install python3-psutil python3-colorama
```
Be sure to **check your distributions package repository**.

## Hint
If there should be issues feel free to open a **Issue** here on **GitHub** to futher inspect the problem.
**Suggestions** and **feedback** are of course welcome.

##
