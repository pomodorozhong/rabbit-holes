# Recovering a commit after its branch is deleted

A branch disappears from the branch list, yet its last commit can usually still be recovered. Deleting a branch removes a name, and the commit stays in the object database for a while. This guide shows how to find that commit and keep it.

The explanation depends on **reachability**. Starting at a branch or tag, Git can follow a commit to its parents, its directory tree, and the blobs containing file contents. A commit that no ref leads to is **unreachable**, which puts it at risk of eventual removal without erasing it right away. [Git objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

## Lose a commit on purpose

Try this in a new, disposable directory with a Git author identity configured.

```sh
git init -b main
git commit --allow-empty -m "Start example"
git switch -c scratch-export
printf 'example export\n' > demo.mov
git add demo.mov
git commit -m "Save the export"
git switch main
git branch -D scratch-export
```

`git log --all --oneline` now starts from `main` alone and omits the export commit.

## Find it in the reflog

The **reflog** is a local record of where HEAD and each branch have pointed. Run `git reflog show HEAD` and look for the line `commit: Save the export`. [Git reflog](https://git-scm.com/docs/git-reflog)

Inspect that commit with `git show --stat <id>`, using the object ID from the reflog line. Then give it a durable name with `git tag keep-export <id>`, or use `git branch` if development should continue there. The new ref keeps the commit, its ancestors, and their file contents reachable.

## Search the object database when the reflog can't help

If the reflog has no useful entry, `git fsck --no-reflogs --unreachable` lists objects that no ref leads to. Run it before making the rescue tag to see the difference. A **dangling** commit is an unreferenced tip among those objects. Its parents can still count as unreachable even though the tip points to them. [Git fsck](https://git-scm.com/docs/git-fsck)

## Know how long you have

Reflogs are local and their entries expire. Garbage collection can prune older unreachable objects after its retention period, and once an object has been pruned, recovery needs another copy. A clone won't help unless it already has the commit, because cloning copies what refs can reach. [Git garbage collection](https://git-scm.com/docs/git-gc)

The same reachability rules explain the opposite problem, a file you deleted that keeps downloading. [Removing a large file from Git history](remove-large-file-from-history.md) follows that case.
