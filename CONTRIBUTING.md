# Contributing to the Project

First off, thank you for considering contributing to this project! This document outlines the standard process for working on the codebase, our branching strategy, and how to handle common Git issues.

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [Your Repository URL]
   cd [Your Repository Name]
   ```

2. **Install dependencies / Setup:**
*(Add any specific instructions here, like `npm install`, `pip install -r requirements.txt`, etc.)*

## 🌿 Branching Strategy and Best Practices

**CRITICAL: Our default development branch is `dev`.**
All new features, bug fixes, and modifications must be branched off of `dev` and merged back into `dev` via a Pull Request (PR). Please **do not** commit directly to `main` or `dev`.

### 1. Update your local `dev` branch

Before starting any new work, make sure your local `dev` branch is up to date:

```bash
git checkout dev
git pull origin dev
```

### 2. Create a new branch

Create a new branch for your specific feature or bug fix. Use a descriptive naming convention:

* **Features:** `feature/short-description` (e.g., `feature/login-page`)
* **Bug Fixes:** `bugfix/short-description` (e.g., `bugfix/header-typo`)
* **Docs/Refactor:** `docs/update-readme` or `refactor/api-calls`

```bash
git checkout -b feature/your-feature-name
```

### 3. Make your changes and commit

Write clear, concise commit messages. A good commit message explains *what* changed and *why*.

```bash
git add .
git commit -m "Add: User login form validation"

```

### 4. Push your branch

```bash
git push origin feature/your-feature-name

```

### 5. Open a Pull Request (PR)

Go to the repository on GitHub and open a PR.

* **Base branch:** `dev` (Ensure this is selected!)
* **Compare branch:** `feature/your-feature-name`
* Add a brief description of what your code does and request a review from a teammate.

---

## 🛠 Troubleshooting: Common Merge Problems

Working with Git in a team almost always leads to a few hiccups. Here is how to solve the most common ones.

### Problem 1: "Merge Conflicts"

**What happened:** You and a teammate edited the exact same lines of code in the same file, and Git doesn't know whose changes to keep.
**How to fix it:**

1. In your PR on GitHub, it will say "This branch has conflicts that must be resolved."
2. Pull the latest `dev` branch into your current feature branch locally:
```bash
git checkout feature/your-feature-name
git pull origin dev


```



```
3. Open the conflicting files in your code editor (like VS Code). You will see markers like `<<<<<<< HEAD`, `=======`, and `>>>>>>> dev`.
4. Manually edit the file to keep the correct code, and delete the `<<<<<<<`, `=======`, and `>>>>>>>` markers.
5. Save the file, commit the resolution, and push:
   ```bash
   git add .
   git commit -m "Fix merge conflicts with dev"
   git push origin feature/your-feature-name
   

```

### Problem 2: "My branch is behind `dev`"

**What happened:** While you were working on your feature, someone else merged their PR into `dev`. Your branch is now missing their updates.
**How to fix it:** Update your branch by pulling from `dev`. It is a good practice to do this daily to avoid massive merge conflicts later.

```bash
git pull origin dev

```

### Problem 3: I accidentally committed directly to `dev`!

**What happened:** You forgot to create a branch and started writing code/committing on `dev`.
**How to fix it:**
If you haven't pushed yet, you can move your commits to a new branch:

```bash
# Create and switch to a new branch with your commits
git checkout -b feature/my-new-work

# Switch back to dev
git checkout dev

# Reset dev to match the remote version (undoing your local commits on dev)
git reset --hard origin/dev

# Go back to your feature branch to continue working
git checkout feature/my-new-work

```
