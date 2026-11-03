# Removing a large file from Git history

A large export disappears from the checkout, yet cloning the repository still downloads it. Git keeps a file's contents for as long as any branch or tag can reach them, and a later commit that deletes the file leaves the earlier commits in place. This guide helps you decide whether you need to rewrite history, then removes the file and checks that it's gone.

## Decide whether you need to rewrite history

Rewriting history is only sometimes necessary. The right fix depends on where the file already is and what you want to stop.

| Where the file is | What you want | What to do | What happens to the file |
| --- | --- | --- | --- |
| Any commit | New checkouts no longer include it | Run `git rm`, then commit | It stays in history, and clones still download it |
| Only your latest commit, not yet pushed | It was never committed | Run `git rm`, then `git commit --amend` | It's gone from that branch's history |
| An older commit you've pushed, or a release tag | Clones stop downloading it | Rewrite history, as shown below | It's gone from the rewritten history |

Whichever fix you use, a `.gitignore` entry helps prevent adding the file again by accident. [GitHub's guide to large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

## See the file survive a deletion

Try this in a new, disposable directory with a Git author identity configured. A few bytes stand in for the large file so the exercise runs quickly.

```sh
git init -b main
printf 'A small project\n' > README.md
mkdir assets
printf 'example export\n' > assets/demo.mov
git add README.md assets/demo.mov
git commit -m "Add the project and an export"
git tag v1.0
git rm assets/demo.mov
git commit -m "Remove the export"
```

The latest commit has no `assets/demo.mov`, but `git log --all --oneline -- assets/demo.mov` still lists both commits, and `git show v1.0:assets/demo.mov` still prints the contents.

## Rewrite a copy of the repository

Work in a fresh mirror so that every branch and tag is included and the original directory remains available for comparison. `--no-local` makes this local clone copy objects through Git's transport. The filtering step uses the separate `git-filter-repo` tool. [git-filter-repo manual](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)

```sh
old_blob=$(git rev-parse v1.0:assets/demo.mov)
git clone --mirror --no-local . ../scrubbed.git
cd ../scrubbed.git
git filter-repo --invert-paths --path assets/demo.mov
git log --all -- assets/demo.mov
git rev-list --objects --all | cut -d ' ' -f 1 | grep -Fx "$old_blob"
```

The last two commands should print nothing here. The path check asks whether a surviving history mentions that name. The object-ID check asks whether any surviving ref reaches those same bytes, including under another name.

For a real export, include every historical path in the filter and check each known large blob ID. Renaming a file can leave another path to it, and editing it creates a different blob ID.

## Check the result

For a large, non-sensitive file, the practical success test is that a fresh clone reaches the intended release history without fetching that blob. Disk usage in an old clone can lag, because it has its own reflogs and retention policy.

A rewrite changes commit IDs, so anyone else using the repository needs a fresh clone. Merging an old branch back can bring the file with it.
