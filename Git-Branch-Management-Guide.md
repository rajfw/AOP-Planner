Git Branch Management Guide

How to Switch Branches & Update from Main

📋 Quick Reference Cheat Sheet

Daily Workflow

bash
# Update your branch with latest main
git checkout main
git pull origin main
git checkout your-branch
git rebase main  # or git merge main
git push origin your-branch
Branch Operations

Task	Command
List branches	git branch -a
Create & switch	git checkout -b new-branch
Switch branch	git checkout branch-name
Delete branch	git branch -d branch-name
Update from remote	git fetch --all
🔀 Three Common Scenarios

Scenario 1: Update Existing Feature Branch

bash
# 1. Save current work
git stash

# 2. Get latest main
git checkout main
git pull origin main

# 3. Update your branch
git checkout feature-branch
git rebase main  # Clean history
# OR git merge main  # Preserve branch timeline

# 4. Restore work
git stash pop

# 5. Push updates
git push origin feature-branch
Scenario 2: Create New Branch from Latest Main

bash
# 1. Ensure main is current
git checkout main
git pull origin main

# 2. Create new branch
git checkout -b feature/new-feature

# 3. Verify
git status  # Should show "On branch feature/new-feature"
Scenario 3: Switch to Existing Branch & Sync

bash
# Switch to branch
git checkout existing-branch

# Sync with remote (if exists)
git pull origin existing-branch

# Update from main
git fetch origin
git merge origin/main
🔄 Merge vs Rebase: Which to Use?

Use MERGE when:

Working on long-lived branches
Multiple people collaborating on same branch
You want to preserve complete branch history
Working with release branches
bash
git merge main
# Creates a merge commit showing branch integration
Use REBASE when:

Working on feature branches
You want linear, clean history
Preparing for pull request
Solo development
bash
git rebase main
# Puts your commits on top of main, no merge commit
⚠️ Handling Common Issues

1. Uncommitted Changes Blocking Switch

bash
# Save changes temporarily
git stash

# Perform operations
git checkout main
git pull origin main
git checkout your-branch
git rebase main

# Restore changes
git stash pop
2. Merge Conflicts

bash
# When conflict occurs during merge/rebase:

# 1. Check conflicted files
git status

# 2. Open files and resolve (look for <<<<<<<, =======, >>>>>>>)

# 3. Mark as resolved
git add resolved-file.txt

# 4. Continue
git rebase --continue  # or git merge --continue

# 5. If you want to abort
git rebase --abort  # or git merge --abort
3. Branch Doesn't Exist on Remote

bash
# Push branch to remote for first time
git push -u origin branch-name
# -u sets upstream for future git push/pull
4. Force Push After Rebase (Use Carefully!)

bash
# Only if you've rebased and need to update remote
git push origin branch-name --force-with-lease
# Safer than --force, checks for others' changes
📊 Visual Workflow Guide

text
┌─────────────────────────────────────────────┐
│              Start: On Main Branch          │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│        git fetch origin                     │
│        (Get latest from remote)             │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
                 ┌─────────┐
                 │ Choose: │
                 └─────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│  New Branch   │           │ Existing Branch│
├───────────────┤           ├───────────────┤
│ git checkout  │           │ git checkout  │
│   -b new-feat │           │   feature-br  │
└───────┬───────┘           └───────┬───────┘
        │                           │
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│ Start Coding  │           │ git merge main│
│               │           │ or rebase main│
└───────────────┘           └───────┬───────┘
                                    │
                                    ▼
                           ┌───────────────┐
                           │ Push Changes  │
                           │ git push      │
                           └───────────────┘
🔧 Useful Git Aliases (Add to ~/.gitconfig)

ini
[alias]
    # Branch operations
    br = branch
    co = checkout
    cob = checkout -b
    
    # Update workflows
    sync = !git pull --rebase origin main
    update = !git fetch origin && git rebase origin/main
    quick-update = !git stash && git pull --rebase origin main && git stash pop
    
    # Cleanup
    cleanup = !git fetch -p && git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d
    
    # Visual
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
📝 Team Best Practices

Do's:

✅ Fetch regularly - git fetch origin
✅ Rebase feature branches before PR
✅ Write meaningful commit messages
✅ Keep branches focused (one feature per branch)
✅ Delete merged branches locally and remotely

Don'ts:

❌ Commit directly to main
❌ Force push to shared branches
❌ Leave branches unmerged for weeks
❌ Ignore merge conflicts
❌ Push without pulling updates first

Team Workflow Agreement:

main branch = Production-ready code only
develop branch (optional) = Integration branch
feature/* branches = Individual features
hotfix/* branches = Urgent production fixes
🎯 Quick Commands Reference Card

Basic Operations

bash
# View branches
git branch          # Local
git branch -r       # Remote
git branch -a       # All

# Create & move
git branch new-feature      # Create
git checkout new-feature    # Switch
git checkout -b new-feature # Create & switch

# Sync with remote
git push origin branch-name          # Push
git pull origin branch-name          # Pull
git push -d origin old-branch        # Delete remote
Update from Main

bash
# Method A: Rebase (recommended)
git checkout feature-branch
git fetch origin
git rebase origin/main

# Method B: Merge
git checkout feature-branch
git fetch origin
git merge origin/main
Cleanup

bash
# Delete merged branches
git branch --merged main | grep -v "main" | xargs git branch -d

# Prune remote tracking branches
git remote prune origin
🆘 Emergency Commands

Undo last commit (keep changes)

bash
git reset --soft HEAD~1
Undo last commit (discard changes)

bash
git reset --hard HEAD~1
Recover deleted branch

bash
git reflog
git checkout -b recovered-branch <commit-hash>
