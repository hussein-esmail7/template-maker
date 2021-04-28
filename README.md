# template-maker
This program generates those boilerplate files that you always happen to need.

# Table of Contents
- [What is this?](#what-is-this)
- [Installation](#installation)
- [Usage](#usage)

# What is this?

This program is meant to create the template files that you normally need. My goal is to make it as customizable as possible so you can make it your own.

# Installation

At the moment, you can only `git clone` this repository, but I an hoping to put it on Homebrew soon.

## Installing through Git
```
git clone https://github.com/hussein-esmail7/template-maker
cd template-maker
./INSTALL
```
If you want to run this program in Terminal just by typing the program name, you would have to add an alias in your `.bashrc` file. If you do this, you should alias to the `main.sh` file.

## Running the program

To use this program, you have to make sure you are in the correct directory, and that the file has executable permission.
```
cd template-maker
chmod +x template-maker
```

Personally, I assigned the file `template-maker` as an alias in my `.bashrc` so whichever directory I'm in, I can just type `template <args>` and it will make the file I need right there.

## Arguments

When running this program, you can pass the file name with an extension in the command line arguments. If you don't, it will ask you what type of file you want and will use the default or pre-defined file name.
