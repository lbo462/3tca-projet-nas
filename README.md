# 3TCA Projet NAS

Léo BONNAIRE Léonard PRINCE Kowsigan ALAGARAJAH Hédi SFAXI Matthieu NSI ELA Mounir RADJABOU

## How to use confgen

<hr>

1. Create a new GNS3 project
2. Build your backbone architecture
3. Write down the JSON file describing your architecture, including your client's edge routers
4. In a Python virtual env, install the requirements with
```shell
pip install -r requirements.txt 
```
5. Launch script with 
```shell
python -m confgen -c <path-to-json-file> -n <gns3-project-name>
```
The writing to the routers can take time. Make a coffe before the start of the process.


## How to use git

<hr>

### **1. Install git on your machine**

On Windows : Install [Git Bash](https://git-scm.com/downloads)

On Linux : probably already installed (try `git --version` to check)

### **2. Configure git**

#### **2.1 Configure git locally**

Configure your name and email with the following commands :

```shell
$ git config --global user.name "your name here"
$ git config --global user.email "your email here"
```

#### **2.2 Connection to github repo**

First thing needed is to create a set of SSH keys to access this repo.

(See tutorial full here : [https://docs.github.com/fr/authentication/connecting-to-github-with-ssh](https://docs.github.com/fr/authentication/connecting-to-github-with-ssh))

Step-by-step process:

1. Generate a SSH key and add it to your SSH-agent ([detailed tutorial](https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent))

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
```
Do not change the default folder and enter a solid passphrase.

Then add your key to your SSH agent

```shell
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_ed25519
```

2. Add it to your github profile

```shell
cat ~/.ssh/id_ed25519.pub
```
Copy the exact output of this command and paste it on [Github](https://github.com/settings/ssh/new).


### **3. Clone the repo**

```shell
git clone git@github.com:leoNord462/3tca-projet-nas.git
```

This creates a folder named after the github repo. `cd` to this repo to work within it.

<br>

With the above configuration, you should be able to access with read and write access to the distance repo.

### **Every day use**

Before working on the repo, remember to pull the changes made by other.

```shell
git pull origin <your-branch>
```

When you finished a task and want to commit your changes, use

```shell
$ git add -A  # This add your files to be commited
$ git commit -m "an-explicit-message-to-describe-your-work"  # Commit your changes on your local repo
$ git push origin <your-branch>  # Push your commit to github
```

The use of github might be handy for beginners so don't hesitate to ask.

#### **Work on branches**

To work on a specifiq branch:

```shell
$ git fetch origin  # retrieve remote branches

$ git checkout <your-branch>  # change to branch you work on
```

**! Please, don't work on branch master. The branch master should be a clean branch. !**

When you work on a new issue, create the issue (via the milestone) and a related branch on github, then checkout locally with the above commands. When you work is done and ready for the branch master, create a pull request that will be reviewed before merging.
