<p align="center">
  <a href="https://RedstoneCoreDev.github.io/MasioASM/">
    <img src="MasioASM.svg" alt="MasioASM Logo" width="300">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arch-x86__64-blue" alt="Architecture">
  <a href="https://RedstoneCoreDev.github.io/MasioASM/documentation.html">
    <img src="https://img.shields.io/badge/Linux-first-green" alt="Linux-first">
  </a>
  <a href="https://RedstoneCoreDev.github.io/MasioASM/">
    <img src="https://img.shields.io/badge/Website-Documentation-orange" alt="Documentation">
  </a>
</p>

---

**MasioASM** is a custom compiled language ecosystem for `.masio` files. It transforms clean, readable MasioASM code into standard NASM code through a structured, multi-pass pipeline. By introducing custom nominal typing, embedded code styles, and powerful macro expansion, it brings modern safety ergonomics and high-level design to low-level x86_64 programming.

Check out the full [MasioASM Documentation Website](https://RedstoneCoreDev.github.io/MasioASM/documentation.html).

---

## Project Goals

- **Understand Assembly:** Demystify Assembly and make it safer without sacrificing raw performance.

- **Make Learning Easier:** Lower the barrier of entry for anyone wanting to learn systems and assembly programming.

- **Reduce Code:** Write concise, self-documenting instructions while retaining full x86_64 power.

- **Build Things:** Create practical applications and tools entirely in MasioASM.

---

## Features

- **NASM Transpilation:** Translates clean MasioASM source files into standard NASM code for robust building and linking.
- **`zero`**: Translates to `xor`.
- **`fn`**: Functions.
- **`FSetup`**: Frame Setup.
- **`FDestroy`**: Frame Destroy.
- **`return`**: Figures out how it should return (e.g. if it is in _start or not).
- **`print`**: Adds the function for printing into the translated `.nasm` file.
- **`comments`**: Valid comments are `//`, `#`, `--`, `;`. Can be later strictly defined with `codestyle` keyword when the Feature gets added.

## Coming Features

- **Multi-Pass Compiler Architecture:** Advanced pipeline that normalizes indentation, handles block parsing, and builds clean internal structures.
- **File-Embedded Governance (`codestyle`):** Source-level strictness controls for error and warning handling.
- **Custom Nominal Types:** Semantic typing to prevent incompatible operations at compile-time.
- **`map` Bindings:** Compile-time bindings for values, constants (`magic`), and states.
- **`macro` System:** Flexible code expansion supporting single-line shorthands and multi-line blocks with `end`.
- **`if`:** Native conditional branching.
- **`loop`:** Clean iteration constructs.
- **`public` & `private`:** Visibility scoping for modular organization.
