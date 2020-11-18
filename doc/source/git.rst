git
===

Git is a distributed source code management / version control system. Since it is distributed, each local copy of a repository is a full-blown repository and is identical in scope, features and functionality to a repository hosted on a server.

============= ================================================
command       description
============= ================================================
``git stash`` temporarily store away local uncommitted changes
============= ================================================

.. contents:: Table of Contents



``git stash``
-------------

Temporarily stash, i.e. store away, local uncommitted changes to the working directory.

Use cases:

- When you need to pull because of some upstream change that will be relevant to your current work, but the pulled changes can't be applied because of your current work in progress.
- When you are working on something, but need to interrupt this to quickly implement something else

Relevant commands:

- ``git stash list``: show the list of stashes
- ``git stash show <stash>``: show information about a particular stash
- ``git stash push [-p|--patch] [-m <message>]``: create a stash and revert the working directory to the state of the last commit
- ``git stash pop``: apply a stash on top of the current working directory and then delete it from the list of stashes

  - if there is a conflict and the stash can't be applied, then the conflict has to be resolved manually and the stash deleted with ``git stash drop``

- ``git stash branch``: promote a stash to a branch, leaving at the previous commit, i.e. a stash pop/apply conflict is resolved by creating a new feature branch
- ``git stash clear``: delete all stashes
- ``git stash drop <stash>``: delete a particular stash
