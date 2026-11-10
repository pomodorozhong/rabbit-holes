# Git & Github

This very page is serve to be a table of contents. And [this Project Board](https://github.com/pomodorozhong/rabbit-holes/projects/2?fullscreen=true) is used to manage the progress of all the related works.

## Roadmaps

### Roadmap of Git section

-   [ ] Basic usage
-   [ ] Commit Message conventions
-   [ ] Branching conventions
-   [ ] Tools
-   [ ] Scripts for advanced use cases

### Roadmap of Github section

-   [ ] Issues
-   [ ] Pull request
-   [ ] Actions
-   [ ] All sorts of conventions

## Git

### Usage

-   [Deleting a branch checked out in another worktree](worktree-branch-deletion.md) — locate the checkout, preserve work, and remove or detach it before deleting the branch.
-   Multiple repo & Submodule
    -   [What's the best practice for putting multiple projects in a git repository? - Stack Overflow](https://stackoverflow.com/questions/14679614/whats-the-best-practice-for-putting-multiple-projects-in-a-git-repository)
    -   [github - How to link folder from a git repo to another repo? - Stack Overflow](https://stackoverflow.com/questions/36554810/how-to-link-folder-from-a-git-repo-to-another-repo/36554930#36554930)
        -   "Submodule are different git repositories under the same root."
    -   to setup all submodule: `git submodule update --init --recursive`
    -   [Git 進階應用 Submodule 與 Subtree，使用它們來拆分專案 | Puck's Blog](https://blog.puckwang.com/post/2020/git-submodule-vs-subtree/)
-   Copy commits from one Git repo to another: Patch
    -   [linux - How to copy commits from one Git repo to another? - Stack Overflow](https://stackoverflow.com/questions/37471740/how-to-copy-commits-from-one-git-repo-to-another)
    -   [git: Apply changes introduced by commit in one repo to another repo - Stack Overflow](https://stackoverflow.com/questions/3816040/git-apply-changes-introduced-by-commit-in-one-repo-to-another-repo)
    -   [What is the difference between git cherry-pick and git format-patch | git am? - Stack Overflow](https://stackoverflow.com/questions/52119937/what-is-the-difference-between-git-cherry-pick-and-git-format-patch-git-am)
-   [On undoing, fixing, or removing commits in git](https://sethrobertson.github.io/GitFixUm/fixup.html)
    -   "a fairly comprehensive guide to recovering from what you did not mean to do when using git."
-   [Difference between author and committer in Git? - Stack Overflow](https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git)

### Placeholder Title 1

Here goes another placeholder text.

## Github

### Repository settings

-   [Turn on automatic head branch deletion for many repositories](scripts/auto-delete-branches.sh) — a script for GitHub's "Automatically delete head branches" setting, which deletes a pull request's branch on GitHub once the pull request merges.
    -   Which of my repositories have the setting off? `list` scans a folder of clones (default `~/repo`) and writes the ones you administer to a text file.
    -   How do I turn it on for only some of them? Delete or comment out lines in that file, then run `apply` to turn the setting on for each repository left.
    -   Does it work with squash merges? Yes. The setting applies to every merge method, but only to pull requests merged on GitHub after it is turned on, and it never deletes your local branches.
