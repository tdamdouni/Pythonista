# Pythonista/spellGen

spellGen is a simple, pbkdf2-based password generator utility.

It allows the generation of mnemonic password bases for any number of services and accounts, including the ability to generate 9 different "iterations" of passwords for a single service/account pair in case a password is compromised and needs to be replaced.

It stores a user-provided secret to be used in generating the passes in the keychain.

The core idea is from old Famicom (Japanese NES) games, which used password systems for 'saving' the game state. Unlike western versions, the Japanese passwords were uncannily mnemonic, thanks to the rather limited syllable set of the Japanese language.

To achieve similar results, spellGen uses a base66 representation of the hash function's output, with each digit represented by a syllable. The result is a pronounceable string, a substring of which may be used as a convenient and mnemonic password.

I didn't go out of my way to crop the string to size, add uppercase letters, numbers or non-alphanumeric characters. When used correctly, the app gives you plenty of entropy; feel free to just add '-1' to the end of all passwords or something.