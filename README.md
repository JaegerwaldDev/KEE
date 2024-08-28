<h1 align="center"><img src="graphics/kee_github.svg" height="256px"><br>KEE Encryption</h1>

<p align="center"><strong>A way of encryption through the programming of keys.</strong></p>

# Topics

1. [About](#about)
2. [Installation](#installation)
    - [From the Releases](#from-the-releases)
3. [Usage](#usage)
    - [Encrypting/Decrypting files with a key](#encryptingdecrypting-files-with-a-key)
    - [Writing your own keys](#writing-your-own-keys)
        - [About XKEE](#about-xkee)
        - [XKEE Syntax](#xkee-syntax)
        - [Base Concepts](#base-concepts)
        - [XKEE Instructions](#xkee-instructions)
        - [XKEE Arguments](#xkee-arguments)
        - [Compiling `.xkee` to `.kee`](#compiling-xkee-to-kee)
4. [License](#license)

# About

KEE is a joke turned real project. Originally I wanted to have my own cipher system (similar to a caesar cipher) for some of my friends, but then I moved on to ciphering on a binary level, and it became more of an encryption system. After a bit of back-and-forth messaging, I decided to actually make an encryption system and language.

It works by writing whatever you feel is complicated in XKEE (the more you write the better), and then compiling it into the KEE format. With this key, you can start encrypting files, like images, documents, or plain text files. You can then decrypt those files with the same key.

> [!WARNING]
> I believe XKEE is the first of its kind, a language specifically for writing ways to encrypt something. Please let me know if this has been done before, I would be very interested to hear about more of these!

# Installation

> [!NOTE]
> I'm currently looking for a way to turn this into an executable. This _might_ require a rewrite in another language, like Rust. That way it also won't require to install Python 3 and the libraries used.

> [!NOTE]
> If you find it more convenient, make sure to add Python, `kee.py`, and `xkee.py` to PATH. I'm thinking about making an installation script to do this automatically.

## From the Releases

1. Download the [latest releases](https://github.com/JaegerwaldDev/KEE/releases/latest) of `kee.py` (optionally also `xkee.py`) and put them somewhere you'll remember (e.g. `Documents`).

2. **Done!**

# Usage

This section will explain every feature of KEE and XKEY, if you want to skip to certain parts, look [here](https://github.com/JaegerwaldDev/KEE/tree/main?tab=readme-ov-file#topics)!

## Encrypting/Decrypting Files with a key

The recommended option is to copy the file to encrypt into the same folder as the KEE scripts, but you can also use other ways to run the scripts, it doesn't really matter. Make sure you directly run the script like `kee.py` (or `.\kee.py` for PS).

Let's say we have an example file, `my_file.txt`, and it contains the following content:

```txt
My day has been going great!
```

> [!WARNING]
> I am not showing an example of the key used here so that nobody encrypts their files with publicly accessible keys. Please use your own, private, keys in this example.

We can now encrypt our text file with a key called `my_key.kee`!

```cmd
kee.py my_file.txt my_key.kee en
```

> [!NOTE] > `en` can be replaced with `de` to decrypt the file back to its original state.

---

## Writing your own keys

### About XKEE

XKEE is the encryption language that keys are written in. It's a slightly enhanced, plain-text version of the HEX "KEE" format. It compiles to `.kee`, which then can be used for encryption. XKEE looks similar to assembly, but there are differences that we'll talk about in a bit.

### XKEE Syntax

The syntax for XKEE is pretty basic, easy to learn, and easy to understand, even for beginner programmers.

Every line is formatted like a variation of the following syntax:
<br><img src="graphics/xkee_instruction_argument.png">

Sometimes, there aren't any arguments required at all<br>
<img src="graphics/xkee_instruction.png">
<br>Instructions like this often use separate variables for modification.

Of course, you're also able to write comments. They aren't really complex and don't support being inline with another instruction. This serves well enough for most stuff you want to write down, anyway.<br>
<img src="graphics/xkee_comment.png">

Some instructions make use of 2-4 variables for modification, as mentioned above, the syntax for them is formatted like:
<br><img src="graphics/xkee_variable.png"><br>
These are NOT compiled. They exist purely to make the syntax simpler. They are the only instruction that can also be used as an argument at the same time.

### Base Concepts

Whenever a byte exceeds `0xff`, it loops back around to `0x00`

### XKEE Instructions

-   `LGD`: Calculates a linear number gradient between the variables `hx0` and `hx1`, then, every byte gets the number for its position added to itself.
-   `GRD`: Calculates a number gradient between the variables `hx0`, `hx1`, `hx2`, and `hx3`, then, every byte gets the number for its position added to itself.
-   `ADD`: Adds a number to each byte.
-   `SUB`: Subtracts a number from each byte.

### XKEE Arguments

-   `TSP`: The current timestamp modulo 256 to fit within a single byte. This may be changed in the future. This instruction exists to make replicating a key from source code more difficult.
-   `RND`: A random number from `0x00` to `0xff`. This instruction exists to make replicating a key from source code more difficult.

### Compiling `.xkee` to `.kee`

Once you're done writing your key, you can compile it with the following command:

```
xkee.py my_key.xkee
```

Optionally, you can define a name for the compiled key:

```
xkee.py my_key.xkee cool_key.kee
```

If you have any issues when compiling, please report them as an issue! I will try to do my best and fix these issues ASAP.

---

# License

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
