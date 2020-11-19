git
===

Git is a distributed source code management / version control system. Since it is distributed, each local copy of a repository is a full-blown repository and is identical in scope, features and functionality to a repository hosted on a server.

====================== ================================================
command                description
====================== ================================================
``git commit --amend`` add uncomitted changes to the previous commit
``git stash``          temporarily store away local uncommitted changes
====================== ================================================

.. contents:: Table of Contents



``git commit --amend``
----------------------

Add uncommitted changes to the previous commit.

Use case:

- When you forget to add a change before committing
- When you add all your changes and commit them, but then notice that there is a bug
- When you want to edit the previous commit message (just do ``git commit --amend`` without adding any new changes)

This is straightforward as long as you have not pushed your previous commit to a remote respository yet.

.. code:: bash

  $ git add <somefile>   # add some changes
  $ git commit --amend   # amend the previous commit, i.e. add the new changes

This will bring up an editor with the commit message, which you can modify if you wish. In case you don't want to be given this opportunity, you can use ``git commit --amend --no-edit`` instead.

As long as you haven't pushed your previous commit, you can now do a single push.

.. warning:: When you have already pushed your previous commit, be extremely careful, as ``git commit --amend`` changes the history and other people may have already pulled your previous commit after you pushed it. Therefore, you should normally not ``git commit --amend`` after pushing. If you still want to do this, you have to force the push:

  .. code:: bash

    $ git push -f origin master   # or whichever branch you are using instead of 'master'



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
